import pygame
import math
from OpenGL.GL import *
from systems.data_manager import DataManager
from utilities.basic_objects import draw_pyrect, draw_pyrect_border
import utilities.text_renderer as TextUtil

class BoardMessage:
    """
    Muestra un panel con MULTIPLES líneas de texto.
    Incluye animación de entrada/salida y fondo semitransparente.
    """
    def __init__(self, text_lines, duration=5.0, y_pos=100, font_name="montserrat_bold", font_size=24, text_color=(255, 255, 255, 255)):
        """
        :param text_lines: Lista de strings ["Línea 1", "Línea 2"].
        :param duration: Tiempo en segundos antes de desaparecer.
        :param y_pos: Posición vertical base (desde arriba).
        :param font_size: Tamaño de la fuente.
        :param text_color: Color del texto (R, G, B, A).
        """
        data_manager = DataManager.instance()
        config = data_manager.get_config()
        
        self.text_lines = text_lines
        self.duration = duration
        self.timer = 0.0
        self.is_active = True
        
        # Configuración Visual
        self.base_y = y_pos
        self.font_size = font_size
        self.line_spacing = 1.2 # Espaciado entre líneas (multiplicador de altura de fuente)
        
        self.bg_color = (0.0, 0.0, 0.0, 1.0) # Negro opaco
        self.text_color = text_color
        self.border_color = (0.8, 0.8, 0.8, 1.0)
        
        # Configuración de Animación
        self.fade_in_time = 0.5
        self.fade_out_time = 0.5
        self.float_speed = 2.0
        self.float_amplitude = 3.0 # Menor amplitud para texto largo (se lee mejor)
        
        # --- CÁLCULO DE TAMAÑO DINÁMICO ---
        font = TextUtil.get_font(font_name, size=font_size)
        
        max_text_w = 0
        total_text_h = 0
        single_line_h = font.get_linesize() # Altura de una línea estándar
        
        # Calcular ancho máximo y altura total
        for line in text_lines:
            w, h = font.size(line)
            if w > max_text_w:
                max_text_w = w
            # Sumamos altura + un poco de espacio extra
            total_text_h += int(single_line_h * self.line_spacing)
            
        # Ajustar un poco la altura final (quitar el espacio extra del último elemento)
        # total_text_h -= int(single_line_h * (self.line_spacing - 1.0))

        display_config = config.get("rendered_display", {})
        display_width = display_config.get("width", 1280)
        # display_height = display_config.get("height", 720) # No usado aquí
        
        padding_x = 30
        padding_y = 30
        
        rect_w = max_text_w + (padding_x * 2)
        rect_h = total_text_h + (padding_y * 2)
        rect_x = (display_width - rect_w) / 2
        
        self.rect = pygame.Rect(rect_x, y_pos, rect_w, rect_h)
        self.current_alpha = 0.0
        
        # Guardamos la altura de línea para usarla en draw()
        self.line_height_pixels = int(single_line_h * self.line_spacing)

    def update(self, delta_time):
        if not self.is_active:
            return

        self.timer += delta_time
        
        if self.timer >= self.duration:
            self.is_active = False
            return

        # region Lógica de Animación (Alpha)
        if self.timer < self.fade_in_time:
            self.current_alpha = self.timer / self.fade_in_time
        elif self.timer > (self.duration - self.fade_out_time):
            remaining = self.duration - self.timer
            self.current_alpha = remaining / self.fade_out_time
        else:
            self.current_alpha = 1.0
        # endregion

        # region Lógica de Movimiento
        offset_y = math.sin(self.timer * self.float_speed) * self.float_amplitude
        
        if self.timer < self.fade_in_time:
            slide_offset = (1.0 - self.current_alpha) * 20.0
            offset_y += slide_offset
            
        self.rect.y = self.base_y + offset_y
        # endregion

    def draw(self):
        if not self.is_active:
            return

        # 1. Fondo
        r, g, b, base_a = self.bg_color
        final_alpha = base_a * self.current_alpha
        glColor4f(r, g, b, final_alpha)
        draw_pyrect(self.rect)
        
        # 2. Borde
        br, bg, bb, b_alpha = self.border_color
        glColor4f(br, bg, bb, b_alpha * self.current_alpha)
        draw_pyrect_border(self.rect)
        
        # 3. Texto (Múltiples líneas)
        text_r, text_g, text_b, text_a = self.text_color
        final_text_alpha = int(text_a * self.current_alpha)
        
        # Empezamos a dibujar desde arriba + padding
        current_text_y = self.rect.top + 30 # Mismo padding_y que definimos en __init__
        center_x = self.rect.centerx
        
        for line in self.text_lines:
            TextUtil.draw_text_2d(
                center_x,
                current_text_y,
                line,
                size=self.font_size,
                center=True,
                color=(text_r, text_g, text_b, final_text_alpha)
            )
            current_text_y -= self.line_height_pixels