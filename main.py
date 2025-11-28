import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from engine import GameEngine
from systems.data_manager import DataManager
from systems.input_manager import InputManager
from systems.audio_manager import AudioManager

def main():
    pygame.init()
    pygame.font.init()
    # region Instancias Singleton
    data_manager = DataManager.instance()
    input_manager = InputManager.instance()
    audio_manager = AudioManager.instance()
    # endregion
    config = data_manager.get_config()
    display_config = config.get("display", {}) 
    display_size = (
        display_config.get("width", 1280),
        display_config.get("height", 720)
    )
    
    pygame.display.set_mode(display_size, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Proyecto RXJ")
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    input_manager.setup_bindings()

    game_engine = GameEngine()

    clock = pygame.time.Clock()

    while game_engine.running:
        delta_time = clock.tick(60) / 1000.0

        # --- Manejo de Eventos ---
        events = pygame.event.get()
        input_manager.process_inputs(events)
        # --- Actualización de Lógica ---
        game_engine.update(delta_time, events)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        game_engine.draw()
        pygame.display.flip()
    
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()