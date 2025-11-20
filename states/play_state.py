"""
Implementa el estado principal del juego (3D). 
Gestiona la lógica del jugador (update, draw) y la 
cámara 3D activa (apply_view) en cada fotograma.
"""
from states.base_state import BaseState
from systems.data_manager import DataManager
from systems.camera_manager import CameraManager
from systems.input_manager import InputManager
from game_objects.character_models.santo import SantoSkin
from game_objects.character_models.alien import AlienSkin
from game_objects.character_models.walter import WalterSkin
from game_objects.player import Player

class PlayState(BaseState):
    def __init__(self, engine):
        super().__init__(engine)
        self.engine = engine
        self.engine.setup_3d_perspective()
        data_manager = DataManager.instance()
        player_config = data_manager.load_game_data()
        skins = [SantoSkin, AlienSkin, WalterSkin]
        selected_index = player_config.get("character_index", 0)
        selected_skin = skins[selected_index]
        self.player = Player(0, 0, 0, selected_skin)
        self.input_manager = InputManager.instance()
        self.cam_manager = CameraManager.instance()

    def update(self, delta_time, _event_list):
        if self.input_manager.was_action_pressed("return"):
            self.engine.pop_state()
            return
        self.player.update(delta_time)

    def draw(self):
        _active_cam = self.cam_manager.get_active_camera()
        if _active_cam:
            _active_cam.apply_view()
        else:
            print("¡Advertencia! No hay cámara activa.")
        self.player.draw()
        