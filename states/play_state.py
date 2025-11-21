"""
Implementa el estado principal del juego (3D). 
Gestiona la lógica del jugador (update, draw) y la 
cámara 3D activa (apply_view) en cada fotograma.
"""
from states.base_state import BaseState
from systems.data_manager import DataManager
from systems.camera_manager import CameraManager
from systems.input_manager import InputManager
from systems.texture_manager import TextureManager
import os
from game_objects.character_models.santo import SantoSkin
from game_objects.character_models.alien import AlienSkin
from game_objects.character_models.walter import WalterSkin
from game_objects.player import Player
from OpenGL.GL import *
from utilities import basic_objects as Objects

class PlayState(BaseState):
    def __init__(self, engine):
        super().__init__(engine)
        self.engine = engine
        self.engine.setup_3d_perspective()
        data_manager = DataManager.instance()
        player_config = data_manager.load_game_data()
        skins = [SantoSkin, AlienSkin, WalterSkin]
        selected_index = player_config.get("character_index", 0)
        selected_skin = skins[selected_index]
        self.player = Player(0, 0, 0, selected_skin)
        self.input_manager = InputManager.instance()
        self.cam_manager = CameraManager.instance()
        
        # --- Texturas de escena (nivel 1) ---
        self.texture_manager = TextureManager.instance()
        # Rutas relativas dentro del proyecto
        self.floor_texture = self.texture_manager.get_texture("floor_lvl_1", "assets/scenes/floor_lvl_1.png")
        self.walls_texture = self.texture_manager.get_texture("walls_lvl_1", "assets/scenes/Walls_lvl_1.png")

        # Parámetros del mundo (área rectangular centrada en origen)
        # Ajusta estos valores si quieres un área mayor/menor
        self.world_half_extent = 20.0  # ± en X/Z
        self.wall_height = 8.0

        # Cargar dinámicamente todas las imágenes de `assets/scenes`
        self.scene_textures = {}
        try:
            scene_dir = "assets/scenes"
            for fname in sorted(os.listdir(scene_dir)):
                if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
                    continue
                key = os.path.splitext(fname)[0]
                full_path = f"{scene_dir}/{fname}"
                tex_id = self.texture_manager.get_texture(key, full_path)
                self.scene_textures[key] = tex_id
        except Exception as e:
            print(f"Advertencia: no se pudieron cargar texturas de 'assets/scenes': {e}")

    def update(self, delta_time, _event_list):
        # Abrir pausa con la acción "pause" (tecla 'P')
        if self.input_manager.was_action_pressed("pause"):
            from states.pause_state import PauseState
            self.engine.push_state(PauseState(self.engine))
            return

        if self.input_manager.was_action_pressed("return"):
            self.engine.pop_state()
            return
        self.player.update(delta_time)

    def draw(self):
        _active_cam = self.cam_manager.get_active_camera()
        if _active_cam:
            _active_cam.apply_view()
        else:
            print("¡Advertencia! No hay cámara activa.")
        # Dibujar geometría del nivel (piso y paredes) antes del jugador
        self._draw_level_textures()
        self.player.draw()

    def _draw_level_textures(self):
        """
        Dibuja un suelo texturizado y 4 paredes alrededor del área central.
        Asume que `self.floor_texture` y `self.walls_texture` contienen IDs válidos
        (cargados con `TextureManager.get_texture`).
        """
        # Seguridad: si alguna textura no está disponible, no intentar bindearla
        glEnable(GL_TEXTURE_2D)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

        # --- Piso ---
        if self.floor_texture and self.floor_texture != -1:
            glBindTexture(GL_TEXTURE_2D, self.floor_texture)
            glColor4f(1.0, 1.0, 1.0, 1.0)
            # Un plano amplio en X/Z
            Objects.draw_textured_plane_3d(size_x=self.world_half_extent*2, size_z=self.world_half_extent*2, translate=[0, 0, 0])

        # --- Paredes (4 caras) ---
        if self.walls_texture and self.walls_texture != -1:
            glBindTexture(GL_TEXTURE_2D, self.walls_texture)
            glColor4f(1.0, 1.0, 1.0, 1.0)

            # Pared trasera (al fondo, -Z)
            Objects.draw_textured_plane_3d(size_x=self.world_half_extent*2, size_z=self.wall_height,
                                          translate=[0, self.wall_height/2.0, -self.world_half_extent], rotation=[90, 1, 0, 0])

            # Pared frontal (+Z)
            Objects.draw_textured_plane_3d(size_x=self.world_half_extent*2, size_z=self.wall_height,
                                          translate=[0, self.wall_height/2.0, self.world_half_extent], rotation=[-90, 1, 0, 0])

            # Pared izquierda (-X)
            Objects.draw_textured_plane_3d(size_x=self.world_half_extent*2, size_z=self.wall_height,
                                          translate=[-self.world_half_extent, self.wall_height/2.0, 0], rotation=[90, 0, 0, 1])

            # Pared derecha (+X)
            Objects.draw_textured_plane_3d(size_x=self.world_half_extent*2, size_z=self.wall_height,
                                          translate=[self.world_half_extent, self.wall_height/2.0, 0], rotation=[-90, 0, 0, 1])

        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)
        