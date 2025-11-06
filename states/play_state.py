import pygame
from states.base_state import BaseState
from game_objects.player import Player
from systems.camera_manager import CameraManager
from systems.input_manager import InputManager

class PlayState(BaseState):
    def __init__(self, engine):
        super().__init__(engine)
        self.engine = engine
        self.player = Player(0, 0, 0)
        self.input_manager = InputManager.instance()
        self.cam_manager = CameraManager.instance()

    def update(self, delta_time, event_list):
        if self.input_manager.was_action_pressed("return"):
            from states.menu_state import MenuState
            self.engine.change_state(MenuState(self.engine))
            return
        self.player.update(delta_time)

    def draw(self):
        _active_cam = self.cam_manager.get_active_camera()
        if _active_cam:
            _active_cam.apply_view()
        else:
            print("¡Advertencia! No hay cámara activa.")
        self.player.draw()