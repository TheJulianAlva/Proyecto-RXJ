import pygame
import math
from OpenGL.GL import *
from systems.texture_manager import TextureManager
from systems.data_manager import DataManager
from utilities.basic_objects import draw_textured_pyrect

class KeyIcon:
    """
    Elemento de UI que muestra un icono de tecla (Pixel Art).
    Mantiene la relación de aspecto original de la textura.
    Incluye una animación suave de flotación (senoidal).
    """
    def __init__(self, x, y, height, key_identifier):
        """
        :param x: Posición X en pantalla.
        :param y: Posición Y en pantalla.
        :param height: Altura deseada en píxeles. El ancho se calcula automático.
        :param key_identifier: Clave para buscar en el JSON (ej. "E", "SPACE", "ESC").
        """
        self.base_x = x
        self.base_y = y
        self.height = height
        
        self.float_amplitude = 5.0  # Píxeles que se mueve arriba/abajo
        self.float_speed = 3.0      # Velocidad de la oscilación
        self.animation_timer = 0.0  # Tiempo acumulado para la animación
        
        data_manager = DataManager.instance()
        icons_config = data_manager.get_config().get("ui_icons", {})
        
        texture_path = icons_config.get(key_identifier, f"assets/ui/icon_keys/{key_identifier}.png")
        
        texture_manager = TextureManager.instance()
        tex_name = f"ui_key_{key_identifier}"
        self.texture_id = texture_manager.get_texture(tex_name, texture_path)
        
        self.width = height
        
        if self.texture_id != -1:
            try:
                surf = pygame.image.load(texture_path)
                aspect_ratio = surf.get_width() / surf.get_height()
                self.width = int(height * aspect_ratio)
            except:
                self.width = height

        self.rect = pygame.Rect(x, y, self.width, self.height)

    def set_position(self, x, y):
        """Actualiza la posición base del icono."""
        self.base_x = x
        self.base_y = y
        self.rect.x = x
        self.rect.y = y

    def update(self, delta_time):
        """
        Actualiza el estado de la animación.
        Debe ser llamado una vez por frame.
        """
        self.animation_timer += delta_time
        
        offset_y = math.sin(self.animation_timer * self.float_speed) * self.float_amplitude
        
        self.rect.x = self.base_x
        self.rect.y = self.base_y + offset_y

    def draw(self):
        """
        Dibuja el icono.
        ASUME: Modo 2D ortográfico y GL_BLEND activados.
        """
        if self.texture_id != -1:
            glColor3f(1.0, 1.0, 1.0)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            
            draw_textured_pyrect(self.rect)
            
            glDisable(GL_TEXTURE_2D)