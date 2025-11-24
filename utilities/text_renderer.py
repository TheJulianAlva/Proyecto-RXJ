import pygame
from OpenGL.GL import *

# --- 1. Diccionario de Fuentes ---
FONTS = {
    "montserrat_bold": "fonts/Montserrat-Thin.ttf",
}

DEFAULT_FONT_NAME = "montserrat_bold"

FONT_CACHE = {}

def get_font(font_name=DEFAULT_FONT_NAME, size=32):
    """
    Obtiene una fuente de Pygame del nombre y tamaño especificados.
    Usa un caché para evitar recargar.
    """
    if not font_name:
        font_name = DEFAULT_FONT_NAME
    key = (font_name, size)
    
    if key not in FONT_CACHE:
        font_path_to_load = None
        
        if font_name in FONTS:
            font_path_to_load = FONTS[font_name]
        else:
            print(f"Advertencia: Fuente '{font_name}' no encontrada en FONT_PATHS. Usando default de Pygame.")
            
        try:
            loaded_font = pygame.font.Font(font_path_to_load, size)
            FONT_CACHE[key] = loaded_font
            
        except Exception as e:
            print(f"Error al cargar la fuente '{font_path_to_load}': {e}.")
            print("Usando la fuente default absoluta de Pygame como fallback.")
            fallback_font = pygame.font.Font(pygame.font.get_default_font(), size)
            FONT_CACHE[key] = fallback_font

    return FONT_CACHE[key]

def draw_text_2d(x, y, text, font_name=DEFAULT_FONT_NAME, size=32, center = False, color=(255, 255, 255, 255)):
    """
    Dibuja texto en coordenadas de pantalla 2D.
    """
    try:
        font = get_font(font_name, size)
        
        text_surface = font.render(text, True, color)
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        width, height = text_surface.get_size()
        
        # Ajustar posición si se solicita centrado
        if center:
            x -= width / 2
            y -= height / 2
        
        glWindowPos2f(x, y) 
        glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        
    except Exception as e:
        print(f"Error al dibujar texto '{text}': {e}")