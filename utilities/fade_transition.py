"""
Sistema de Transición con Fade Out/In

Maneja animaciones de fade out/in para transiciones suaves entre niveles.
Permite ejecutar callbacks en momentos específicos de la transición.
"""
from OpenGL.GL import *

class FadeTransition:
    IDLE = 0
    FADING_OUT = 1
    FADING_IN = 2
    COMPLETE = 3
    
    def __init__(self, display_width, display_height, fade_speed=1.5):
        """
        Args:
            display_width: Ancho de la pantalla
            display_height: Alto de la pantalla
            fade_speed: Velocidad del fade (mayor = más rápido)
        """
        self.display_width = display_width
        self.display_height = display_height
        self.fade_speed = fade_speed
        
        self.state = self.IDLE
        self.alpha = 0.0
        self.on_fade_out_complete = None
        self.on_transition_complete = None
        
    def start_transition(self, on_fade_out_complete=None, on_transition_complete=None):
        """
        Inicia una transición completa (fade out -> acción -> fade in)
        
        param: on_fade_out_complete: Función a ejecutar cuando el fade out termine
        param: on_transition_complete: Función a ejecutar cuando toda la transición termine
        """
        self.state = self.FADING_OUT
        self.alpha = 0.0
        self.on_fade_out_complete = on_fade_out_complete
        self.on_transition_complete = on_transition_complete
        
    def update(self, delta_time):
        """Actualiza la animación de fade"""
        if self.state == self.FADING_OUT:
            self.alpha += self.fade_speed * delta_time
            if self.alpha >= 1.0:
                self.alpha = 1.0
                self.state = self.FADING_IN
                if self.on_fade_out_complete:
                    self.on_fade_out_complete()
                    
        elif self.state == self.FADING_IN:
            self.alpha -= self.fade_speed * delta_time
            if self.alpha <= 0.0:
                self.alpha = 0.0
                self.state = self.COMPLETE
                if self.on_transition_complete:
                    self.on_transition_complete()
                    
        elif self.state == self.COMPLETE:
            self.state = self.IDLE
            
    def draw(self):
        """Renderiza el overlay de fade"""
        if self.state == self.IDLE or self.alpha <= 0.0:
            return
            
        glPushAttrib(GL_ENABLE_BIT | GL_CURRENT_BIT)
        
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        
        # Dibujar rectángulo negro con alpha
        glColor4f(0.0, 0.0, 0.0, self.alpha)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(self.display_width, 0)
        glVertex2f(self.display_width, self.display_height)
        glVertex2f(0, self.display_height)
        glEnd()
        
        glPopAttrib()
        
    def is_active(self):
        """Retorna True si hay una transición en progreso"""
        return self.state != self.IDLE
