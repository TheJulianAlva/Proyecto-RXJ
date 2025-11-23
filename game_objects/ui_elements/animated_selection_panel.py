import pygame
from OpenGL.GL import GL_QUADS, glBegin, glColor4f, glEnd, glVertex2f
from systems.data_manager import DataManager
import utilities.text_renderer as TextUtil
from utilities.basic_objects import draw_pyrect, draw_pyrect_border


def _normalize_color(color):
    """Convierte colores en formato 0-255 o 0-1 a floats 0-1."""
    if len(color) == 3:
        if any(channel > 1.0 for channel in color):
            color = (*color, 255)
        else:
            color = (*color, 1.0)
    if any(channel > 1.0 for channel in color):
        return tuple(channel / 255.0 for channel in color)
    return tuple(float(channel) for channel in color)


def _clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))


def _lerp(a, b, t):
    return a + (b - a) * t


def _lerp_color(color_a, color_b, t):
    return tuple(_lerp(color_a[i], color_b[i], t) for i in range(len(color_a)))


def _brighten(color, amount):
    r, g, b, a = color
    return (_clamp(r + amount), _clamp(g + amount), _clamp(b + amount), a)


def _darken(color, amount):
    r, g, b, a = color
    return (_clamp(r - amount), _clamp(g - amount), _clamp(b - amount), a)


def _approach(value, target, step):
    if value < target:
        return min(value + step, target)
    if value > target:
        return max(value - step, target)
    return value


def _scaled_rect(rect, scale):
    width = max(1, int(round(rect.width * scale)))
    height = max(1, int(round(rect.height * scale)))
    scaled = pygame.Rect(0, 0, width, height)
    scaled.center = rect.center
    return scaled


def _inflate_rect(rect, amount):
    inflated = rect.inflate(int(round(amount)), int(round(amount)))
    return inflated


class _SelectablePanelItem:
    def __init__(
        self,
        rect,
        label,
        display_height,
        font_name,
        font_size,
        base_color,
        highlight_color,
        border_color,
        glow_color,
        accent_color,
        text_color,
        index_badge,
    ):
        self.rect = rect
        self.label = label
        self.display_height = display_height
        self.font_name = font_name
        self.font_size = font_size
        self.base_color = _normalize_color(base_color)
        self.highlight_color = _normalize_color(highlight_color)
        self.border_color = _normalize_color(border_color)
        self.glow_color = _normalize_color(glow_color)
        self.accent_color = _normalize_color(accent_color)
        self.text_color = text_color if len(text_color) == 4 else (*text_color, 255)
        self.index_badge = index_badge
        self.is_selected = False
        self.hovered = False
        self.highlight = 0.0
        self.target_highlight = 0.0
        self.press_feedback = 0.0
        self.animation_speed = 6.5
        self.hover_intensity = 0.35

    def set_selected(self, selected, *, play_feedback=True):
        self.is_selected = selected
        self.target_highlight = 1.0 if selected else (self.hover_intensity if self.hovered else 0.0)
        if play_feedback and selected:
            self.press_feedback = 1.0

    def set_hovered(self, hovered):
        self.hovered = hovered
        if not self.is_selected:
            self.target_highlight = self.hover_intensity if hovered else 0.0

    def trigger_feedback(self):
        self.press_feedback = 1.0

    def update(self, delta_time):
        step = self.animation_speed * delta_time
        self.highlight = _approach(self.highlight, self.target_highlight, step)
        if self.press_feedback > 0.0:
            self.press_feedback = max(0.0, self.press_feedback - delta_time * 4.5)

    def draw(self):
        base_rect = self.rect
        enlarge_scale = 1.0 + 0.025 * self.highlight
        press_scale = 1.0 - 0.06 * self.press_feedback
        current_scale = _clamp(enlarge_scale * press_scale, 0.85, 1.12)
        current_rect = _scaled_rect(base_rect, current_scale)

        if self.highlight > 0.01:
            glow_rect = _inflate_rect(base_rect, 24 * self.highlight)
            glColor4f(
                self.glow_color[0],
                self.glow_color[1],
                self.glow_color[2],
                self.glow_color[3] * (0.45 + 0.4 * self.highlight),
            )
            draw_pyrect(glow_rect)

        current_color = _lerp_color(self.base_color, self.highlight_color, self.highlight)
        top_color = _brighten(current_color, 0.12 + 0.08 * self.highlight)
        bottom_color = _darken(current_color, 0.08)

        glBegin(GL_QUADS)
        glColor4f(*top_color)
        glVertex2f(current_rect.left, current_rect.top)
        glColor4f(*top_color)
        glVertex2f(current_rect.right, current_rect.top)
        glColor4f(*bottom_color)
        glVertex2f(current_rect.right, current_rect.bottom)
        glColor4f(*bottom_color)
        glVertex2f(current_rect.left, current_rect.bottom)
        glEnd()

        border_color = _lerp_color(self.border_color, self.highlight_color, self.highlight)
        glColor4f(*border_color)
        draw_pyrect_border(current_rect)

        if self.highlight > 0.01:
            accent_height = max(4, int(round(current_rect.height * 0.14)))
            accent_width = int(round(current_rect.width * (0.4 + 0.6 * self.highlight)))
            accent_rect = pygame.Rect(0, 0, accent_width, accent_height)
            accent_rect.centerx = current_rect.centerx
            accent_rect.bottom = current_rect.bottom - 8
            glColor4f(
                self.accent_color[0],
                self.accent_color[1],
                self.accent_color[2],
                self.accent_color[3] * (0.4 + 0.4 * self.highlight),
            )
            draw_pyrect(accent_rect)

        badge_size = max(22, int(round(current_rect.height * 0.22)))
        badge_rect = pygame.Rect(0, 0, badge_size, badge_size)
        badge_rect.centerx = current_rect.centerx
        badge_rect.top = current_rect.top + 10
        badge_color = _lerp_color(self.border_color, self.highlight_color, 0.45)
        glColor4f(*badge_color)
        draw_pyrect(badge_rect)
        glColor4f(*_darken(badge_color, 0.25))
        draw_pyrect_border(badge_rect)

        badge_text_y = self.display_height - (badge_rect.centery)
        TextUtil.draw_text_2d(
            badge_rect.centerx,
            badge_text_y,
            str(self.index_badge),
            font_name=self.font_name,
            size=int(self.font_size * 0.7),
            center=True,
            color=self.text_color,
        )

        text_y = self.display_height - current_rect.centery
        TextUtil.draw_text_2d(
            current_rect.centerx,
            text_y,
            self.label,
            font_name=self.font_name,
            size=self.font_size,
            center=True,
            color=self.text_color,
        )


