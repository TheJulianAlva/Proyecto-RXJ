from OpenGL.GL import *
from systems.texture_manager import TextureManager
from systems.collision_system import CollisionSystem
from game_objects.puzzles.statue import Statue
from game_objects.puzzles.pedestal import Pedestal
from game_objects.environment.door import Door
from game_objects.ui_elements.text_message import TextMessage

class StatuePuzzle:
    def __init__(self, puzzle_data, display_width=800, display_height=600):
        self.texture_manager = TextureManager.instance()
        self.display_width, self.display_height = display_width, display_height
        self.solved = False
        self.active_message = None
        self.selected_statue = None
        
        props = puzzle_data.get("properties", {})
        
        # region Instancias Pedestals
        pedestals_conf = props.get("pedestals", [])
        self.pedestals = []
        self.slots_positions = []
        pedestal_tex = self.texture_manager.get_texture("tex_pedestal")
        
        for pedestal_data in pedestals_conf:
            pos = pedestal_data.get("position", [0,0,0])
            statue_offset = pedestal_data.get("statue_offset", 3.0)
            new_pedestal = Pedestal(
                position=pos,
                size=pedestal_data.get("size", [1.0, 1.0, 1.0]),
                phrase=pedestal_data.get("phrase", ""),
                correct_statue_id=pedestal_data.get("correct_statue_id"),
                tex_id=pedestal_tex
            )
            self.pedestals.append(new_pedestal)
            # La posición de la estatua será encima del pedestal (y + offset)
            statue_pos = [pos[0], pos[1] + statue_offset, pos[2]] 
            self.slots_positions.append(statue_pos)
        # endregion

        # region Instancias Statues Desordenadas
        statues_config = props.get("statues", [])
        self.statues = [] # Esta lista NO cambia de orden
        self.current_statues_order = [None] * len(self.pedestals) # Esta lista guarda [StatueA, StatueC, StatueB]
        
        for statue_data in statues_config:
            tex_id = self.texture_manager.get_texture(statue_data.get("asset"))
            slot_index = statue_data.get("initial_slot", 0)
            
            initial_pos = list(self.slots_positions[slot_index])
            
            new_statue = Statue(
                id=statue_data.get("id"),
                position=initial_pos,
                size=statue_data.get("size", [1, 2, 1]),
                rotation=statue_data.get("rotation", [90, 0, 1, 0]),
                name=statue_data.get("name"),
                tex_id=tex_id
            )
            new_statue.highlight_color = None
            self.statues.append(new_statue)
            self.current_statues_order[slot_index] = new_statue
        # endregion

        # region Instancia Door
        door_config = props.get("door_config", {})
        self.door = Door(
            position=door_config.get("position", [0,0,0]),
            size=door_config.get("size", [1,2,1]),
            rotation=door_config.get("rotation", [0,0,0,1]),
            tex_id=self.texture_manager.get_texture(door_config.get("texture_asset")),
            is_locked=True
        )
        # endregion

        self.touch_interactables = self.statues + [self.door]
        self.read_interactables = self.pedestals
        self.interaction_radius = 8.0
        print("Puzzle Histórico cargado.")

    def update(self, delta_time):
        if self.active_message: self.active_message.update(delta_time)

    def draw(self):
        for obj in self.touch_interactables:
            if obj != self.selected_statue:
                obj.draw()
        if self.active_message: self.active_message.draw()

    def interact(self, player_pos, player_rot):
        target = CollisionSystem.cast_ray(player_pos, player_rot, self.touch_interactables, self.interaction_radius)
        if not target: return None

        if isinstance(target, Statue):
            self._handle_statue_selection(target)

        elif isinstance(target, Door):
            if self.solved:
                if target.interact(): return "LEVEL_COMPLETE"
            else:
                self._show_message("La puerta está cerrada. La historia debe ser corregida.")
        
        return target

    def read_interact(self, player_pos, player_rot):
        target = CollisionSystem.cast_ray(player_pos, player_rot, self.read_interactables, self.interaction_radius)
        if not target: return None

        elif isinstance(target, Pedestal):
            self._show_message(f"Inscripción: \"{target.phrase}\"")

        return target

    def can_touch_interact(self, player_pos, player_rot):
        target = CollisionSystem.cast_ray(player_pos, player_rot, self.touch_interactables, self.interaction_radius)
        return True if target else False
    
    def can_read_interact(self, player_pos, player_rot):
        target = CollisionSystem.cast_ray(player_pos, player_rot, self.read_interactables, self.interaction_radius)
        return True if target else False

    def _handle_statue_selection(self, statue):
        if self.selected_statue is None:
            self.selected_statue = statue
            self._show_message(f"Seleccionado: {statue.name}. Elige otra posición.")
        elif self.selected_statue is statue:
            self.selected_statue = None
            self._show_message("Selección cancelada.")
        else:
            self._swap_statues(self.selected_statue, statue)
            self.selected_statue = None
            self._check_solution()

    def _swap_statues(self, statue_1, statue_2):
        index_1 = self.current_statues_order.index(statue_1)
        index_2 = self.current_statues_order.index(statue_2)
        
        # Intercambiar en la lista lógica
        self.current_statues_order[index_1], self.current_statues_order[index_2] = \
            self.current_statues_order[index_2], self.current_statues_order[index_1]
            
        # Actualizar posiciones físicas
        statue_1.set_position(list(self.slots_positions[index_2]))
        statue_2.set_position(list(self.slots_positions[index_1]))
        
        self._show_message("Estatuas intercambiadas.")

    def _check_solution(self):
        correct_count = 0
        for i, pedestal in enumerate(self.pedestals):
            statue_on_top = self.current_statues_order[i]
            if statue_on_top.id == pedestal.correct_statue_id:
                correct_count += 1
        
        if correct_count == len(self.pedestals):
            self.solved = True
            self.door.unlock()
            self._show_message("¡Click! La historia está en orden. La puerta se abre.")

    def _show_message(self, text):
        self.active_message = TextMessage(text, duration=5.0, y_pos=800, font_size=28)