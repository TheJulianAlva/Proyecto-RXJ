from OpenGL.GL import *
from OpenGL.GLU import *
from systems.texture_manager import TextureManager
from systems.collision_system import CollisionSystem
from game_objects.puzzles.statue import Statue
from game_objects.environment.door import Door
<<<<<<< Updated upstream
from game_objects.ui_elements.text_message import TextMessage
=======
>>>>>>> Stashed changes

class StatuePuzzle:
    """
    Puzzle que consiste en varias estatuas que deben ser rotadas
    a una orientación específica para resolver el acertijo.
    """
    def __init__(self, puzzle_data, display_width, display_height):
        self.texture_manager = TextureManager.instance()
        self.solved = False
        self.display_width = display_width
        self.display_height = display_height
        
        props = puzzle_data.get("properties", {})
        statues_config = props.get("statues", [])
            
        self.statues = []
        self.interactables = []
        ordered_candidates = []

        for s_data in statues_config:
            statue_position = s_data.get("position", [0, 0, 0])
            asset_name = s_data.get("asset")
            tex_id = self.texture_manager.get_texture(asset_name)
            
            new_statue = Statue(
                id=s_data.get("id", "Estatua Desconocida"),
                position=statue_position,
                size=s_data.get("size", [1, 2, 1]),
                rotation=[90, 0, 1, 0],
                name=s_data.get("name", "Estatua Desconocida"),
                phrase=s_data.get("phrase", "Estatua Desconocida"),
                tex_id=tex_id
            )
            self.statues.append(new_statue)
            self.interactables.append(new_statue)
            ordered_candidates.append(new_statue)
        self.door = Door([-34.5, 5.0, 5.0], [1.0, 10.0, 4.0], [0, 0, 0, 1], self.texture_manager.get_texture("tex_floor"))
        self.interactables.append(self.door)
        self.interaction_radius = 8.0
        self.selected_statue = None
        expected_names = props.get(
            "expected_order_names",
            ["el_camaleon", "el_siervo", "el_caudillo"],
        )
        self.expected_order = [name.lower().replace(" ", "_") for name in expected_names]
        self.success_message_shown = False

        self.selection_highlight_color = (1.0, 0.9, 0.2)
        self.success_highlight_color = (0.2, 0.9, 0.2)
        axis_index = self._resolve_primary_axis(ordered_candidates)
        self._slot_axis_index = axis_index
        ordered_candidates.sort(
            key=lambda statue: statue.position[self._slot_axis_index],
            reverse=True,
        )
        self.slot_positions = [list(statue.position) for statue in ordered_candidates]
        self.current_order = list(ordered_candidates)
        self._apply_current_order()
        self._update_highlights()
        print(f"StatuePuzzle inicializado con {len(self.statues)} estatuas.")
        self.active_message = None

    def update(self, delta_time):
        """
        Actualiza eventos y comprueba si se resolvió.
        """
        if self.solved:
            return
        if self.active_message:
            self.active_message.update(delta_time)

    def can_interact(self, player_pos, player_rotation):
        """
        Llamado cada frame para mostrar UI de interacción.
        Determina qué estatua está cerca y muestra su información.
        """
        target_object = CollisionSystem.cast_ray(
            player_pos, 
            player_rotation, 
            self.interactables,
            max_distance=self.interaction_radius
        )
        
        return bool(target_object)

        
    def draw(self):
        """
        Dibuja todas las estatuas del puzzle.
        """
        for interactable in self.interactables:
            interactable.draw()
        if self.active_message:
            self.active_message.draw()

    def interact(self, player_pos, player_rotation):
        """
        Llamado cuando el jugador pulsa 'E'.
        Determina qué estatua está cerca y muestra su información.
        """
        target_object = CollisionSystem.cast_ray(
            player_pos,
            player_rotation,
            self.interactables,
            max_distance=self.interaction_radius,
        )
        
        if isinstance(target_object, Statue):
<<<<<<< Updated upstream
            self._show_message(f"Interactuando con: {target_object.name}")
=======
            if self.solved:
                print("El acertijo ya está resuelto. No necesitas mover más las estatuas.")
                return
            self._handle_statue_selection(target_object)
>>>>>>> Stashed changes
        elif isinstance(target_object, Door):
            if self.solved:
                target_object.interact()
            else:
                print("La puerta permanece cerrada. Acomoda las estatuas en el orden correcto.")
        else:
            print("No hay ninguna estatua enfrente para interactuar.")

        return target_object

    def is_completed(self):
        return self.solved
<<<<<<< Updated upstream
    
    def _show_message(self, text):
            self.active_message = TextMessage(
            text=text,
            duration=3.0,
            y_pos=self.display_height*0.5
        )
=======

    def _statue_key(self, statue):
        return statue.name.lower().replace(" ", "_")

    def _resolve_primary_axis(self, statues):
        if not statues:
            return 0

        positions = [statue.position for statue in statues]
        range_x = max(pos[0] for pos in positions) - min(pos[0] for pos in positions)
        range_z = max(pos[2] for pos in positions) - min(pos[2] for pos in positions)
        if range_z >= range_x:
            return 2
        return 0

    def _apply_current_order(self):
        for slot_position, statue in zip(self.slot_positions, self.current_order):
            statue.set_position(slot_position)

    def _handle_statue_selection(self, statue):
        if self.selected_statue is None:
            self.selected_statue = statue
            print(f"Seleccionaste '{statue.name}'. Elige otra estatua para intercambiar.")
            self._update_highlights()
            return

        if self.selected_statue is statue:
            print(f"Se canceló la selección de '{statue.name}'.")
            self.selected_statue = None
            self._update_highlights()
            return

        self._swap_statues(self.selected_statue, statue)
        self.selected_statue = None
        self._check_solution()
        self._update_highlights()

    def _swap_statues(self, first, second):
        try:
            index_a = self.current_order.index(first)
            index_b = self.current_order.index(second)
        except ValueError:
            print("Error interno: no se encontró una estatua seleccionada en el orden actual.")
            return

        self.current_order[index_a], self.current_order[index_b] = self.current_order[index_b], self.current_order[index_a]
        self._apply_current_order()
        print(f"Intercambiaste las posiciones de '{first.name}' y '{second.name}'.")

    def _check_solution(self):
        current_keys = [self._statue_key(statue) for statue in self.current_order]
        if current_keys == self.expected_order:
            self.solved = True
            if not self.success_message_shown:
                print(
                    "¡Orden correcto! De derecha a izquierda: El Camaleon, El Siervo y El Caudillo. Un mecanismo se activa."
                )
                self.success_message_shown = True
            self.door.unlock()
            self._update_highlights()
        else:
            print(
                "Orden actual (derecha a izquierda): "
                + ", ".join(current_keys)
                + ". Sigue intentando."
            )

    def _update_highlights(self):
        if self.solved:
            for statue in self.statues:
                statue.set_highlight_color(self.success_highlight_color)
            return

        for statue in self.statues:
            if statue is self.selected_statue:
                statue.set_highlight_color(self.selection_highlight_color)
            else:
                statue.set_highlight_color(None)
>>>>>>> Stashed changes