class AnimatedSelectionPanel:
    """Panel 2D con tres opciones seleccionables y animacion de feedback."""

    def __init__(
        self,
        topleft,
        size,
        labels=("Opcion A", "Opcion B", "Opcion C"),
        title="Selecciona un panel",
        on_select=None,
        font_name="montserrat_bold",
        item_font_size=26,
    ):
        if len(labels) != 3:
            raise ValueError("AnimatedSelectionPanel requiere exactamente tres etiquetas")

        self.on_select = on_select
        self.title = title
        self.font_name = font_name
        self.item_font_size = item_font_size

        data_manager = DataManager.instance()
        config = data_manager.get_config().get("rendered_display", {})
        self.display_width = config.get("width", 1280)
        self.display_height = config.get("height", 720)

        self.container_rect = pygame.Rect(
            int(round(topleft[0])),
            int(round(topleft[1])),
            int(round(size[0])),
            int(round(size[1])),
        )

        self.container_color = _normalize_color((24, 32, 48, 235))
        self.container_border_color = _normalize_color((84, 120, 184, 255))
        self.shadow_color = _normalize_color((0, 0, 0, 170))
        self.text_color = (240, 244, 255, 255)
        self.caption_color = (192, 210, 235, 255)
        self.caption_font_size = max(18, int(item_font_size * 0.72))

        self.padding = 24
        self.item_spacing = 18
        self.title_margin = 12

        items_top = self.container_rect.top + self.padding + self.title_margin + item_font_size
        items_bottom = self.container_rect.bottom - self.padding - self.caption_font_size - 12
        items_height = max(1, int(round(items_bottom - items_top)))

        available_width = (
            self.container_rect.width
            - (self.padding * 2)
            - self.item_spacing * (len(labels) - 1)
        )
        item_width = available_width / len(labels)

        left = self.container_rect.left + self.padding
        self.items = []
        for index, label in enumerate(labels):
            width = item_width
            if index == len(labels) - 1:
                right_edge = self.container_rect.left + self.container_rect.width - self.padding
                width = right_edge - left
            rect = pygame.Rect(
                int(round(left)),
                int(round(items_top)),
                max(1, int(round(width))),
                items_height,
            )
            item = _SelectablePanelItem(
                rect=rect,
                label=label,
                display_height=self.display_height,
                font_name=self.font_name,
                font_size=self.item_font_size,
                base_color=(32, 52, 84, 240),
                highlight_color=(96, 176, 255, 255),
                border_color=(68, 104, 164, 255),
                glow_color=(88, 168, 255, 180),
                accent_color=(250, 255, 255, 160),
                text_color=self.text_color,
                index_badge=index + 1,
            )
            self.items.append(item)
            left += width + self.item_spacing

        self.slot_rects = [item.rect.copy() for item in self.items]
        self._apply_layout()

        self.selected_index = None
        self.selected_item = None
        self.swap_candidate_index = None
        if self.items:
            self._select_index(0, play_feedback=False, notify=False)

    def _apply_layout(self):
        for slot_rect, item in zip(self.slot_rects, self.items):
            item.rect = slot_rect.copy()

    def _handle_click(self, index):
        if self.swap_candidate_index is None:
            self._select_index(index)
            self.swap_candidate_index = index
            return

        if index == self.swap_candidate_index:
            self.items[index].trigger_feedback()
            self.swap_candidate_index = None
            return

        if index < 0 or index >= len(self.items):
            return

        target_item = self.items[index]
        self._swap_items(self.swap_candidate_index, index)

        new_target_index = self.items.index(target_item)
        self._select_index(new_target_index)
        self.swap_candidate_index = None

    def _swap_items(self, index_a, index_b):
        if index_a == index_b:
            return
        self.items[index_a], self.items[index_b] = self.items[index_b], self.items[index_a]
        self._apply_layout()

    def _clear_selection(self):
        if self.selected_item is not None:
            self.selected_item.set_selected(False)
        self.selected_item = None
        self.selected_index = None

    def _select_index(self, index, *, play_feedback=True, notify=True):
        if index is None:
            self._clear_selection()
            return
        if index < 0 or index >= len(self.items):
            return

        new_item = self.items[index]
        if self.selected_item is new_item and self.selected_index == index:
            if play_feedback:
                new_item.trigger_feedback()
            return

        if self.selected_item is not None:
            self.selected_item.set_selected(False)

        self.selected_item = new_item
        self.selected_index = index
        self.selected_item.set_selected(True, play_feedback=play_feedback)

        if notify and self.on_select:
            self.on_select(index, self.selected_item.label)

    def handle_event(self, event):
        handled = False
        if event.type == pygame.MOUSEMOTION:
            for item in self.items:
                item.set_hovered(item.rect.collidepoint(event.pos))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for index, item in enumerate(self.items):
                if item.rect.collidepoint(event.pos):
                    self._handle_click(index)
                    handled = True
                    break
        return handled

    def update(self, delta_time):
        for item in self.items:
            if not item.is_selected and not item.hovered:
                item.target_highlight = 0.0
            item.update(delta_time)

    def draw(self):
        shadow_rect = self.container_rect.copy()
        shadow_rect.move_ip(0, 8)
        glColor4f(
            self.shadow_color[0],
            self.shadow_color[1],
            self.shadow_color[2],
            self.shadow_color[3] * 0.2,
        )
        draw_pyrect(shadow_rect)

        glBegin(GL_QUADS)
        top_color = _brighten(self.container_color, 0.05)
        bottom_color = _darken(self.container_color, 0.04)
        glColor4f(*top_color)
        glVertex2f(self.container_rect.left, self.container_rect.top)
        glColor4f(*top_color)
        glVertex2f(self.container_rect.right, self.container_rect.top)
        glColor4f(*bottom_color)
        glVertex2f(self.container_rect.right, self.container_rect.bottom)
        glColor4f(*bottom_color)
        glVertex2f(self.container_rect.left, self.container_rect.bottom)
        glEnd()

        glColor4f(*self.container_border_color)
        draw_pyrect_border(self.container_rect)

        title_center_y = (
            self.container_rect.top
            + self.padding
            + self.title_margin
            + (self.item_font_size * 0.5)
        )
        title_window_y = self.display_height - title_center_y
        TextUtil.draw_text_2d(
            self.container_rect.centerx,
            title_window_y,
            self.title,
            font_name=self.font_name,
            size=int(self.item_font_size * 0.9),
            center=True,
            color=self.text_color,
        )

        for item in self.items:
            item.draw()

        if self.selected_item is not None:
            caption_text = f"Seleccionado: {self.selected_item.label}"
        else:
            caption_text = "Seleccionado: Ninguno"
        caption_center_y = (
            self.container_rect.bottom
            - self.padding
            - (self.caption_font_size * 0.5)
        )
        TextUtil.draw_text_2d(
            self.container_rect.centerx,
            self.display_height - caption_center_y,
            caption_text,
            font_name=self.font_name,
            size=self.caption_font_size,
            center=True,
            color=self.caption_color,
        )

    def focus_previous(self):
        if not self.items:
            return
        if self.selected_index is None:
            self._select_index(0, play_feedback=False, notify=False)
            return
        new_index = (self.selected_index - 1) % len(self.items)
        self._select_index(new_index, play_feedback=False, notify=False)

    def focus_next(self):
        if not self.items:
            return
        if self.selected_index is None:
            self._select_index(0, play_feedback=False, notify=False)
            return
        new_index = (self.selected_index + 1) % len(self.items)
        self._select_index(new_index, play_feedback=False, notify=False)

    def confirm_focus(self):
        if not self.items:
            return
        if self.selected_index is None:
            self._select_index(0, play_feedback=False, notify=False)
        if self.selected_index is not None:
            self._handle_click(self.selected_index)

    def set_selected_index(self, index):
        if index is None:
            self._clear_selection()
            self.swap_candidate_index = None
            return
        if 0 <= index < len(self.items):
            self._select_index(index)
            self.swap_candidate_index = index

    def get_selected_index(self):
        return self.selected_index

    def get_selected_label(self):
        return self.selected_item.label if self.selected_item is not None else None
