import math
import pygame
from OpenGL.GL import *
from states.base_state import BaseState
from game_objects.ui_elements.menu_button import MenuButton
from systems.audio_manager import AudioManager
from systems.data_manager import DataManager
import utilities.basic_objects as Objects
import utilities.text_renderer as TextUtil
from utilities.instructions_overlay import draw_instructions
from states.menu_state import MenuState


def _clamp(value, low, high):
    return max(low, min(high, value))


class PauseState(BaseState):
    def __init__(self, engine):
        super().__init__(engine)
        self.engine = engine
        self.input_manager = __import__('systems.input_manager', fromlist=['']).InputManager.instance()
        self.audio = AudioManager.instance()

        data_manager = DataManager.instance()
        display_config = data_manager.get_config().get("rendered_display", {})
        self.display_width = display_config.get("width", 1280)
        self.display_height = display_config.get("height", 720)

        base_width = min(int(self.display_width * 0.52), 720)
        base_height = min(int(self.display_height * 0.62), 420)
        self._window_rect_base = pygame.Rect(
            (self.display_width - base_width) // 2,
            (self.display_height - base_height) // 2,
            base_width,
            base_height,
        )

        self.header_height = int(base_height * 0.27)
        self.content_padding = 28
        self.volume_card_height = 140
        self.track_height = 10
        self.track_margin = 42
        self.knob_size = (20, 30)

        self._volume_card_rect_base = pygame.Rect(
            self._window_rect_base.left + 36,
            self._window_rect_base.top + self.header_height + self.content_padding,
            self._window_rect_base.width - 72,
            self.volume_card_height,
        )

        track_width = max(60, self._volume_card_rect_base.width - self.track_margin * 2)
        track_y = self._volume_card_rect_base.top + int(self.volume_card_height * 0.58)
        self._track_rect_base = pygame.Rect(
            self._volume_card_rect_base.left + self.track_margin,
            track_y,
            track_width,
            self.track_height,
        )

        btn_width, btn_height = 210, 52
        btn_gap = 24
        btn_y = self._window_rect_base.bottom - btn_height - 30
        center_x = self._window_rect_base.centerx

        resume_x = center_x - btn_gap // 2 - btn_width
        exit_x = center_x + btn_gap // 2

        self.resume_button = MenuButton(
            pos_x=resume_x,
            pos_y=btn_y,
            width=btn_width,
            height=btn_height,
            text="Reanudar",
            text_font="montserrat_bold",
            text_size=26,
            color=(68, 124, 86, 255),
            hover_color=(98, 154, 116, 255),
            border_color=(180, 224, 188, 255),
            text_color=(255, 255, 255, 255),
        )

        self.exit_button = MenuButton(
            pos_x=exit_x,
            pos_y=btn_y,
            width=btn_width,
            height=btn_height,
            text="Salir al menu",
            text_font="montserrat_bold",
            text_size=26,
            color=(84, 92, 132, 255),
            hover_color=(114, 122, 162, 255),
            border_color=(194, 198, 236, 255),
            text_color=(255, 255, 255, 255),
        )

        self._resume_rect_base = self.resume_button.rect.copy()
        self._exit_rect_base = self.exit_button.rect.copy()

        self.overlay_alpha = 0.0
        self.window_offset = 36.0
        self.glow_timer = 0.0

        self.volume_amount = _clamp(self.audio.get_volume(), 0.0, 1.0)
        self._layout = None

        self.buttons = [self.resume_button, self.exit_button]
        self.button_focus_index = 0
        self._apply_button_focus()

        self.instructions_lines = [
            "Esc: Reanudar",
            "A/D: Ajustar volumen",
            "Flechas Arriba/Abajo: Cambiar botón",
            "Enter o S: Activar opción",
        ]

    def update(self, delta_time, event_list):
        self.overlay_alpha = _clamp(self.overlay_alpha + delta_time * 3.5, 0.0, 0.7)
        self.window_offset = max(0.0, self.window_offset - delta_time * 120.0)
        self.glow_timer = (self.glow_timer + delta_time * 1.2) % 1.0

        layout = self._compute_layout()
        self._apply_button_focus()

        if self.input_manager.was_action_pressed("pause"):
            self.engine.pop_state()
            return

        if (
            self.input_manager.was_action_pressed("ui_up")
            or self.input_manager.was_action_pressed("ui_down")
        ):
            self.button_focus_index = (self.button_focus_index + 1) % len(self.buttons)
            self._apply_button_focus()

        if self.input_manager.was_action_pressed("panel_left"):
            self._adjust_volume(-0.05)
            layout = self._compute_layout()
            self._apply_button_focus()

        if self.input_manager.was_action_pressed("panel_right"):
            self._adjust_volume(0.05)
            layout = self._compute_layout()
            self._apply_button_focus()

        if self.input_manager.was_action_pressed("ui_select") or self.input_manager.was_action_pressed("panel_select"):
            if self.button_focus_index == 0:
                self.engine.pop_state()
            else:
                self._exit_to_menu()

    def _compute_layout(self):
        offset = int(round(self.window_offset))
        window_rect = self._window_rect_base.move(0, offset)
        header_rect = pygame.Rect(window_rect.left, window_rect.top, window_rect.width, self.header_height)
        volume_card_rect = self._volume_card_rect_base.move(0, offset)
        track_rect = self._track_rect_base.move(0, offset)
        track_rect.width = max(track_rect.width, 1)

        knob_width, knob_height = self.knob_size
        knob_center_x = int(track_rect.left + self.volume_amount * track_rect.width)
        knob_rect = pygame.Rect(
            knob_center_x - knob_width // 2,
            track_rect.centery - knob_height // 2,
            knob_width,
            knob_height,
        )

        resume_rect = self._resume_rect_base.move(0, offset)
        exit_rect = self._exit_rect_base.move(0, offset)
        self._assign_button_rect(self.resume_button, resume_rect)
        self._assign_button_rect(self.exit_button, exit_rect)

        layout = {
            "window_rect": window_rect,
            "header_rect": header_rect,
            "volume_card_rect": volume_card_rect,
            "track_rect": track_rect,
            "track_hit_rect": track_rect.inflate(0, 28),
            "knob_rect": knob_rect,
            "resume_rect": resume_rect,
            "exit_rect": exit_rect,
        }
        self._layout = layout
        return layout

    def _assign_button_rect(self, button, rect):
        button.rect = rect
        button.text_pos_y = self.display_height - rect.y - rect.height / 2

    def _apply_button_focus(self):
        for index, button in enumerate(self.buttons):
            button.set_selected(index == self.button_focus_index)

    def _adjust_volume(self, delta):
        self.volume_amount = _clamp(self.volume_amount + delta, 0.0, 1.0)
        self.audio.set_volume(self.volume_amount)
        self._compute_layout()

    def _exit_to_menu(self):
        self.engine.pop_state()
        while self.engine.state_stack and not isinstance(self.engine.state_stack[-1], MenuState):
            self.engine.pop_state()
        if not self.engine.state_stack:
            self.engine.push_state(MenuState(self.engine))

    def draw(self):
        layout = self._compute_layout() if self._layout is None else self._layout
        window_rect = layout["window_rect"]
        header_rect = layout["header_rect"]
        volume_card_rect = layout["volume_card_rect"]
        track_rect = layout["track_rect"]
        knob_rect = layout["knob_rect"]

        self.engine.setup_2d_orthographic()

        glColor4f(0.0, 0.0, 0.0, self.overlay_alpha)
        Objects.draw_pyrect(pygame.Rect(0, 0, self.display_width, self.display_height))

        glBegin(GL_QUADS)
        glColor4f(0.08, 0.11, 0.17, 0.95)
        glVertex2f(window_rect.left, window_rect.top)
        glVertex2f(window_rect.right, window_rect.top)
        glColor4f(0.05, 0.07, 0.11, 0.95)
        glVertex2f(window_rect.right, window_rect.bottom)
        glVertex2f(window_rect.left, window_rect.bottom)
        glEnd()

        glColor4f(0.18, 0.24, 0.32, 0.85)
        Objects.draw_pyrect_border(window_rect)

        glBegin(GL_QUADS)
        glColor4f(0.12, 0.17, 0.25, 0.96)
        glVertex2f(header_rect.left, header_rect.top)
        glVertex2f(header_rect.right, header_rect.top)
        glColor4f(0.09, 0.13, 0.2, 0.96)
        glVertex2f(header_rect.right, header_rect.bottom)
        glVertex2f(header_rect.left, header_rect.bottom)
        glEnd()

        accent_width = int(window_rect.width * (0.42 + 0.18 * math.sin(self.glow_timer * math.tau)))
        accent_rect = pygame.Rect(
            window_rect.left + (window_rect.width - accent_width) // 2,
            header_rect.bottom - 8,
            accent_width,
            3,
        )
        glColor4f(0.32, 0.58, 0.88, 0.8)
        Objects.draw_pyrect(accent_rect)

        header_center_y = header_rect.top + header_rect.height // 2
        TextUtil.draw_text_2d(
            window_rect.centerx,
            self.display_height - header_center_y,
            "Pausa",
            font_name="montserrat_bold",
            size=48,
            center=True,
            color=(234, 242, 255, 255),
        )

        glBegin(GL_QUADS)
        glColor4f(0.11, 0.15, 0.22, 0.92)
        glVertex2f(volume_card_rect.left, volume_card_rect.top)
        glVertex2f(volume_card_rect.right, volume_card_rect.top)
        glColor4f(0.08, 0.11, 0.18, 0.92)
        glVertex2f(volume_card_rect.right, volume_card_rect.bottom)
        glVertex2f(volume_card_rect.left, volume_card_rect.bottom)
        glEnd()

        glColor4f(0.2, 0.27, 0.38, 0.78)
        Objects.draw_pyrect_border(volume_card_rect)

        volume_title_y = volume_card_rect.top + 32
        TextUtil.draw_text_2d(
            volume_card_rect.centerx,
            self.display_height - volume_title_y,
            "Volumen",
            font_name="montserrat_bold",
            size=26,
            center=True,
            color=(214, 226, 238, 255),
        )

        glBegin(GL_QUADS)
        glColor4f(0.22, 0.32, 0.48, 0.8)
        glVertex2f(track_rect.left, track_rect.top)
        glVertex2f(track_rect.right, track_rect.top)
        glColor4f(0.16, 0.24, 0.38, 0.8)
        glVertex2f(track_rect.right, track_rect.bottom)
        glVertex2f(track_rect.left, track_rect.bottom)
        glEnd()

        glow_rect = knob_rect.inflate(18, 12)
        pulse = 0.35 + 0.35 * math.sin(self.glow_timer * math.tau)
        glColor4f(0.35, 0.55, 0.85, 0.18 + 0.22 * pulse)
        Objects.draw_pyrect(glow_rect)

        glColor4f(0.76, 0.88, 0.97, 1.0)
        Objects.draw_pyrect(knob_rect)
        glColor4f(0.28, 0.4, 0.6, 0.9)
        Objects.draw_pyrect_border(knob_rect)

        volume_value_y = track_rect.bottom + 36
        volume_percent = int(round(self.volume_amount * 100.0))
        TextUtil.draw_text_2d(
            volume_card_rect.centerx,
            self.display_height - volume_value_y,
            f"{volume_percent}%",
            font_name="montserrat_bold",
            size=24,
            center=True,
            color=(214, 226, 238, 255),
        )

        self.resume_button.draw()
        self.exit_button.draw()
        draw_instructions(self.display_width, self.display_height, self.instructions_lines)
