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
        
        self.clear_color = (0.1, 0.1, 0.2, 1.0)
        self.button_color = (0.0, 0.5, 0.0)
        self.button_exit_color = (0.5, 0.0, 0.0)
        
        print("MenuState inicializado.")
        print("  -> Haz clic en el botón VERDE para Jugar.")
        print("  -> Haz clic en el botón ROJO para Salir.")

    def update(self, _delta_time, event_list):
        if self.input_manager.was_action_pressed("quit"):
            self.engine.quit_game()
            
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clic izquierdo
                    if self.start_button.collidepoint(event.pos):
                        from states.play_state import PlayState
                        self.engine.change_state(PlayState(self.engine))
                        
                    elif self.exit_button.collidepoint(event.pos):
                        self.engine.quit_game()

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
        
        # 4. Volver a la configuración 3D (buena práctica)
        glEnable(GL_DEPTH_TEST)
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def _draw_rect(self, rect):
        """Función helper para dibujar un pygame.Rect con GL_QUADS."""
        glBegin(GL_QUADS)
        glVertex2f(rect.left, rect.top)
        glVertex2f(rect.right, rect.top)
        glVertex2f(rect.right, rect.bottom)
        glVertex2f(rect.left, rect.bottom)
        glEnd()