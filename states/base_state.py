class BaseState:
    """Clase abstracta para todos los estados del juego"""
    def __init__(self, engine):
        pass

    def update(self, delta_time, event_list):
        pass # Cada estado actualizará su lógica

    def draw(self):
        pass # Cada estado se dibujará a sí mismo