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
        self.camera = Camera(position=[0, 3, 12], look_at=[0, 0, 0])
        
        self.selected_index = 0
        self.platform_rotation = 0.0
        # 0 = Personaje 0, 120 = Personaje 1, 240 = Personaje 2
        self.target_rotation = 0.0 
        
    
    def update(self, delta_time, _event_list):

        if self.input_manager.was_action_pressed("interact"):
            print(f"Iniciando juego con personaje {self.selected_index}")
            from states.play_state import PlayState
            self.engine.push_state(PlayState(self.engine))
        
        if self.input_manager.was_action_pressed("return"):
            self.engine.pop_state()
            return
    
        self.character_selection_platform.update(delta_time)        


    def draw(self):
        glClearColor(*self.background_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.camera.apply_view()
        self.character_selection_platform.draw()
    