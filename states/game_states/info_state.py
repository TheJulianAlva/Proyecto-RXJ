from states.base_state import BaseState
from systems.input_manager import InputManager

class InfoState(BaseState):
    def __init__(self, engine):
        super().__init__(engine)
        self.engine = engine
        self.input_manager = InputManager.instance()

    def update(self, delta_time, event_list):
        """Actualiza la lógica del estado."""
        pass

    def draw(self):
        """Dibuja el estado en la pantalla."""
        pass