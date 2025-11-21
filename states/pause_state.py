import pygame
from OpenGL.GL import *
from states.base_state import BaseState
from game_objects.ui_elements.menu_button import MenuButton
from systems.audio_manager import AudioManager
from systems.data_manager import DataManager
import utilities.basic_objects as Objects
import utilities.text_renderer as TextUtil


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

        # Ventana de pausa centrada
        self.window_w = 520
        self.window_h = 260
        self.window_x = (self.display_width - self.window_w) // 2
        self.window_y = (self.display_height - self.window_h) // 2

        # Slider de volumen (track dentro de la ventana)
        self.track_margin = 40
        self.track_w = self.window_w - self.track_margin * 2
        self.track_h = 10
        self.track_x = self.window_x + self.track_margin
        self.track_y = self.window_y + 80

        # Knob
        self.knob_w = 14
        self.knob_h = 24
        self.dragging = False

        # Resume button (usar MenuButton para consistencia)
        # Hacerlo más pequeño según petición
        btn_w, btn_h = 140, 40
        btn_x = self.window_x + (self.window_w - btn_w) // 2
        btn_y = self.window_y + self.window_h - btn_h - 24
        self.resume_button = MenuButton(pos_x=(self.window_x + self.window_w // 2)-50, pos_y=350, width=btn_w, height=btn_h,
                                        text="Reanudar", text_font="montserrat_bold", text_size=24,
                                        color=(70, 70, 70, 255), hover_color=(90, 90, 90, 255), border_color=(255,255,255,255))

        # Estado inicial del knob basado en volumen actual
        vol = self.audio.get_volume()
        self.knob_x = self.track_x + int(vol * self.track_w) - self.knob_w // 2

    def update(self, delta_time, event_list):
        # Procesar entrada: teclas y ratón
        for ev in event_list:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_p or ev.key == pygame.K_ESCAPE:
                    # Reanudar: quitar este estado
                    self.engine.pop_state()
                    return

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                # Comprobar click en resume_button
                bx, by, bw, bh = self.resume_button.rect.left, self.resume_button.rect.top, self.resume_button.rect.width, self.resume_button.rect.height
                if bx <= mx <= bx + bw and by <= my <= by + bh:
                    self.engine.pop_state()
                    return

                # Comprobar inicio drag en el track or knob
                if (self.track_x <= mx <= self.track_x + self.track_w) and (self.track_y - 10 <= my <= self.track_y + self.track_h + 10):
                    self.dragging = True
                    self._update_volume_by_mouse(mx)

            if ev.type == pygame.MOUSEMOTION and self.dragging:
                mx, my = ev.pos
                self._update_volume_by_mouse(mx)

            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1 and self.dragging:
                self.dragging = False

        # Actualizar estado visual del botón (hover) según mouse actual
        mx, my = pygame.mouse.get_pos()
        # Actualizar selección de MenuButton: set_selected si hover
        # MenuButton expects top-left Y coordinate; rect is available.
        # Hacer simple hover detection
        bx, by = self.resume_button.rect.left, self.resume_button.rect.top
        if bx <= mx <= bx + self.resume_button.rect.width and by <= my <= by + self.resume_button.rect.height:
            self.resume_button.set_selected(True)
        else:
            self.resume_button.set_selected(False)

    def _update_volume_by_mouse(self, mx):
        # Clamp mouse to track
        rel_x = max(self.track_x, min(self.track_x + self.track_w, mx))
        t = (rel_x - self.track_x) / float(self.track_w)
        # Update knob position
        self.knob_x = int(self.track_x + t * self.track_w) - self.knob_w // 2
        # Set audio volume
        self.audio.set_volume(t)

    def draw(self):
        # Dibujar overlay semitransparente
        self.engine.setup_2d_orthographic()
        glColor4f(0.0, 0.0, 0.0, 0.6)
        overlay_rect = pygame.Rect(0, 0, self.display_width, self.display_height)
        Objects.draw_pyrect(overlay_rect)

        # Dibujar ventana central
        glColor4f(0.12, 0.12, 0.12, 0.95)
        win_rect = pygame.Rect(self.window_x, self.window_y, self.window_w, self.window_h)
        Objects.draw_pyrect(win_rect)

        # Título
        TextUtil.draw_text_2d(self.window_x + self.window_w // 2, self.window_y + 30, "Pausa",
                              font_name="montserrat_bold", size=32, center=True, color=(255,255,255,255))

        # Dibujar slider track
        glColor4f(0.4, 0.4, 0.4, 1.0)
        track_rect = pygame.Rect(self.track_x, self.track_y, self.track_w, self.track_h)
        Objects.draw_pyrect(track_rect)

        # Texto del slider
        TextUtil.draw_text_2d(self.track_x + self.track_w // 2, self.track_y + 120, "Volumen",
                      font_name="montserrat_bold", size=20, center=True, color=(255,255,255,255))

        # Dibujar knob
        glColor4f(0.9, 0.9, 0.9, 1.0)
        knob_rect = pygame.Rect(self.knob_x, self.track_y - (self.knob_h - self.track_h)//2, self.knob_w, self.knob_h)
        Objects.draw_pyrect(knob_rect)

        # Mostrar valor de volumen al lado
        vol = int(self.audio.get_volume() * 100)
        TextUtil.draw_text_2d(self.track_x + self.track_w + 30, self.track_y + self.track_h // 2, f"{vol}%",
                              font_name="montserrat_bold", size=20, center=True, color=(255,255,255,255))

        # Dibujar botón Reanudar
        self.resume_button.draw()
