"""
Define la clase 'BaseState', la plantilla abstracta (interfaz) 
de la que deben heredar todos los estados del juego (ej. MenuState, PlayState).
Asegura que todos los estados respondan a update() y draw().
"""

class BaseState:
    """Clase abstracta para todos los estados del juego"""
    def __init__(self, engine):
        self.engine = engine

    def update(self, delta_time, event_list):
        """Actualiza la lógica del estado."""
        pass

    def draw(self):
        """Dibuja el estado en la pantalla."""
        pass