import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from engine import GameEngine
from systems.camera_manager import CameraManager
from systems.input_manager import InputManager

def main():
    pygame.init()
    display_size = (800, 600)
    pygame.display.set_mode(display_size, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Mi Juego de Puzzles 3D - Fase 2")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (800 / 600), 0.1, 100.0)
    cam_manager = CameraManager.instance()
    cam_manager.load_cameras()
    glEnable(GL_DEPTH_TEST)

    input_manager = InputManager.instance()
    input_manager.setup_bindings()
    game_engine = GameEngine()

    clock = pygame.time.Clock()

    while game_engine.running:
        delta_time = clock.tick(60) / 1000.0

        # --- Manejo de Eventos ---
        events = pygame.event.get()
        input_manager.process_inputs(events)

        if input_manager.did_quit():
            running = False
        
        # --- Actualización de Lógica ---
        game_engine.update(delta_time, events)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        game_engine.draw()
        pygame.display.flip()
    
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()