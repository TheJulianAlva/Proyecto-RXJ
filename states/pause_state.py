import pygame
from states.play_state import PlayState

class PauseState:
    def __init__(self, game):
        self.game = game

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            # Reanudar juego con "P"
            if event.key == pygame.K_p:
                self.game.change_state(PlayState(self.game))

    def update(self, delta_time):
        # Menú de pausa: podrías mostrar un texto "Pausa"
        pass

    def draw(self):
        print("Dibujando estado: PAUSA")
