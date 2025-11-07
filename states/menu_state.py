"""
Implementa el estado del menú principal (UI). 
Dibuja en 2D (usando gluOrtho2D) y maneja la navegación
para iniciar el juego (push PlayState) o salir (pop).
"""

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from states.base_state import BaseState
from systems.input_manager import InputManager

class MenuState(BaseState):
    """
    Estado del Menú Principal. Dibuja UI en 2D y maneja
    la navegación del menú (Iniciar Juego, Salir).
    """
    
    def __init__(self, engine):
        super().__init__(engine)
        self.engine = engine
        self.input_manager = InputManager.instance()
        display_width, display_height = 800, 600
        btn_width, btn_height = 200, 50
        btn_x = (display_width - btn_width) / 2
        
        self.start_button = pygame.Rect(btn_x, 250, btn_width, btn_height)
        self.exit_button = pygame.Rect(btn_x, 320, btn_width, btn_height)
        self.selected_button = self.start_button
        self.clear_color = (0.3, 0.3, 0.4, 1.0)
        self.button_color = (0.0, 0.5, 0.0)
        self.button_exit_color = (0.5, 0.0, 0.0)
        
        print("MenuState inicializado.")
        print("  -> Haz clic en el botón VERDE para Jugar.")
        print("  -> Haz clic en el botón ROJO para Salir.")

    def update(self, _delta_time, event_list):
        from states.play_state import PlayState
        if self.input_manager.was_action_pressed("quit"):
            self.engine.pop_state()
        elif self.input_manager.was_action_pressed("ui_up"):
            self._toogle_button_selected()
        elif self.input_manager.was_action_pressed("ui_down"):
            self._toogle_button_selected()
        elif self.input_manager.was_action_pressed("ui_select"):
            if self.selected_button == self.start_button:
                self.engine.push_state(PlayState(self.engine))
            else:
                self.engine.pop_state()

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clic izquierdo
                    if self.start_button.collidepoint(event.pos):
                        self.engine.push_state(PlayState(self.engine))
                        
                    elif self.exit_button.collidepoint(event.pos):
                        self.engine.pop_state()

    def _toogle_button_selected(self):
        if self.selected_button == self.start_button:
            self.selected_button = self.exit_button
        else:
            self.selected_button = self.start_button

    def draw(self):
        """Dibuja la UI en 2D."""
        glClearColor(*self.clear_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        # Coordenadas de pantalla: (0,0) es arriba-izquierda
        gluOrtho2D(0, 800, 600, 0) 
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glDisable(GL_DEPTH_TEST) # No necesitamos profundidad para 2D
        
        # Botón Iniciar
        glColor3f(*self.button_color)
        self._draw_rect(self.start_button)
        
        # Botón Salir
        glColor3f(*self.button_exit_color)
        self._draw_rect(self.exit_button)
        
        glColor3f(1.0, 1.0, 1.0)
        if self.selected_button == self.start_button:
            self._draw_rect_border(self.start_button)
        else:
            self._draw_rect_border(self.exit_button)
            

        # 4. Volver a la configuración 3D (buena práctica)
        glEnable(GL_DEPTH_TEST)
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def _draw_rect(self, rect):
        """Función para dibujar un pygame.Rect con GL_QUADS."""
        glBegin(GL_QUADS)
        glVertex2f(rect.left, rect.top)
        glVertex2f(rect.right, rect.top)
        glVertex2f(rect.right, rect.bottom)
        glVertex2f(rect.left, rect.bottom)
        glEnd()

    def _draw_rect_border(self, rect):
        """Función para dibujar un pygame.Rect con GL_LINES."""
        glBegin(GL_LINES)
        glVertex2f(rect.left, rect.top)
        glVertex2f(rect.right, rect.top)
        glVertex2f(rect.right, rect.top)
        glVertex2f(rect.right, rect.bottom)
        glVertex2f(rect.right, rect.bottom)
        glVertex2f(rect.left, rect.bottom)
        glVertex2f(rect.left, rect.bottom)
        glVertex2f(rect.left, rect.top)
        glEnd()