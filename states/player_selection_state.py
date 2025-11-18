"""
Implementa el estado de selección de personaje (3D).
Presenta una escena 3D con cámara fija donde el jugador puede
elegir entre 3 personajes antes de iniciar el juego.
"""

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from .base_state import BaseState
from systems.input_manager import InputManager
from utilities.text_renderer import draw_text_2d, get_font
from game_objects.camera import Camera
from game_objects.character_selection_platform import CharacterSelectionPlatform

class PlayerSelectionState(BaseState):
    
    def __init__(self, engine):
        super().__init__(engine)
        self.engine.setup_3d_perspective()
        self.input_manager = InputManager.instance()
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        self.character_selection_platform = CharacterSelectionPlatform(0.0, 0.0, 0.0)
        self.background_color = (0.1, 0.1, 0.1, 1.0)
        self.camera = Camera(position=[0, 7, 20], look_at=[0, 1, 0])
        
        self.selected_index = 0
        self.platform_rotation = 0.0
        # 0 = Personaje 0, 120 = Personaje 1, 240 = Personaje 2
        self.target_rotation = 0.0 

        self.character_names = ["Santo", "Alien", "Walter"]
        self.banner_color = [0.5, 0.2, 0.2, 0.7]
        self.banner_rect = pygame.Rect(0, 500, 800, 100)
        
    
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
        glClearColor(*self.background_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.camera.apply_view()
        self.character_selection_platform.draw()
        self.engine.setup_2d_orthographic()
        self._draw_banner_and_text()
        self.engine.setup_3d_perspective()
    

    def _draw_banner_and_text(self):
        """
        Dibuja el banner 2D y el nombre del personaje.
        """
        glColor4f(*self.banner_color)
        glBegin(GL_QUADS)
        glVertex2f(self.banner_rect.left, self.banner_rect.top)
        glVertex2f(self.banner_rect.right, self.banner_rect.top)
        glVertex2f(self.banner_rect.right, self.banner_rect.bottom)
        glVertex2f(self.banner_rect.left, self.banner_rect.bottom)
        glEnd()
        
        nombre_actual = self.character_names[self.selected_index]
        font = get_font(48)
        text_width, text_height = font.size(nombre_actual)
        pos_x = (800 - text_width) / 2
        pos_y = self.banner_rect.top + (self.banner_rect.height - text_height) / 2
        
        if not self.character_selection_platform.is_moving:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            draw_text_2d(x=pos_x, y=pos_y, text=nombre_actual, size=48, color=(250, 250, 250, 255))
            glDisable(GL_BLEND)
    