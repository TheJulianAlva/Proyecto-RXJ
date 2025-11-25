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
from game_objects.ui_elements.key_icon import KeyIcon
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
        config = data_manager.get_config()
        display_config = config.get("rendered_display", {})
        self.display_width = display_config.get("width", 1280)
        self.display_height = display_config.get("height", 720)
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
            self.current_level = Level(level_data, self.display_width, self.display_height)
            self.cam_manager.load_cameras(level_data)
            self.trigger_manager.load_triggers(level_data)
            if self.current_level: self.current_puzzle = self.current_level.puzzle
                
        else:
            print(f"Error Crítico: No se pudieron cargar los datos del nivel...")
            self.current_level = None
            self.current_puzzle = None
            spawn_pos_player = [0, 0, 0]
            spawn_rot_player = 0
        # endregion
        self.player = Player(*spawn_pos_player, selected_skin)
        self.player.rotate(spawn_rot_player)
        self.player_can_touch_interact = False
        self.player_can_read_interact = False
        self.instructions_lines = [
            "Flechas: Mover a Personaje",
            "E: Interactuar",
            "Esc: Pausar",
        ]
        self.key_interact = KeyIcon(
            self.display_width*0.85,
            self.display_height*0.75,
            84,
            "E"
            )

    def update(self, delta_time, _event_list):
        self.player_can_touch_interact = self.current_puzzle.can_touch_interact(self.player.position, self.player.rotation_y)
        self.player_can_read_interact = self.current_puzzle.can_read_interact(self.player.position, self.player.rotation_y)
        if self.input_manager.was_action_pressed("pause"):
            self.engine.push_state(PauseState(self.engine))
            return

        if self.input_manager.was_action_pressed("return"):
            self.engine.pop_state()
            return
        if self.input_manager.was_action_pressed("interact") and self.player_can_touch_interact:
            if self.current_level:
                self.current_level.handle_interaction(self.player.position, self.player.rotation_y)
        self.player.update(delta_time, self.current_level)
        if self.current_level:
            self.current_level.update(delta_time)
            self.update_active_camera()
        self.key_interact.update(delta_time)    


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
        self.player.draw()
        if self.current_level:
            self.current_level.draw()
            #self._draw_debug_triggers()


        self.engine.setup_2d_orthographic()
        draw_instructions(
            self.engine.display_width,
            self.engine.display_height,
            self.instructions_lines,
        )
        if self.player_can_touch_interact:
            self.key_interact.draw()
        
    def _draw_debug_triggers(self):
        for trigger in self.trigger_manager.triggers:
            trigger.draw()