from states.play_state import PlayState

class GameEngine:
    def __init__(self):
        self.current_state = PlayState() # Empezar en el estado de juego
        # (Más adelante aquí tendrás MenuState, PauseState, etc.)

    def change_state(self, new_state):
        """Cambia de estado, por ejemplo: self.change_state(PlayState(self))"""
        self.current_state = new_state

    def update(self, delta_time):
        self.current_state.update(delta_time)

    def draw(self):
        self.current_state.draw()