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
from systems.audio_manager import AudioManager
from game_objects.level import Level
from game_objects.character_models.santo import SantoSkin
from game_objects.character_models.alien import AlienSkin
from game_objects.character_models.walter import WalterSkin
from game_objects.player import Player
from states.pause_state import PauseState
from game_objects.ui_elements.key_icon import KeyIcon
from game_objects.ui_elements.menu_button import MenuButton
from utilities.instructions_overlay import draw_instructions
from utilities.fade_transition import FadeTransition
from states.game_complete_state import GameCompleteState

class PlayState(BaseState):
    def __init__(self, engine, initial_level="level_1"):
        super().__init__(engine)
        self.engine = engine
        self.engine.setup_3d_perspective()
        # region Instancias Singleton
        self.data_manager = DataManager.instance()
        self.input_manager = InputManager.instance()
        self.cam_manager = CameraManager.instance()
        self.trigger_manager = TriggerManager.instance()
        self.audio_manager = AudioManager.instance()
        # endregion
        config = self.data_manager.get_config()
        self.display_width = self.engine.display_width
        self.display_height = self.engine.display_height
        
        # region Configuración Player
        player_config = self.data_manager.load_game_data()
        selected_index = player_config.get("character_index", 0)
        skins = [SantoSkin, AlienSkin, WalterSkin]
        self.selected_skin = skins[selected_index]
        # endregion
        
        # region Transiciones
        self.fade_transition = FadeTransition(self.display_width, self.display_height)
        self.next_level_id = None  # ID del siguiente nivel a cargar
        # endregion
        
        # Inicializar variables de nivel y jugador
        self.current_level = None
        self.current_puzzle = None
        self.player = None
        
        # Cargar el nivel inicial
        self.load_level(initial_level)
        
        # region Instancia Sounds
        data_assets_play = config.get("states", {}).get("play_state", {}).get("assets")
        sound_assets = data_assets_play.get("sounds").items()
        for sound_name, sound_path in sound_assets:
            self.audio_manager.load_sound(sound_name, sound_path)
        play_music = data_assets_play.get("music")
        self.audio_manager.play_music_loop(play_music, volume=0.6)
        # endregion
        
        self.player_can_touch_interact = False
        self.player_can_read_interact = False
        self.instructions_lines = [
            "Objetivo: Acomoda las estatuas en sus respectivos pedestales..."
        ]
        # region Instancias UI
        self.key_interact = KeyIcon(
            self.display_width*0.85,
            self.display_height*0.65,
            84,
            "M"
            )
        self.key_read = KeyIcon(
            self.display_width*0.85,
            self.display_height*0.80,
            84,
            "L"
            )
        self.button_interact = MenuButton(
            self.display_width*0.72,
            self.display_height*0.68,
            self.display_width*0.1,
            self.display_height*0.05,
            text= "Interactuar",
            text_font="montserrat_bold",
            text_size=28,
            color=(0, 0, 0, 0),
            border_color=(0, 0, 0, 0)
        )
        self.button_read = MenuButton(
            self.display_width*0.72,
            self.display_height*0.83,
            self.display_width*0.1,
            self.display_height*0.05,
            text= "Leer",
            text_font="montserrat_bold",
            text_size=28,
            color=(0, 0, 0, 0),
            border_color=(0, 0, 0, 0)
        )
        # endregion
        
    def load_level(self, level_id):
        """
        Carga un nivel dinámicamente basado en su ID.
        Limpia el nivel anterior si existe.
        """
        if self.current_level:
            self.current_level.destroy()
            self.current_level = None
            self.current_puzzle = None
        
        level_path = f"data/levels/{level_id}.json"
        level_data = self.data_manager._load_json(level_path)
        
        if not level_data:
            print(f"Error: No se pudo cargar el nivel '{level_id}'")
            return
        
        # Crear nuevo nivel
        spawn_player_config = level_data.get("player_spawn")
        spawn_pos_player = spawn_player_config.get("position", [0, 0, 0])
        spawn_rot_player = spawn_player_config.get("rotation_y", 0)
        
        self.current_level = Level(level_data, self.display_width, self.display_height)
        self.cam_manager.load_cameras(level_data)
        self.trigger_manager.load_triggers(level_data)
        
        if self.current_level:
            self.current_puzzle = self.current_level.puzzle
        
        # Reposicionar jugador (o crear si es primera vez)
        if self.player:
            self.player.position = list(spawn_pos_player)
            self.player.rotate(spawn_rot_player)
        else:
            self.player = Player(*spawn_pos_player, self.selected_skin)
            self.player.rotate(spawn_rot_player)
        
        print(f"Nivel '{level_id}' cargado exitosamente.")

    def update(self, delta_time, _event_list):
        # Actualizar transición si está activa
        if self.fade_transition.is_active():
            self.fade_transition.update(delta_time)
            return  # No procesar inputs durante la transición
        
        # Verificar si se debe iniciar transición de nivel
        if self.current_puzzle and self.current_puzzle.level_complete:
            # Obtener el next_level_id del nivel actual
            level_metadata = self.current_level.data.get("metadata", {})
            next_level_id = level_metadata.get("next_level_id")
            
            if next_level_id == "game_complete" or next_level_id is None:
                # Juego completado
                def transition_to_complete():
                    self.audio_manager.stop_music()
                    self.camera_recording_mask_video.release()
                    self.engine.change_state(GameCompleteState(self.engine))
                
                self.fade_transition.start_transition(
                    on_fade_out_complete=transition_to_complete
                )
            else:
                # Cargar siguiente nivel
                def load_next_level():
                    self.load_level(next_level_id)
                
                self.fade_transition.start_transition(
                    on_fade_out_complete=load_next_level
                )
            
            return
        
        self.player_can_touch_interact = self.current_puzzle.can_touch_interact(self.player.position, self.player.rotation_y)
        self.player_can_read_interact = self.current_puzzle.can_read_interact(self.player.position, self.player.rotation_y)
        
        if self.input_manager.was_action_pressed("pause"):
            self.engine.push_state(PauseState(self.engine))
            return

        if self.input_manager.was_action_pressed("return"):
            self.camera_recording_mask_video.release()
            self.engine.pop_state()
            return
            
        if self.input_manager.was_action_pressed("interact") and self.player_can_touch_interact:
            if self.current_level:
                self.current_level.handle_interaction(self.player.position, self.player.rotation_y)
                
        if self.input_manager.was_action_pressed("read") and self.player_can_read_interact:
            if self.current_level:
                self.current_level.handle_read_interaction(self.player.position, self.player.rotation_y)
                
        self.player.update(delta_time, self.current_level)
        
        if self.current_level:
            self.current_level.update(delta_time)
            self.update_active_camera()
        self.key_interact.update(delta_time)    
        self.key_read.update(delta_time)    

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
            self.button_interact.draw()
        if self.player_can_read_interact:
            self.key_read.draw()
            self.button_read.draw()
        
        # Dibujar el fade si está activo
        if self.fade_transition.is_active():
            self.fade_transition.draw()

        
    def _draw_debug_triggers(self):
        for trigger in self.trigger_manager.triggers:
            trigger.draw()