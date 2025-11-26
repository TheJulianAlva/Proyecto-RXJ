"""
Estado de Juego Completado

Muestra una pantalla de felicitaciones cuando el jugador
completa todos los niveles del juego.
"""
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
from states.base_state import BaseState

class GameCompleteState(BaseState):
    """
    Estado de Juego Completado. Muestra mensaje de victoria
    y permite regresar al menú principal.
    """
    def __init__(self, engine):
        super().__init__(engine)
        self.engine = engine
        self.display_width = self.engine.display_width
        self.display_height = self.engine.display_height
        
        # Instancias Singleton
        self.input_manager = InputManager.instance()
        self.audio_manager = AudioManager.instance()
        self.texture_manager = TextureManager.instance()
        data_manager = DataManager.instance()
        
        # Configurar música (reutilizar del menú o usar una especial)
        data_assets_menu = data_manager.get_config().get("states", {}).get("menu_state",{}).get("assets", {})
        victory_music = data_assets_menu.get("music")
        
        # Botón para volver al menú
        btn_width, btn_height = self.display_width*0.3, self.display_height*0.08
        btn_x = (self.display_width - btn_width) / 2
        btn_y = self.display_height * 0.7
        
        button_color = (90, 130, 70, 180)
        button_hover_color = (110, 150, 90, 255)
        button_border_color = (110, 150, 90, 180)
        button_text_color = (255, 255, 255, 255)
        
        self.menu_button = MenuButton(
            pos_x=btn_x, 
            pos_y=btn_y,
            width=btn_width,
            height=btn_height,
            color=button_color,
            hover_color=button_hover_color,
            border_color=button_border_color,
            text="Volver al Menú Principal",
            text_font="montserrat_bold",
            text_size=24,
            text_color=button_text_color
        )
        self.menu_button.set_selected(True)
        
        # Icono de tecla
        self.key_enter = KeyIcon(
            self.menu_button.rect.centerx - 21,
            self.menu_button.rect.top - 60,
            42,
            "ENTER"
        )
        
        # Mensajes de victoria
        self.title = "¡FELICIDADES!"
        self.message_lines = [
            "Has completado todos los niveles",
            "y restaurado la historia de México.",
            "",
            "Gracias por jugar."
        ]
        
        print("GameCompleteState inicializado.")
        self.audio_manager.play_music_loop(victory_music, volume=0.5)

    def update(self, delta_time, _event_list):
        from states.menu_state import MenuState
        
        if self.input_manager.was_action_pressed("ui_select") or \
           self.input_manager.was_action_pressed("quit"):
            self.audio_manager.stop_music()
            while len(self.engine.state_stack) > 1:
                self.engine.pop_state()
            
        self.key_enter.update(delta_time)

    def draw(self):
        """Dibuja la pantalla de victoria."""
        glClearColor(0.05, 0.05, 0.1, 1.0)  # Fondo azul oscuro
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.engine.setup_2d_orthographic()
        
        # Título principal
        title_y = self.display_height * 0.85
        TextUtil.draw_text_2d(
            self.display_width / 2,
            title_y,
            self.title,
            font_name="montserrat_bold",
            size=64,
            color=(255, 215, 0, 255),
            center=True
        )
        
        # Mensajes
        message_start_y = self.display_height * 0.7
        line_height = 40
        for i, line in enumerate(self.message_lines):
            TextUtil.draw_text_2d(
                x=self.display_width / 2,
                y=message_start_y - (i * line_height),
                text=line,
                font_name="montserrat_bold",
                size=28,
                color=(255, 255, 255, 255),
                center=True
            )
        
        # Botón y tecla
        self.menu_button.draw()
        self.key_enter.draw()
