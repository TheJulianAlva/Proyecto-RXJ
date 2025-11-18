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
from utilities.text_renderer import draw_text_2d
from utilities.basic_objects import draw_pyrect
from game_objects.camera import Camera
from game_objects.character_selection_platform import CharacterSelectionPlatform

class PlayerSelectionState(BaseState):
    
    def __init__(self, engine):
        super().__init__(engine)
        self.input_manager = InputManager.instance()
        data_manager = DataManager.instance()
        config = data_manager.get_config()

        display_config = config.get("display", {})
        self.display_width = display_config.get("width", 800)
        self.display_height = display_config.get("height", 600)
        
        data_selection = data_manager.get_text_dict().get("selection_state", {})
        self.character_names = data_selection.get("banner_names")
        
        self.engine.setup_3d_perspective()
        glEnable(GL_LIGHTING)
        self.character_selection_platform = CharacterSelectionPlatform(0.0, 0.0, 0.0)
        self.background_color = (0.1, 0.1, 0.1, 1.0)
        self.camera = Camera(position=[0, 7, 20], look_at=[0, 1, 0])
        
        self.selected_index = 0
        self.platform_rotation = 0.0
        # 0 = Personaje 0, 120 = Personaje 1, 240 = Personaje 2
        self.target_rotation = 0.0 

        self.banner_color = [0.5, 0.2, 0.2, 0.7]
        self.banner_rect = pygame.Rect(0, 500, self.display_width, 100)
        self.montserrat_font = "montserrat_bold"
        
    
    def update(self, delta_time, _event_list):
        self.platform_rotation = self.character_selection_platform.get_rotation()
        if not self.character_selection_platform.is_moving:
            if self.input_manager.was_action_pressed("ui_left"):
                self.selected_index = (self.selected_index - 1) % 3
                self.target_rotation += 120.0
            elif self.input_manager.was_action_pressed("ui_right"):
                self.selected_index = (self.selected_index + 1) % 3
                self.target_rotation -= 120.0
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
        if self.input_manager.was_action_pressed("interact"):
            print(f"Iniciando juego con personaje {self.character_names[self.selected_index]}")
            from states.play_state import PlayState
            self.engine.push_state(PlayState(self.engine))
        
        if self.input_manager.was_action_pressed("return"):
            self.engine.pop_state()
            return
    


    def draw(self):
        self.engine.setup_3d_perspective()
        glClearColor(*self.background_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.camera.apply_view()
        self.character_selection_platform.draw()
        self.engine.setup_2d_orthographic()
        self._draw_banner()
    

    def _draw_banner(self):
        """
        Dibuja el banner 2D y el nombre del personaje.
        """
        glColor4f(*self.banner_color)
        draw_pyrect(self.banner_rect)
        nombre_actual = self.character_names[self.selected_index]
        pos_x = self.display_width / 2
        pos_y = self.banner_rect.top + self.banner_rect.height / 2
        if not self.character_selection_platform.is_moving:
            draw_text_2d(x=pos_x, y=pos_y, text=nombre_actual, font_name= self.montserrat_font, size=48, center=True,color=(255, 255, 255, 255))
    