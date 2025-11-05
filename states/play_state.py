import pygame
from .base_state import BaseState
from game_objects.player import Player
from systems.camera_manager import CameraManager

class PlayState(BaseState):
    def __init__(self):
        super().__init__()
        self.player = Player(0, 0, 0)

    def update(self, delta_time):
        self.player.update(delta_time)

    def draw(self):
        cam_manager = CameraManager.instance()
        active_cam = cam_manager.get_active_camera()
        if active_cam:
            active_cam.apply_view()
        else:
            print("¡Advertencia! No hay cámara activa.")
        self.player.draw()