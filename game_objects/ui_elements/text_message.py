import pygame
import math
from OpenGL.GL import *
from systems.data_manager import DataManager
from utilities.basic_objects import draw_pyrect, draw_pyrect_border
import utilities.text_renderer as TextUtil

class TextMessage:
    """
    Muestra un mensaje de texto temporal en pantalla con un fondo semitransparente.
    Incluye animación de entrada/salida (fade o slide) y movimiento suave.
    """
    def __init__(self, text, duration=3.0, y_pos=100, font_name="montserrat_bold", font_size=32):
        """
        :param text: El mensaje a mostrar.
        :param duration: Tiempo en segundos antes de desaparecer.
        :param y_pos: Posición vertical base (desde arriba).
        :param font_size: Tamaño de la fuente.
        """
        data_manager = DataManager.instance()
        config = data_manager.get_config()
        self.text = text
        self.duration = duration
        self.timer = 0.0
        self.is_active = True
        
        # Configuración Visual
        self.base_y = y_pos
        self.font_size = font_size
        self.bg_color = (0.0, 0.0, 0.0, 0.7) # Negro semitransparente
        self.text_color = (255, 255, 255, 255)
        self.border_color = (0.8, 0.8, 0.8, 1.0)
        
        # Configuración de Animación
        self.fade_in_time = 0.5
        self.fade_out_time = 0.5
        self.float_speed = 2.0
        self.float_amplitude = 5.0
        
        font = TextUtil.get_font(font_name, size=font_size)
        text_w, text_h = font.size(text)

        display_config = config.get("rendered_display", {})
        display_width = display_config.get("width", 1280)
        display_height = display_config.get("height", 720)
        padding_x = display_width*0.1
        padding_y = display_height*0.05
        
        rect_w = text_w + (padding_x * 2)
        rect_h = text_h + (padding_y * 2)
        rect_x = (display_width - rect_w) / 2
        
        self.rect = pygame.Rect(rect_x, y_pos, rect_w, rect_h)
        self.current_alpha = 0.0

    def update(self, delta_time):
        if not self.is_active:
            return

        self.timer += delta_time
        
        if self.timer >= self.duration:
            self.is_active = False
            return

        # region Lógica de Animación (Alpha)
        # Fade In
        if self.timer < self.fade_in_time:
            self.current_alpha = self.timer / self.fade_in_time
        # Fade Out
        elif self.timer > (self.duration - self.fade_out_time):
            remaining = self.duration - self.timer
            self.current_alpha = remaining / self.fade_out_time

        else:
            self.current_alpha = 1.0
        # endregion
        # region Lógica de Movimiento (Senoidal)
        offset_y = math.sin(self.timer * self.float_speed) * self.float_amplitude
        
        # Si estamos entrando (fade in), añadimos un desplazamiento extra hacia arriba
        # para que parezca que el mensaje "sube"
        if self.timer < self.fade_in_time:
            slide_offset = (1.0 - self.current_alpha) * 20.0
            offset_y += slide_offset
            
        self.rect.y = self.base_y + offset_y
        # endregion
    def draw(self):
        if not self.is_active:
            return

        r, g, b, base_a = self.bg_color
        final_alpha = base_a * self.current_alpha
        glColor4f(r, g, b, final_alpha)
        draw_pyrect(self.rect)
        
        br, bg, bb, b_alpha = self.border_color
        glColor4f(br, bg, bb, b_alpha * self.current_alpha)
        draw_pyrect_border(self.rect)
        
        text_r, text_g, text_b, text_a = self.text_color
        final_text_alpha = int(text_a * self.current_alpha)
        
        TextUtil.draw_text_2d(
            self.rect.centerx,
            self.rect.centery,
            self.text,
            size=self.font_size,
            center=True,
            color=(text_r, text_g, text_b, final_text_alpha)
        )