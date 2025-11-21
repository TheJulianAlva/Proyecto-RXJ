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
    data_manager = DataManager.instance()

    config = data_manager.get_config()
    display_config = config.get("display", {}) 
    display_size = (
        display_config.get("width", 1280),  # 1280 por defecto
        display_config.get("height", 720)  # 720 por defecto
    )
    
    rendered_display_config = config.get("rendered_display", {})
    rendered_display_size = (
        rendered_display_config.get("width", 1280),
        rendered_display_config.get("height", 720)
    )
    
    pygame.display.set_mode(display_size, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Proyecto RXJ")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (rendered_display_size[0] / rendered_display_size[1]), 0.1, 100.0)
    # Materiales: Permite que glColor3f afecte el material
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)

    input_manager = InputManager.instance()
    input_manager.setup_bindings()
    # Inicializar audio y reproducir sound ambient en loop
    audio_mgr = AudioManager.instance()
    ambient_path = "assets/audio/ambientSound.mp3"
    audio_mgr.play_music_loop(ambient_path, loops=-1, volume=0.5)
    # Cargar SFX de pasos para usar en los personajes
    audio_mgr.load_sound("footsteps", "assets/audio/footSteps.mp3")

    game_engine = GameEngine()

    # Botón transparente en esquina superior derecha (pixels de ventana)
    display_config = data_manager.get_config().get("rendered_display", {})
    window_w = display_config.get("width", 1280)
    window_h = display_config.get("height", 720)
    # Tamaño del botón: 48x48 px, margen 10 px
    btn_size = 48
    btn_margin = 10
    btn_rect = (window_w - btn_margin - btn_size, btn_margin, btn_size, btn_size)

    clock = pygame.time.Clock()

    while game_engine.running:
        delta_time = clock.tick(60) / 1000.0

        # --- Manejo de Eventos ---
        events = pygame.event.get()
        input_manager.process_inputs(events)
        # Manejar clicks en el botón transparente para pausar/reanudar música
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                bx, by, bw, bh = btn_rect
                # Nota: las coordenadas de Pygame tienen (0,0) en esquina superior izquierda
                if bx <= mx <= bx + bw and by <= my <= by + bh:
                    audio_mgr.toggle_music()
        
        # --- Actualización de Lógica ---
        game_engine.update(delta_time, events)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        game_engine.draw()

        # (Opcional) dibujar un borde muy sutil del área del botón para debug
        # Se hace en modo 2D ortográfico y luego no se ve si alpha=0
        game_engine.setup_2d_orthographic()
        # No dibujamos nada visible porque el botón es transparente
        glLoadIdentity()
        # Restaurar matrices para 3D siguiente frame
        game_engine.setup_3d_perspective()
        pygame.display.flip()
    
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()