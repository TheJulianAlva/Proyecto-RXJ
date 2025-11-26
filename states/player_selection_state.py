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
        self.engine = engine
        self.display_width = self.engine.display_width
        self.display_height = self.engine.display_height
        
        # region Instancias Singleton
        self.input_manager = InputManager.instance()
        data_manager = DataManager.instance()
        self.texture_manager = TextureManager.instance()
        self.audio_manager = AudioManager.instance()
        # endregion

        # region Cargar Data
        config = data_manager.get_config()
        data_assets_player_selection = data_manager.get_config().get("states", {}).get("player_selection_state",{}).get("assets", {})
        self.textures = data_assets_player_selection.get("textures", {}).items()
        for texture_key, texture_path in self.textures:
            self.texture_manager.load_texture(texture_key, texture_path)

        self.background_textures = [
            self.texture_manager.get_texture("bg_selection_0"),
            self.texture_manager.get_texture("bg_selection_1"),
            self.texture_manager.get_texture("bg_selection_2")
            ]
        
        self.sounds = data_assets_player_selection.get("sounds", {}).items()
        for sound_key, sound_path in self.sounds:
            self.audio_manager.load_sound(sound_key, sound_path)
        
        self.background_sounds = ["audio_selection_0", "audio_selection_1", "audio_selection_2"]

        data_text_selection = data_manager.get_text_dict().get("selection_state", {})
        self.character_names = data_text_selection.get("banner_names", ["El Maskara", "Marciana", "Walter"])
        self.text_title = data_text_selection.get("title", "Selecciona")
        self.text_play_button = data_text_selection.get("confirm_button", "Jugar")
        self.text_exit_button = data_text_selection.get("exit_button", "Regresar")
        # endregion

        self.character_selection_platform = CharacterSelectionPlatform(0.0, 0.0, 0.0)
        self.camera = Camera(position=[0, 5, 19], look_at=[0, 4, 0])
        
        self.selected_index = 0
        self.platform_rotation = 0.0
        self.target_rotation = 0.0 

        self.title_font = "montserrat_semibold"
        self.button_font = "montserrat_bold"
        self.banner_color = [0.1, 0.1, 0.05, 0.95]
        banner_width = self.display_width * 0.35
        self.banner_rect = pygame.Rect(
            (self.display_width - banner_width) * 0.5,
            self.display_height * 0.7,
            banner_width,
            self.display_height * 0.18)

        self.play_button = MenuButton(
            self.display_width * 0.8,
            self.display_height * 0.85,
            self.display_width * 0.15,
            self.display_height * 0.1,
            self.text_play_button,
            text_font=self.button_font,
            text_size=24,
            border_color=(0.1, 0.1, 0.1, 1.0)
        )
        
        self.back_button = MenuButton(
            self.display_width * 0.05,
            self.display_height * 0.85,
            self.display_width * 0.15,
            self.display_height * 0.1,
            self.text_exit_button,
            text_font=self.button_font,
            text_size=24,
            border_color=(0.1, 0.1, 0.1, 1.0)
        )
        
        # region Variables animación
        self.fade_alpha = 1.0
        self.fade_state = "IDLE"       # Estados: IDLE, FADE_OUT, FADE_IN
        self.fade_speed = 3.0
        self.display_index = 0
        # endregion
        self.background_rect = (38.4, 25.6, 0.0, 7.0, -5.0)
        
        
        # region Icons
        self.key_play = KeyIcon(self.play_button.rect.left-45, self.play_button.rect.top-45, 63, "ENTER")
        self.key_return = KeyIcon(self.back_button.rect.right-45, self.back_button.rect.top-45, 42, "BACKSPACE")
        self.key_left = KeyIcon(self.display_width * 0.1, self.display_height * 0.5, 105, "ARROWLEFT")
        self.key_right = KeyIcon(self.display_width * 0.9, self.display_height * 0.5, 105, "ARROWRIGHT")
        # endregion
        
        self.audio_manager.play_sound(self.background_sounds[self.selected_index], volume=0.5)
    
    def update(self, delta_time, _event_list):
        # region Movimiento
        past_index = self.selected_index
        self.platform_rotation = self.character_selection_platform.get_rotation()
        if not self.character_selection_platform.is_moving:
            moved = False
            if self.input_manager.was_action_pressed("ui_left") or self.input_manager.was_action_pressed("panel_left"):
                self.audio_manager.play_sound("toggle_button_selected", volume=1.0)
                self.selected_index = (self.selected_index - 1) % 3
                self.target_rotation += 120.0
                moved = True
            elif self.input_manager.was_action_pressed("ui_right") or self.input_manager.was_action_pressed("panel_right"):
                self.audio_manager.play_sound("toggle_button_selected", volume=1.0)
                self.selected_index = (self.selected_index + 1) % 3
                self.target_rotation -= 120.0
                moved = True
            
            if moved:
                self.fade_state = "FADE_OUT"
                self._update_background_sound(past_index, self.selected_index)
        self._update_background_animation(delta_time)

        if self.platform_rotation - 5 <= self.target_rotation <= self.platform_rotation + 5:
            self.platform_rotation = self.target_rotation
        
        if self.platform_rotation == 360.0:
            self.platform_rotation = 0.0
            self.target_rotation = 0.0
        self.character_selection_platform.set_rotation(self.platform_rotation)
        self.character_selection_platform.set_target_rotation(self.target_rotation)
        self.character_selection_platform.update(delta_time)
        # endregion
        if self.character_selection_platform.is_moving:
            return
        if self.input_manager.was_action_pressed("ui_select"):
            self._stop_current_audio()
            self.audio_manager.play_sound("confirm_button_selected", volume=1.0)
            print(f"Iniciando juego con personaje {self.character_names[self.selected_index]}")
            player_config = {"character_index": self.selected_index}
            DataManager.instance().save_game_data(player_config)
            from states.play_state import PlayState
            self.engine.change_state(PlayState(self.engine))
        if self.input_manager.was_action_pressed("return"):
            self._stop_current_audio()
            self.audio_manager.play_sound("confirm_button_selected", volume=1.0)
            self.engine.pop_state()
            return
        # region Icons
        self.key_play.update(delta_time)
        self.key_return.update(delta_time)
        self.key_left.update(delta_time)
        self.key_right.update(delta_time) 
        # endregion
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

    def _update_background_sound(self, past_index, actual_index):
        self.audio_manager.stop_sound(self.background_sounds[past_index])
        self.audio_manager.play_sound(self.background_sounds[actual_index], volume=0.5)

    def draw(self):
        self.engine.setup_3d_perspective()
        glClearColor(0, 0, 0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.camera.apply_view()
        self.character_selection_platform.draw()
        self._draw_background()
        self.engine.setup_2d_orthographic()
        self._draw_banner()
        self._draw_title()
        self._draw_icons()
    
    def _draw_banner(self):
        """
        Dibuja el banner 2D y el nombre del personaje.
        """
        if self.character_selection_platform.is_moving:
            return
        glColor4fv(self.banner_color)
        Objects.draw_pyrect(self.banner_rect)
        nombre_actual = self.character_names[self.selected_index]
        pos_x = self.display_width / 2
        pos_y = self.banner_rect.top + self.banner_rect.height / 2
        draw_text_2d(x=pos_x, y=self.display_height-pos_y, text=nombre_actual, size=48, font_name=self.title_font, center=True,color=(255, 255, 255, 255))
    
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
        pos_y = self.display_height * 0.1
        draw_text_2d(x=pos_x, y=self.display_height-pos_y, text="Selecciona Un Personaje", size=56, font_name=self.title_font,center=True,color=(255, 255, 255, 255))

    def _draw_icons(self):
        self.play_button.draw()
        self.back_button.draw()
        self.key_play.draw()
        self.key_return.draw()
        self.key_left.draw()
        self.key_right.draw()
    
    def _stop_current_audio(self):
        self.audio_manager.stop_sound(self.background_sounds[self.selected_index])