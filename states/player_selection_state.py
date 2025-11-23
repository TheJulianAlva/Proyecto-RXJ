"""
Implementa el estado de selección de personaje (3D).
Presenta una escena 3D con cámara fija donde el jugador puede
elegir entre 3 personajes antes de iniciar el juego.
"""

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from .base_state import BaseState
from systems.data_manager import DataManager
from systems.input_manager import InputManager
from systems.texture_manager import TextureManager
from utilities.text_renderer import draw_text_2d
from utilities import basic_objects as Objects
from game_objects.camera import Camera
from game_objects.selection_menu.character_selection_platform import CharacterSelectionPlatform
from utilities.instructions_overlay import draw_instructions

class PlayerSelectionState(BaseState):
    
    def __init__(self, engine):
        super().__init__(engine)
        self.input_manager = InputManager.instance()
        data_manager = DataManager.instance()
        self.texture_manager = TextureManager.instance()
        config = data_manager.get_config()

        display_config = config.get("rendered_display", {})
        self.display_width = display_config.get("width", 1280)
        self.display_height = display_config.get("height", 720)
        
        data_selection = data_manager.get_text_dict().get("selection_state", {})
        self.character_names = data_selection.get("banner_names", ["El Maskara", "Marciana", "Walter"])

        self.engine.setup_3d_perspective()
        glEnable(GL_LIGHTING)
        self.character_selection_platform = CharacterSelectionPlatform(0.0, 0.0, 0.0)
        self.background_color = (0.0, 0.0, 0.0, 1.0)
        self.camera = Camera(position=[0, 5, 19], look_at=[0, 4, 0])
        
        self.selected_index = 0
        self.platform_rotation = 0.0
        # 0 = Personaje 0, 120 = Personaje 1, 240 = Personaje 2
        self.target_rotation = 0.0 

        self.banner_color = [0.5, 0.2, 0.2, 0.7]
        margin = self.display_width * 0.2
        banner_width = self.display_width - 2 * margin
        banner_height = margin / 2
        self.banner_rect = pygame.Rect(margin, self.display_height-margin, banner_width, banner_height)
        self.montserrat_font = "montserrat_bold"

        background_files = [
            "assets/background/menu_selection_0.png",
            "assets/background/menu_selection_1.png",
            "assets/background/menu_selection_2.png"]
        self.background_textures = [
            self.texture_manager.get_texture("bg_selection_0", background_files[0]),
            self.texture_manager.get_texture("bg_selection_1", background_files[1]),
            self.texture_manager.get_texture("bg_selection_2", background_files[2])
            ]
        
        # VARIABLES ANIMACION FONDOS
        self.fade_alpha = 1.0
        self.fade_state = "IDLE"       # Estados: IDLE, FADE_OUT, FADE_IN
        self.fade_speed = 3.0
        self.display_index = 0
        
        self.background_rect = (38.4, 25.6, 0.0, 7.0, -5.0)
        self.instructions_lines = [
            "Flechas o A/D: Cambiar personaje",
            "E, Enter o S: Confirmar selección",
            "Backspace: Volver al menú",
        ]
        
    
    def update(self, delta_time, _event_list):
        self.platform_rotation = self.character_selection_platform.get_rotation()
        if not self.character_selection_platform.is_moving:
            moved = False
            if self.input_manager.was_action_pressed("ui_left") or self.input_manager.was_action_pressed("panel_left"):
                self.selected_index = (self.selected_index - 1) % 3
                self.target_rotation += 120.0
                moved = True
            elif self.input_manager.was_action_pressed("ui_right") or self.input_manager.was_action_pressed("panel_right"):
                self.selected_index = (self.selected_index + 1) % 3
                self.target_rotation -= 120.0
                moved = True
            
            if moved and self.fade_state == "IDLE":
                self.fade_state = "FADE_OUT"
        self._update_background_animation(delta_time)

        if self.platform_rotation - 5 <= self.target_rotation <= self.platform_rotation + 5:
            self.platform_rotation = self.target_rotation
        
        if self.platform_rotation == 360.0:
            self.platform_rotation = 0.0
            self.target_rotation = 0.0
        self.character_selection_platform.set_rotation(self.platform_rotation)
        self.character_selection_platform.set_target_rotation(self.target_rotation)
        self.character_selection_platform.update(delta_time)        
        if self.character_selection_platform.is_moving:
            return
        if (
            self.input_manager.was_action_pressed("interact")
            or self.input_manager.was_action_pressed("panel_select")
            or self.input_manager.was_action_pressed("ui_select")
        ):
            print(f"Iniciando juego con personaje {self.character_names[self.selected_index]}")
            player_config = {"character_index": self.selected_index}
            DataManager.instance().save_game_data(player_config)
            from states.play_state import PlayState
            self.engine.change_state(PlayState(self.engine))
        
        if self.input_manager.was_action_pressed("return"):
            self.engine.pop_state()
            return
    

    def _update_background_animation(self, delta_time):
        if self.fade_state == "FADE_OUT":
            self.fade_alpha -= self.fade_speed * delta_time
            if self.fade_alpha <= 0.0:
                self.fade_alpha = 0.0
                self.display_index = self.selected_index 
                self.fade_state = "FADE_IN"
        
        elif self.fade_state == "FADE_IN":
            self.fade_alpha += self.fade_speed * delta_time
            if self.fade_alpha >= 1.0:
                self.fade_alpha = 1.0
                self.fade_state = "IDLE"

    def draw(self):
        self.engine.setup_3d_perspective()
        glClearColor(*self.background_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.camera.apply_view()
        self.character_selection_platform.draw()
        #Materials.apply_material(Materials.MAT_METAL)
        self._draw_background()
        self.engine.setup_2d_orthographic()
        self._draw_banner()
        draw_instructions(self.display_width, self.display_height, self.instructions_lines)
    

    def _draw_banner(self):
        """
        Dibuja el banner 2D y el nombre del personaje.
        """
        if self.character_selection_platform.is_moving:
            return
        glColor4f(*self.banner_color)
        Objects.draw_pyrect(self.banner_rect)
        nombre_actual = self.character_names[self.selected_index]
        pos_x = self.display_width / 2
        pos_y = self.banner_rect.top + self.banner_rect.height / 2
        draw_text_2d(x=pos_x, y=self.display_height-pos_y, text=nombre_actual, font_name= self.montserrat_font, size=48, center=True,color=(255, 255, 255, 255))
    
    def _draw_background(self):
        width, height, pos_x, pos_y, pos_z = self.background_rect
        glEnable(GL_TEXTURE_2D)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        tex_id = self.background_textures[self.display_index]
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glColor4f(1.0, 1.0, 1.0, self.fade_alpha)
        Objects.draw_crop_plane_3d(width, height, 1152, 896, translate=[pos_x, pos_y, pos_z], rotation=[90, 1, 0, 0])
        glDisable(GL_TEXTURE_2D)