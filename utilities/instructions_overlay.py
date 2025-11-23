import pygame
from OpenGL.GL import glColor4f
from utilities.basic_objects import draw_pyrect, draw_pyrect_border
import utilities.text_renderer as TextUtil


def draw_instructions(display_width, display_height, lines, *, top_left=(24, 24), font_name="montserrat_bold", font_size=18,
                      padding=12, line_spacing=6, background_color=(0.0, 0.0, 0.0, 0.55), border_color=(0.32, 0.48, 0.82, 0.65),
                      text_color=(236, 242, 255, 255)):
    if not lines:
        return

    font = TextUtil.get_font(font_name, font_size)
    metrics = [font.size(line) for line in lines]
    max_width = max(width for width, _ in metrics)
    total_height = sum(height for _, height in metrics) + line_spacing * (len(lines) - 1 if len(lines) > 1 else 0)

    panel_rect = pygame.Rect(
        int(round(top_left[0])),
        int(round(top_left[1])),
        int(round(max_width + padding * 2)),
        int(round(total_height + padding * 2)),
    )

    glColor4f(*background_color)
    draw_pyrect(panel_rect)
    glColor4f(*border_color)
    draw_pyrect_border(panel_rect)

    cursor_y = panel_rect.top + padding
    for (line, (width, height)) in zip(lines, metrics):
        text_x = panel_rect.left + padding
        text_y = display_height - (cursor_y + height)
        TextUtil.draw_text_2d(
            text_x,
            text_y,
            line,
            font_name=font_name,
            size=font_size,
            center=False,
            color=text_color,
        )
        cursor_y += height + line_spacing
