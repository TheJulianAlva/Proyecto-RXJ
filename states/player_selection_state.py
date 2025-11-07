"""
Implementa el estado de selección de personaje (3D).
Presenta una escena 3D con cámara fija donde el jugador puede
elegir entre 3 personajes antes de iniciar el juego.
"""

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from assets import basic_objects as ob
from assets import materials as mats
from .base_state import BaseState
from systems.input_manager import InputManager
from game_objects.camera import Camera # Usaremos una cámara fija

class PlayerSelectionState(BaseState):
    
    def __init__(self, engine):
        super().__init__(engine)
        self.engine.setup_perspective()
        self.input_manager = InputManager.instance()
        
        self.camera = Camera(position=[0, 3, 15], look_at=[0, 0, 0])
        
        self.selected_index = 0
        self.platform_rotation = 0.0
        # 0 = Personaje 0, 120 = Personaje 1, 240 = Personaje 2
        self.target_rotation = 0.0 
        self.quad = gluNewQuadric()
        gluQuadricNormals(self.quad, GLU_SMOOTH)
        self.background_color = (0.1, 0.1, 0.1, 1.0)
        
    def update(self, _delta_time, _event_list):
        
        if self.input_manager.was_action_pressed("rotate_right"): # Tecla 'D'
            self.selected_index = (self.selected_index + 1) % 3
            self.target_rotation += 120.0
            print(f"Personaje seleccionado: {self.selected_index}")

        if self.input_manager.was_action_pressed("rotate_left"): # Tecla 'A'
            self.selected_index = (self.selected_index - 1) % 3
            self.target_rotation -= 120.0
            print(f"Personaje seleccionado: {self.selected_index}")
        
        if self.input_manager.was_action_pressed("interact"):
            print(f"Iniciando juego con personaje {self.selected_index}")
            from states.play_state import PlayState
            self.engine.push_state(PlayState(self.engine))
        
        if self.input_manager.was_action_pressed("return"):
            self.engine.pop_state()
            return
            
        # --- Lógica de Animación (placeholder) ---
        # Aquí animaríamos suavemente self.platform_rotation hacia self.target_rotation
        # Por ahora, es un salto directo:
        self.platform_rotation = self.target_rotation


    def draw(self):
        glClearColor(*self.background_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.camera.apply_view()
        self._configure_light()
        
        glPushMatrix()
        glRotatef(self.platform_rotation, 0, 1, 0)
        mats.apply_material(mats.MAT_GREEN)
        ob.draw_cylinder(quad=self.quad, scale=[10.0, 1.0, 10.0])
        mats.apply_material(mats.MAT_PLAYER)
        ob.draw_cube(translate=[0.0, 1.0, 8.0])
        
        glPopMatrix()

    def _configure_light():
        """Configura la luz 0 según el modo actual (light_mode)."""
        
        # Propiedades básicas de la luz (blanca)
        light_ambient = [0.2, 0.2, 0.2, 1.0]
        light_diffuse = [0.9, 0.9, 0.9, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]
        
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
        
        # Posición (w=1.0 para puntual, w=0.0 para direccional)
        light_pos_point = [0.0, 5.0, 8.0, 1.0]  # Arriba y al frente
        light_pos_dir = [0.8, 0.5, 1.0, 0.0]   # Desde arriba a la derecha
        
        # Configuración del Foco
        spot_dir = [0.0, -1.0, 0.0] # Apuntando hacia abajo y al frente
        spot_cutoff = 30.0          # Ángulo de 30 grados
        spot_exponent = 15.0        # Enfoque del haz de luz
        
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos_point) # Un foco debe ser puntual
        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, spot_cutoff)
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, spot_dir)
        glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, spot_exponent)