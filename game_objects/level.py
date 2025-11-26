from OpenGL.GL import *
from utilities import basic_objects as Objects
from systems.texture_manager import TextureManager
from game_objects.environment.collider import AABB
from game_objects.puzzles.statue_puzzle import StatuePuzzle

class Level:
    """
    Clase que construye y renderiza un nivel completo basándose en
    un diccionario de datos (cargado desde un JSON).
    """
    def __init__(self, level_data, display_width, display_height):
        self.data = level_data
        self.texture_manager = TextureManager.instance()
        
        print(f"Cargando Nivel: {level_data.get('metadata', {}).get('name', 'Desconocido')}")
        
        # --- 1. CARGA DE ASSETS ---
        assets_config = level_data.get("assets", {})
        textures_config = assets_config.get("textures", {})
        
        for tex_key, tex_path in textures_config.items():
            self.texture_manager.load_texture(tex_key, tex_path)
            
        self.lighting_data = level_data.get("lighting", {})
        
        self.layout_data = level_data.get("layout", {})
        
        floor_tex_key = self.layout_data.get("floor", {}).get("texture_id")
        self.floor_texture_id = self.texture_manager.get_texture(floor_tex_key)
        
        walls_list = self.layout_data.get("walls", [])

        self.solid_colliders = []
        
        for wall in walls_list:
            pos = wall.get("pos", [0, 0, 0])
            size = wall.get("size", [1, 1, 1])
            
            half_size_x = size[0] / 2.0
            half_size_z = size[2] / 2.0
            
            min_point = [pos[0] - half_size_x, pos[2] - half_size_z]
            max_point = [pos[0] + half_size_x, pos[2] + half_size_z]
            
            wall_collider = AABB(min_point, max_point)
            self.solid_colliders.append(wall_collider)
            
        print(f"Nivel generado con {len(self.solid_colliders)} paredes sólidas.")
        self.can_interact = False

        # --- 4. PUZZLE ---
        self.puzzle = None
        if "puzzle_config" in level_data:
            puzzle_config = level_data.get("puzzle_config")
            self.puzzle = StatuePuzzle(puzzle_config, display_width, display_height)
            for statue in self.puzzle.statues:
                self.solid_colliders.append(statue.get_AABB())
            pass
        if self.puzzle: self.puzzle.play_intro()

    def update(self, delta_time):
        # Actualizar el puzzle si existe
        if self.puzzle:
            self.puzzle.update(delta_time)
            

    def handle_interaction(self, player_pos, player_rotation):
        """
        Llamado por PlayState cuando el jugador pulsa 'Interactuar'.
        Delega la acción al puzzle si el jugador está cerca.
        """
        if self.puzzle:
            self.puzzle.interact(player_pos, player_rotation)

    def handle_read_interaction(self, player_pos, player_rotation):
        """
        Llamado por PlayState cuando el jugador pulsa 'Interactuar'.
        Delega la acción al puzzle si el jugador está cerca.
        """
        if self.puzzle:
            self.puzzle.read_interact(player_pos, player_rotation)

    def destroy(self):
        """Libera recursos al salir del nivel."""
        assets_config = self.data.get("assets", {})
        for tex_key in assets_config.get("textures", {}).keys():
            self.texture_manager.unload_texture(tex_key)
        print("Nivel liberado.")

    def draw(self):
        self._setup_lighting()

        self._draw_layout()
        
        if self.puzzle:
            self.puzzle.draw()

    def _setup_lighting(self):
        """Configura las luces según el JSON, iterando sobre las disponibles."""
        # 1. Luz Ambiental Global (Afecta a todo por igual)
        ambient = self.lighting_data.get("ambient_color", [0.2, 0.2, 0.2, 1.0])
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient)
        
        # 2. Obtener la lista de luces del JSON
        lights_config = self.lighting_data.get("lights", [])
        
        # 3. Iterar sobre las luces disponibles en el hardware (GL_LIGHT0 a GL_LIGHT7)
        # El máximo suele ser 8 en OpenGL clásico.
        max_lights = 8 
        
        for i in range(max_lights):
            light_id = GL_LIGHT0 + i # Calcula el ID de OpenGL (ej. 16384 + 0)
            
            if i < len(lights_config):
                l_data = lights_config[i]
                
                glEnable(light_id)
                
                # Posición (x, y, z, w)
                # w=1.0 es posicional (foco/bombilla), w=0.0 es direccional (sol)
                pos = l_data.get("position", [0.0, 0.0, 0.0, 1.0])
                glLightfv(light_id, GL_POSITION, pos)
                
                # Colores
                diffuse = l_data.get("diffuse", [1.0, 1.0, 1.0, 1.0])
                specular = l_data.get("specular", [1.0, 1.0, 1.0, 1.0])
                glLightfv(light_id, GL_DIFFUSE, diffuse)
                glLightfv(light_id, GL_SPECULAR, specular)
                
                # Atenuación (Opcional, pero recomendada para luces puntuales)
                attenuation = l_data.get("attenuation", [1.0, 0.0, 0.0])
                glLightf(light_id, GL_CONSTANT_ATTENUATION, attenuation[0])
                glLightf(light_id, GL_LINEAR_ATTENUATION, attenuation[1])
                glLightf(light_id, GL_QUADRATIC_ATTENUATION, attenuation[2])
                
                # Soporte para Focos (Spotlights) si el JSON lo define
                if l_data.get("type") == "spot":
                    direction = l_data.get("direction", [0.0, -1.0, 0.0])
                    cutoff = l_data.get("cutoff", 45.0) # Ángulo del cono
                    exponent = l_data.get("exponent", 0.0) # Enfoque/Suavidad
                    
                    glLightfv(light_id, GL_SPOT_DIRECTION, direction)
                    glLightf(light_id, GL_SPOT_CUTOFF, cutoff)
                    glLightf(light_id, GL_SPOT_EXPONENT, exponent)
                else:
                    # Si no es spot, asegurarnos de que sea omnidireccional
                    # (180.0 es el valor mágico para desactivar el efecto spot)
                    glLightf(light_id, GL_SPOT_CUTOFF, 180.0)

            else:
                # Es CRUCIAL apagar las luces sobrantes que pudieran haber quedado
                # encendidas de un nivel anterior.
                glDisable(light_id)

    def _draw_layout(self):
        if self.floor_texture_id != -1:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.floor_texture_id)
            
            glColor3f(1.0, 1.0, 1.0) 
            
            floor_size = self.layout_data.get("floor", {}).get("size", [10, 10])
            floor_tiling = self.layout_data.get("floor",{}).get("tiling", [1.0, 1.0])
            Objects.draw_textured_plane_3d(size_x=floor_size[0], size_z=floor_size[1], tiling=floor_tiling)
            
            glDisable(GL_TEXTURE_2D)
        
        # --- PAREDES ---
        walls = self.layout_data.get("walls", [])
        for wall in walls:
            tex_id = self.texture_manager.get_texture(wall.get("texture_id"))
            
            if tex_id != -1:
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, tex_id)
                glColor3f(1.0, 1.0, 1.0)
                
                pos = wall.get("pos", [0, 0, 0])
                size = wall.get("size", [1, 1, 1]) 

                Objects.draw_textured_box(
                    size=size,
                    translate=pos
                )
                glDisable(GL_TEXTURE_2D)
            else:
                glColor3f(0.5, 0.5, 0.5)
                Objects.draw_cube(scale=wall.get("size"), translate=wall.get("pos"))
