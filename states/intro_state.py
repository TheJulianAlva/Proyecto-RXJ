import pygame
from OpenGL.GL import *
from states.base_state import BaseState
from systems.input_manager import InputManager
from utilities.video_player import VideoPlayer
from systems.audio_manager import AudioManager

class IntroState(BaseState):
    """
    Estado de Introducción.
    Reproduce la intro del juego.
    Se puede saltar presionando Enter o Escape.
    """
    def __init__(self, engine):
        super().__init__(engine)
        self.engine = engine
        self.width = self.engine.display_width
        self.height = self.engine.display_height

        self.input_manager = InputManager.instance()
        self.audio_manager = AudioManager.instance()

        video_path = "assets/video/intro_video.mp4"
        self.audio_name = "intro_audio"
        audio_path = "assets/audio/intro_audio.ogg"
        self.video = VideoPlayer(video_path, width=self.width*0.9, height=self.height, loop=False)
        self.audio_manager.load_sound(self.audio_name, audio_path)
        self.audio_manager.play_sound(self.audio_name, volume=0.5)
        self.video.play()
        
        print("IntroState: Reproduciendo video de introducción...")

    def update(self, delta_time, _event_list):
        self.video.update(delta_time)
        
        skip_input = self.input_manager.was_action_pressed("quit") or \
                     self.input_manager.was_action_pressed("ui_select")
        
        video_ended = self.video.has_finished
        
        if skip_input or video_ended:
            self._go_to_next_state()

    def draw(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.engine.setup_2d_orthographic()
        self.video.draw(self.width*0.05, 0)

    def _go_to_next_state(self):
        """Limpia recursos y cambia al estado de selección."""
        print("IntroState: Finalizando intro.")
        self.video.stop()
        self.audio_manager.unload_sound(self.audio_name)
        self.video.release()
        from states.player_selection_state import PlayerSelectionState
        self.engine.change_state(PlayerSelectionState(self.engine))