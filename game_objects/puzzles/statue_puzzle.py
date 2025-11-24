from OpenGL.GL import *
from OpenGL.GLU import *
from systems.texture_manager import TextureManager
from systems.collision_system import CollisionSystem
from game_objects.puzzles.statue import Statue

class StatuePuzzle:
    """
    Puzzle que consiste en varias estatuas que deben ser rotadas
    a una orientación específica para resolver el acertijo.
    """
    def __init__(self, puzzle_data):
        self.texture_manager = TextureManager.instance()
        self.solved = False
        
        props = puzzle_data.get("properties", {})
        statues_config = props.get("statues", [])
            
        self.statues = [] # Lista de objetos Statue
        
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
            
        
        self.interaction_radius = 8.0
        print(f"StatuePuzzle inicializado con {len(self.statues)} estatuas.")

    def update(self, delta_time):
        """
        Actualiza eventos y comprueba si se resolvió.
        """
        if self.solved:
            return

        for statue in self.statues:
            statue.update(delta_time)

    def draw(self):
        """
        Dibuja todas las estatuas del puzzle.
        """
        for statue in self.statues:
            statue.draw()

    def interact(self, player_pos, player_rotation):
        """
        Llamado cuando el jugador pulsa 'E'.
        Determina qué estatua está cerca y muestra su información.
        """
        if self.solved:
            print("El puzzle ya está resuelto.")
            return

        target_statue = CollisionSystem.cast_ray(
            player_pos, 
            player_rotation, 
            self.statues,
            max_distance=self.interaction_radius
        )
        
        if target_statue:
            print(f"Interactuando con: {target_statue.name}")
        else:
            print("No hay ninguna estatua enfrente para interactuar.")

    def is_completed(self):
        return self.solved