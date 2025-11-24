from OpenGL.GL import *
from OpenGL.GLU import *
from systems.texture_manager import TextureManager
from systems.collision_system import CollisionSystem
from game_objects.puzzles.statue import Statue
from game_objects.environment.door import Door
from game_objects.ui_elements.text_message import TextMessage

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
        self.door = Door([-34.5, 5.0, 5.0], [1.0, 10.0, 4.0], [0, 0, 0, 1], self.texture_manager.get_texture("tex_floor"))
        self.interactables.append(self.door)
        self.interaction_radius = 8.0
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
        target_statue = CollisionSystem.cast_ray(
            player_pos, 
            player_rotation, 
            self.interactables,
            max_distance=self.interaction_radius
        )
        
        return True if target_statue else False

        
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
        if self.solved:
            print("El puzzle ya está resuelto.")
            return

        target_object = CollisionSystem.cast_ray(
            player_pos, 
            player_rotation, 
            self.interactables,
            max_distance=self.interaction_radius
        )
        
        if isinstance(target_object, Statue):
            self._show_message(f"Interactuando con: {target_object.name}")
        elif isinstance(target_object, Door):
            print("Interactuando con puerta.")
        else:
            print("No hay ninguna estatua enfrente para interactuar.")

        return target_object

    def is_completed(self):
        return self.solved
    
    def _show_message(self, text):
            self.active_message = TextMessage(
            text=text,
            duration=3.0,
            y_pos=self.display_height*0.5
        )