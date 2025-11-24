"""
Implementa el estado principal del juego (3D). 
Gestiona la lógica del jugador (update, draw) y la 
cámara 3D activa (apply_view) en cada fotograma.
"""
from states.base_state import BaseState
from systems.data_manager import DataManager
from systems.camera_manager import CameraManager
from systems.trigger_manager import TriggerManager
from systems.input_manager import InputManager
from game_objects.level import Level
from game_objects.character_models.santo import SantoSkin
from game_objects.character_models.alien import AlienSkin
from game_objects.character_models.walter import WalterSkin
from game_objects.player import Player
from states.pause_state import PauseState
from utilities.instructions_overlay import draw_instructions

class PlayState(BaseState):
    def __init__(self, engine):
        super().__init__(engine)
        self.engine = engine
        self.engine.setup_3d_perspective()
        # region Instancias Singleton
        data_manager = DataManager.instance()
        self.input_manager = InputManager.instance()
        self.cam_manager = CameraManager.instance()
        self.trigger_manager = TriggerManager.instance()
        # endregion
        # region Configuración Player
        player_config = data_manager.load_game_data()
        selected_index = player_config.get("character_index", 0)
        skins = [SantoSkin, AlienSkin, WalterSkin]
        selected_skin = skins[selected_index]
        # endregion
        # region Instancia Level
        level_data = data_manager._load_json("data/levels/level_1.json")
        if level_data:
            spawn_player_config = level_data.get("player_spawn")
            spawn_pos_player = spawn_player_config.get("position", [0, 0, 0])
            spawn_rot_player = spawn_player_config.get("rotation_y", 0)
            self.current_level = Level(level_data)
            self.cam_manager.load_cameras(level_data)
            self.trigger_manager.load_triggers(level_data)
        else:
            print(f"Error Crítico: No se pudieron cargar los datos del nivel...")
            self.current_level = None
            spawn_pos_player = [0, 0, 0]
            spawn_rot_player = 0
        # endregion
        self.player = Player(*spawn_pos_player, selected_skin)
        self.player.rotate(spawn_rot_player)
        self.instructions_lines = [
            "Flechas: Mover a Personaje",
            "E: Interactuar",
            "Esc: Pausar",
        ]

    def update(self, delta_time, _event_list):
        if self.input_manager.was_action_pressed("pause"):
            self.engine.push_state(PauseState(self.engine))
            return

        if self.input_manager.was_action_pressed("return"):
            self.engine.pop_state()
            return
        if self.input_manager.was_action_pressed("interact"):
            if self.current_level:
                self.current_level.handle_interaction(self.player.position, self.player.rotation_y)
        self.player.update(delta_time, self.current_level)
        if self.current_level:
            self.current_level.update(delta_time)
            self.update_active_camera()

    def update_active_camera(self):
        target_camera = self.trigger_manager.check_triggers(self.player)
        current_camera = self.cam_manager.get_active_camera_id()
        if target_camera != current_camera:
            self.cam_manager.set_active_camera(target_camera)

    def draw(self):
        self.engine.setup_3d_perspective()
        _active_cam = self.cam_manager.get_active_camera()
        if _active_cam:
            _active_cam.apply_view()
        else:
            print("¡Advertencia! No hay cámara activa.")
        if self.current_level:
            self.current_level.draw()
            #self._draw_debug_triggers()
        self.player.draw()

        self.engine.setup_2d_orthographic()
        draw_instructions(
            self.engine.display_width,
            self.engine.display_height,
            self.instructions_lines,
        )
        
    def _draw_debug_triggers(self):
        for trigger in self.trigger_manager.triggers:
            trigger.draw()