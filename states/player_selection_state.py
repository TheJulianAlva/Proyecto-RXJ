"""
Implementa el estado de selección de personaje (3D).
Presenta una escena 3D con cámara fija donde el jugador puede
elegir entre 3 personajes antes de iniciar el juego.
"""

import os
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from .base_state import BaseState
from systems.data_manager import DataManager
from systems.input_manager import InputManager
from systems.texture_manager import TextureManager
from systems.audio_manager import AudioManager
from utilities.text_renderer import draw_text_2d
from utilities import basic_objects as Objects
from game_objects.camera import Camera
from game_objects.ui_elements.menu_button import MenuButton
from game_objects.ui_elements.key_icon import KeyIcon
from game_objects.selection_menu.character_selection_platform import CharacterSelectionPlatform
from utilities.instructions_overlay import draw_instructions

class PlayerSelectionState(BaseState):
    
    def __init__(self, engine):
        super().__init__(engine)
        self.input_manager = InputManager.instance()
        data_manager = DataManager.instance()
        self.texture_manager = TextureManager.instance()
        self.audio_manager = AudioManager.instance()
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

        self.banner_color = [0.2, 0.1, 0.05, 0.9]
        banner_width = self.display_width * 0.4
        self.banner_rect = pygame.Rect(
            (self.display_width - banner_width) * 0.5,
            self.display_height * 0.7,
            banner_width,
            self.display_height * 0.18)
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
            "Flechas (<- / ->): Cambiar personaje",
            "Enter: Jugar",
            "Esc: Volver al menú",
        ]
        
        
        self.play_button = MenuButton(
            self.display_width * 0.8,
            self.display_height * 0.85,
            self.display_width * 0.15,
            self.display_height * 0.1,
            "Jugar",
            text_font="montserrat_bold",
            text_size=36,
            border_color=(0.1, 0.1, 0.1, 1.0)
        )
        
        self.back_button = MenuButton(
            self.display_width * 0.05,
            self.display_height * 0.85,
            self.display_width * 0.15,
            self.display_height * 0.1,
            "Regresar",
            text_font="montserrat_bold",
            text_size=36,
            border_color=(0.1, 0.1, 0.1, 1.0)
        )
        # region Icons
        self.key_play = KeyIcon(self.play_button.rect.left-45, self.play_button.rect.top-45, 63, "ENTER")
        self.key_return = KeyIcon(self.back_button.rect.right-45, self.back_button.rect.top-45, 42, "BACKSPACE")
        self.key_left = KeyIcon(self.display_width * 0.1, self.display_height * 0.5, 105, "ARROWLEFT")
        self.key_right = KeyIcon(self.display_width * 0.9, self.display_height * 0.5, 105, "ARROWRIGHT")
        # endregion
        self._current_audio_key = None
        self._load_character_audio()
        self._play_character_audio(self.selected_index)
    
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
                self._play_character_audio(self.selected_index)
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
            self.input_manager.was_action_pressed("ui_select")
            or self.input_manager.was_action_pressed("panel_select")
        ):
            print(f"Iniciando juego con personaje {self.character_names[self.selected_index]}")
            player_config = {"character_index": self.selected_index}
            DataManager.instance().save_game_data(player_config)
            self._stop_current_audio()
            from states.play_state import PlayState
            self.engine.change_state(PlayState(self.engine))
        
        if self.input_manager.was_action_pressed("return"):
            self._stop_current_audio()
            self.engine.pop_state()
            return
        self.key_play.update(delta_time)
        self.key_return.update(delta_time)
        self.key_left.update(delta_time)
        self.key_right.update(delta_time) 

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
        self._draw_background()
        self.engine.setup_2d_orthographic()
        self._draw_banner()
        self._draw_title()
        self.play_button.draw()
        self.back_button.draw()
        self.key_play.draw()
        self.key_return.draw()
        self.key_left.draw()
        self.key_right.draw()
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
        
    def _draw_title(self):
        pos_x = self.display_width / 2
        pos_y = self.display_height * 0.2
        draw_text_2d(x=pos_x, y=self.display_height-pos_y, text="Selecciona Un Personaje", font_name= self.montserrat_font, size=56, center=True,color=(255, 255, 255, 255))

    def _load_character_audio(self):
        base_path = os.path.join("assets", "audio", "select_character")
        audio_map = {
            0: ("santo_theme", "el-santo.mp3"),
            1: ("marciana_theme", "marciana.mp3"),
            2: ("walter_theme", "breaking-bad-intro.mp3"),
        }
        self.character_audio_keys = {}
        for index, (audio_key, filename) in audio_map.items():
            full_path = os.path.join(base_path, filename)
            self.character_audio_keys[index] = audio_key
            self.audio_manager.load_sound(audio_key, full_path)

    def _stop_current_audio(self):
        if self._current_audio_key:
            self.audio_manager.stop_sound(self._current_audio_key)
            self._current_audio_key = None

    def _play_character_audio(self, index):
        audio_key = self.character_audio_keys.get(index)
        if not audio_key:
            return

        if self._current_audio_key and self._current_audio_key != audio_key:
            self.audio_manager.stop_sound(self._current_audio_key)

        channel = self.audio_manager.play_sound(audio_key, loops=0, volume=0.9)
        if channel:
            self._current_audio_key = audio_key