import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from systems.data_manager import DataManager
from systems.input_manager import InputManager
from systems.texture_manager import TextureManager
import utilities.text_renderer as TextUtil
import utilities.basic_objects as Objects
from game_objects.ui_elements.menu_button import MenuButton
from game_objects.ui_elements.animated_selection_panel import AnimatedSelectionPanel
from utilities.instructions_overlay import draw_instructions
from states.base_state import BaseState

class MenuState(BaseState):
    """
    Estado del Menú Principal. Dibuja UI en 2D y maneja
    la navegación del menú (Iniciar Juego, Salir).
    """
    def __init__(self, engine):
        super().__init__(engine)
        self.engine = engine
        self.input_manager = InputManager.instance()
        data_manager = DataManager.instance()
        texture_manager = TextureManager.instance()
        config = data_manager.get_config()

        display_config = config.get("rendered_display", {})
        display_width = display_config.get("width", 1280)
        display_height = display_config.get("height", 720)
        self.display_width = display_width
        self.display_height = display_height
        
        data_menu = data_manager.get_text_dict().get("menu_state", {})
        text_start_button = data_menu.get("start_button", "Jugar")
        text_exit_button = data_menu.get("exit_button", "Salir")
        
        self.texture_background = texture_manager.load_texture(
            "title-background", 
            "assets/background/proyecto-rxj-title.png"
            )
        self.background_image = pygame.Rect(0, 0, display_width, display_height)
        
        margin_display = 100
        btn_width, btn_height = 300, 55
        btn_x = display_width - btn_width - margin_display
        
        btn_y_exit = display_height - btn_height - margin_display
        btn_y_start = btn_y_exit - btn_height - 20

        # Colores
        button_color = (90, 130, 70, 255) # Verde
        button_hover_color = (110, 150, 90, 255) # Verde claro
        button_border_color = (110, 150, 90, 255) # Verde claro
        button_text_color = (255, 255, 255, 255) # Blanco
        
        montserrat_font = "montserrat_bold"
        #default_font = TextUtil.DEFAULT_FONT_NAME

        self.start_button = MenuButton(
            pos_x=btn_x, 
            pos_y=btn_y_start,
            width=btn_width,
            height=btn_height,
            color=button_color,
            hover_color=button_hover_color,
            border_color=button_border_color,
            text=text_start_button,
            text_font=montserrat_font,
            text_size=24,
            text_color=button_text_color
            )
        
        self.exit_button = MenuButton(
            pos_x=btn_x, 
            pos_y=btn_y_exit,
            width=btn_width,
            height=btn_height,
            color=button_color,
            hover_color=button_hover_color,
            border_color=button_border_color,
            text=text_exit_button,
            text_font=montserrat_font,
            text_size=24,
            text_color=button_text_color
            )
        
        self.selected_button = self.start_button
        self.selected_button.set_selected(True)

        panel_title = data_menu.get("highlight_title", "Destacados")
        panel_labels = list(data_menu.get("highlight_options", [
            "Explorar",
            "Desafios",
            "Galeria",
        ]))
        while len(panel_labels) < 3:
            panel_labels.append(f"Opcion {len(panel_labels) + 1}")
        panel_labels = tuple(panel_labels[:3])

        panel_width = int(display_width * 0.4)
        panel_height = int(display_height * 0.55)
        panel_margin = 60
        panel_x = panel_margin
        panel_y = display_height - panel_height - panel_margin

        self.selection_panel = AnimatedSelectionPanel(
            topleft=(panel_x, panel_y),
            size=(panel_width, panel_height),
            labels=panel_labels,
            title=panel_title,
            on_select=self._on_panel_selected,
        )
        self._highlight_label = self.selection_panel.get_selected_label()

        self.instructions_lines = [
            "Enter: Confirmar botón seleccionado",
            "Esc: Salir del juego",
            "Flechas Arriba/Abajo: Cambiar botón",
            "A/D: Cambiar panel destacado",
            "S (dos veces): Intercambiar panel destacado",
        ]
        
        print("MenuState inicializado.")
        print("  -> Usa las flechas para navegar y ENTER para seleccionar.")

    def _on_panel_selected(self, index, label):
        self._highlight_label = label
        print(f"Panel destacado seleccionado ({index}): {label}")

    def update(self, delta_time, event_list):
        from states.player_selection_state import PlayerSelectionState
        
        # Manejo de eventos de teclado
        if self.input_manager.was_action_pressed("quit"):
            self.engine.pop_state()
        elif self.input_manager.was_action_pressed("ui_up"):
            self._toogle_selected_button()
        elif self.input_manager.was_action_pressed("ui_down"):
            self._toogle_selected_button()
        elif self.input_manager.was_action_pressed("ui_select"):
            if self.selected_button == self.start_button:
                self.engine.push_state(PlayerSelectionState(self.engine))
            else:
                self.engine.pop_state()

        if self.input_manager.was_action_pressed("panel_left"):
            self.selection_panel.focus_previous()
        if self.input_manager.was_action_pressed("panel_right"):
            self.selection_panel.focus_next()
        if self.input_manager.was_action_pressed("panel_select"):
            self.selection_panel.confirm_focus()

        self.selection_panel.update(delta_time)

    def _toogle_selected_button(self):
        if self.start_button.is_selected:
            self.start_button.set_selected(False)
            self.exit_button.set_selected(True)
            self.selected_button = self.exit_button
        elif self.exit_button.is_selected:
            self.exit_button.set_selected(False)
            self.start_button.set_selected(True)
            self.selected_button = self.start_button
        else:
            self.exit_button.set_selected(False)
            self.start_button.set_selected(True)
            self.selected_button = self.start_button

    def draw(self):
        """Dibuja la UI en 2D."""
        glClearColor(0, 0, 0, 255)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.engine.setup_2d_orthographic()
        glColor3f(1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glBindTexture(GL_TEXTURE_2D, self.texture_background)
        Objects.draw_crop_pyrect(self.background_image, 1344, 768)
        glDisable(GL_TEXTURE_2D)

        self.selection_panel.draw()
        self.start_button.draw()
        self.exit_button.draw()
        draw_instructions(self.display_width, self.display_height, self.instructions_lines)
