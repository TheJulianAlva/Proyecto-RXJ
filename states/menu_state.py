import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from systems.data_manager import DataManager
from systems.input_manager import InputManager
from systems.texture_manager import TextureManager
from systems.audio_manager import AudioManager
import utilities.text_renderer as TextUtil
import utilities.basic_objects as Objects
from game_objects.ui_elements.key_icon import KeyIcon
from game_objects.ui_elements.menu_button import MenuButton
from utilities.instructions_overlay import draw_instructions
from states.base_state import BaseState

class MenuState(BaseState):
    """
    Estado del Menú Principal. Dibuja UI en 2D y maneja
    la navegación del menú (Iniciar Juego, Salir).
    """
    def __init__(self, engine):
        super().__init__(engine)
        self.engine = engine
        self.display_width = self.engine.display_width
        self.display_height = self.engine.display_height
        # region Instancias Singleton
        self.input_manager = InputManager.instance()
        self.audio_manager = AudioManager.instance()
        data_manager = DataManager.instance()
        self.texture_manager = TextureManager.instance()
        # endregion
        
        # region Cargar Data
        data_text_menu = data_manager.get_text_dict().get("menu_state", {})
        text_start_button = data_text_menu.get("start_button", "Jugar")
        text_exit_button = data_text_menu.get("exit_button", "Salir")
        
        data_assets_menu = data_manager.get_config().get("states", {}).get("menu_state",{}).get("assets", {})
        self.textures = data_assets_menu.get("textures", {}).items()
        for texture_key, texture_path in self.textures:
            self.texture_manager.load_texture(texture_key, texture_path)

        for sound_key, sound_path in data_assets_menu.get("sounds", {}).items():
            self.audio_manager.load_sound(sound_key, sound_path)
            
        menu_music = data_assets_menu.get("music")
        self.background_texture = self.texture_manager.get_texture("texture_background")
        # endregion

        # region Instancias UI
        margin_display = self.display_width*0.08
        padding = self.display_height*0.08
        btn_width, btn_height = self.display_width*0.25, self.display_height*0.08
        btn_x = self.display_width - btn_width - margin_display
        
        btn_y_exit = self.display_height - btn_height - margin_display
        btn_y_start = btn_y_exit - btn_height - padding

        button_color = (90, 130, 70, 130) # Verde
        button_hover_color = (110, 150, 90, 255) # Verde claro
        button_border_color = (110, 150, 90, 130) # Verde claro
        button_text_color = (255, 255, 255, 255) # Blanco
        
        button_font = "montserrat_semibold"

        self.start_button = MenuButton(
            pos_x=btn_x, 
            pos_y=btn_y_start,
            width=btn_width,
            height=btn_height,
            color=button_color,
            hover_color=button_hover_color,
            border_color=button_border_color,
            text=text_start_button,
            text_font=button_font,
            text_size=24,
            text_color=button_text_color
            )
        
        self.exit_button = MenuButton(
            pos_x=btn_x, 
            pos_y=btn_y_exit,
            width=btn_width,
            height=btn_height,
            color=button_color,
            hover_color=button_hover_color,
            border_color=button_border_color,
            text=text_exit_button,
            text_font=button_font,
            text_size=24,
            text_color=button_text_color
            )
        # endregion
        self.selected_button = self.start_button
        self.selected_button.set_selected(True)
        # region Icons
        self.key_up = KeyIcon(self.start_button.rect.left-63, self.start_button.rect.centery-21, 42, "ARROWUP")
        self.key_down = KeyIcon(self.exit_button.rect.left-63, self.exit_button.rect.centery-21, 42, "ARROWDOWN")
        self.key_enter = KeyIcon(self.selected_button.rect.right-21, self.selected_button.rect.centery-42, 42, "ENTER")
        # endregion
        self.background_image = pygame.Rect(0, 0, self.display_width, self.display_height)
        print("MenuState inicializado.")
        self.audio_manager.play_music_loop(menu_music, volume=0.4)

    def update(self, delta_time, _event_list):
        from states.player_selection_state import PlayerSelectionState
        
        if self.input_manager.was_action_pressed("quit"):
            self.engine.pop_state()
        elif self.input_manager.was_action_pressed("ui_up"):
            self._toogle_selected_button()
        elif self.input_manager.was_action_pressed("ui_down"):
            self._toogle_selected_button()
        elif self.input_manager.was_action_pressed("ui_select"):
            self.audio_manager.play_sound("confirm_button_selected")
            self.audio_manager.stop_music()
            if self.selected_button == self.start_button:
                self.engine.push_state(PlayerSelectionState(self.engine))
            else:
                self.engine.pop_state()
        # region UI
        self.key_up.update(delta_time)
        self.key_down.update(delta_time)
        self.key_enter.update(delta_time)
        # endregion

    def _toogle_selected_button(self):
        self.audio_manager.play_sound("toogle_button_selected")
        if self.start_button.is_selected:
            self.start_button.set_selected(False)
            self.exit_button.set_selected(True)
            self.selected_button = self.exit_button
        elif self.exit_button.is_selected:
            self.exit_button.set_selected(False)
            self.start_button.set_selected(True)
            self.selected_button = self.start_button
        else:
            self.exit_button.set_selected(False)
            self.start_button.set_selected(True)
            self.selected_button = self.start_button
        self.key_enter.set_position(self.selected_button.rect.right-21, self.selected_button.rect.centery-42)

    def draw(self):
        """Dibuja la UI en 2D."""
        glClearColor(0, 0, 0, 255)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.engine.setup_2d_orthographic()
        glColor3f(1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.background_texture)
        Objects.draw_crop_pyrect(self.background_image, 1344, 768)
        glDisable(GL_TEXTURE_2D)

        # region UI
        self.start_button.draw()
        self.exit_button.draw()
        self.key_up.draw()
        self.key_down.draw()
        self.key_enter.draw()
        # endregion

    def _unload_textures(self):
        for texture_key in self.textures:
            self.texture_manager.unload_texture(texture_key)