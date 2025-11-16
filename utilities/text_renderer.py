import pygame
from OpenGL.GL import *

# Un caché simple para no recargar la misma fuente una y otra vez
FONT_CACHE = {}

def get_font(size=32):
    """
    Obtiene una fuente de Pygame del tamaño especificado.
    Usa un caché para evitar recargar.
    """
    if size not in FONT_CACHE:
        try:
            # (Asumiendo que pygame.font.init() fue llamado en main.py)
            FONT_CACHE[size] = pygame.font.Font(None, size)
        except Exception as e:
            print(f"Error al cargar la fuente tamaño {size}: {e}.")
            FONT_CACHE[size] = pygame.font.Font(pygame.font.get_default_font(), size)
    return FONT_CACHE[size]

def draw_text_2d(x, y, text, size=32, color=(5, 255, 255, 255)):
    """
    Dibuja texto en coordenadas de pantalla 2D.
    
    IMPORTANTE: Esta función ASUME que ya estás en modo ortográfico 2D
    (es decir, que ya llamaste a engine.setup_2d_orthographic()).
    """
    try:
        font = get_font(size)
        text_surface = font.render(text, True, color)
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        width, height = text_surface.get_size()
        #glRasterPos2f(x, 600 - y - height)
        glWindowPos2f(x, 600 - y - height) 
        glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        
    except Exception as e:
        print(f"Error al dibujar texto '{text}': {e}")