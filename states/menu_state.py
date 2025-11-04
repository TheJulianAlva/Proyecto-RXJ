import pygame
from states.play_state import PlayState
from states.play_state import BaseState

class MenuState(BaseState):
    def __init__(self, game):
        super().__init__()
        self.game = game

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            # Iniciar juego con ENTER
            if event.key == pygame.K_RETURN:
                self.game.change_state(PlayState(self.game))

    def update(self, delta_time):
        # Aquí podrías animar el fondo o botones
        pass

    def draw(self):
        print("Dibujando estado: MENÚ PRINCIPAL")
