class BaseState:
    """Clase abstracta para todos los estados del juego"""
    def __init__(self):
        pass

    def handle_input(self, event):
        pass # Cada estado manejará los eventos de forma diferente

    def update(self, delta_time):
        pass # Cada estado actualizará su lógica

    def draw(self):
        pass # Cada estado se dibujará a sí mismo