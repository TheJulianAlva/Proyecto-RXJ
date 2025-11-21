import pygame
from OpenGL.GL import *
from utilities.basic_objects import draw_pyrect, draw_pyrect_border
import utilities.text_renderer as TextUtil
from systems.data_manager import DataManager

class MenuButton:
    def __init__(self, pos_x, pos_y, width, height, 
                 text="", text_color=(255, 255, 255, 255), text_font=None, text_size=32,
                 color=(0.2, 0.2, 0.2, 1.0), hover_color=(0.4, 0.4, 0.4, 1.0), 
                 border_color=(1.0, 1.0, 1.0, 1.0)):
        """
        Inicializa un botón de menú.

        :param pos_x: Posición X de la esquina superior izquierda.
        :param pos_y: Posición Y de la esquina superior izquierda.
        :param width: Ancho del botón.
        :param height: Alto del botón.
        :param text: Texto a mostrar en el botón.
        :param text_color: Color del texto (tupla RGB o RGBA 0-255).
        :param text_font: Nombre de la fuente (clave en TextUtil).
        :param text_size: Tamaño de la fuente.
        :param color: Color base del botón (RGB float 0.0-1.0).
        :param hover_color: Color cuando está seleccionado (RGB float 0.0-1.0).
        :param border_color: Color del borde (RGB float 0.0-1.0).
        """
        data_manager = DataManager.instance()
        config = data_manager.get_config()

        display_config = config.get("rendered_display", {})
        display_height = display_config.get("height", 720)
        self.text_pos_y = display_height-pos_y-height/2
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.text = text
        self.text_color = text_color
        self.text_font = text_font
        self.text_size = text_size
        
        # Colores (normalizados 0.0 - 1.0 para OpenGL)
        self.base_color = self._convert_rgba_color(color)
        self.hover_color = self._convert_rgba_color(hover_color)
        self.border_color = self._convert_rgba_color(border_color)
        
        self.is_selected = False

    def set_selected(self, selected):
        """
        Establece el estado de selección del botón.
        :param selected: Booleano (True/False).
        """
        self.is_selected = selected

    def _convert_rgba_color(self, color):
        '''
        Toma una tupla con valores 0-255 y retorna 
        una tupla con valores flotantes entre 0.0 y 1.0
        '''
        # Si el color ya está en rango 0.0-1.0, devolver tal cual.
        try:
            # Detectar si los valores parecen estar en 0-255 (alguno > 1.0)
            if any(value > 1.0 for value in color):
                return tuple(value / 255.0 for value in color)
            else:
                return tuple(float(value) for value in color)
        except Exception:
            # Fallback: devolver gris oscuro
            return (0.2, 0.2, 0.2, 1.0)

    def _darken_color(self, color, factor=0.6):
        """Devuelve una versión más oscura del color (multiplica RGB por factor)."""
        # color puede tener 3 o 4 componentes
        if not color:
            return color
        rgb = [max(0.0, min(1.0, c * factor)) for c in color[:3]]
        if len(color) == 4:
            return (*rgb, color[3])
        return tuple(rgb)

    def draw(self):
        """
        Dibuja el botón en la pantalla.
        ASUME: Modo ortográfico 2D activo (setup_2d_orthographic).
        """
        # Cuando está seleccionado, usar una versión más oscura del color base
        if self.is_selected:
            # Priorizar hover_color si fue proporcionada, sino oscurecer base
            if self.hover_color and any(c != 0 for c in self.hover_color[:3]):
                current_color = self._darken_color(self.hover_color, factor=0.6)
            else:
                current_color = self._darken_color(self.base_color, factor=0.6)
        else:
            current_color = self.base_color

        glColor4fv(current_color)
        draw_pyrect(self.rect)
        glColor4fv(self.border_color)
        draw_pyrect_border(self.rect)
        

        full_text_color = self.text_color
        if len(self.text_color) == 3:
            full_text_color = (*self.text_color, 255)

        TextUtil.draw_text_2d(
            self.rect.centerx, 
            self.text_pos_y, 
            self.text,
            font_name=self.text_font, 
            size=self.text_size, 
            center=True, 
            color=full_text_color
        )
