import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import utilities.text_renderer as TextUtil
from utilities.basic_objects import draw_pyrect, draw_pyrect_border
from states.base_state import BaseState
from systems.input_manager import InputManager

class MenuState(BaseState):
    """
    Estado del Menú Principal. Dibuja UI en 2D y maneja
    la navegación del menú (Iniciar Juego, Salir).
    """
    
    def __init__(self, engine):
        super().__init__(engine)
        self.engine = engine
        self.input_manager = InputManager.instance()
        
        self.display_width, self.display_height = 800, 600
        
        # Configuración de botones
        btn_width, btn_height = 200, 50
        btn_x = (self.display_width - btn_width) / 2
        
        self.start_button = pygame.Rect(btn_x, 250, btn_width, btn_height)
        self.exit_button = pygame.Rect(btn_x, 360, btn_width, btn_height)
        self.selected_button = self.start_button
        
        # Colores
        self.clear_color = (0, 0, 0, 255) # Negro
        self.title_color = (255, 255, 255, 255) # Blanco
        self.button_text_color = (255, 255, 255) # Blanco
        self.button_color = (0.0, 0.6, 0.0) # Verde
        self.button_hover_color = (0.2, 0.8, 0.2) # Verde claro
        self.button_exit_color = (0.6, 0.0, 0.0) # Rojo
        self.button_exit_hover_color = (0.8, 0.2, 0.2) # Rojo claro
        
        self.montserrat_font = "montserrat_bold"
        self.default_font = TextUtil.DEFAULT_FONT_NAME
        
        print("MenuState inicializado.")
        print("  -> Usa las flechas para navegar y ENTER para seleccionar.")
        print("  -> Haz clic en los botones con el mouse.")

    def update(self, _delta_time, event_list):
        from states.player_selection_state import PlayerSelectionState
        
        # Manejo de eventos de teclado
        if self.input_manager.was_action_pressed("quit"):
            self.engine.pop_state()
        elif self.input_manager.was_action_pressed("ui_up"):
            self.selected_button = self.start_button
        elif self.input_manager.was_action_pressed("ui_down"):
            self.selected_button = self.exit_button
        elif self.input_manager.was_action_pressed("ui_select"):
            if self.selected_button == self.start_button:
                self.engine.push_state(PlayerSelectionState(self.engine))
            else:
                self.engine.pop_state()

        # Manejo de eventos de mouse
        mouse_pos = pygame.mouse.get_pos()
        
        # Actualizar botón seleccionado por mouse hover
        if self.start_button.collidepoint(mouse_pos):
            self.selected_button = self.start_button
        elif self.exit_button.collidepoint(mouse_pos):
            self.selected_button = self.exit_button
            
        # Manejo de clics del mouse
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic izquierdo
                    if self.start_button.collidepoint(event.pos):
                        self.engine.push_state(PlayerSelectionState(self.engine))
                    elif self.exit_button.collidepoint(event.pos):
                        self.engine.pop_state()

    def draw(self):
        """Dibuja la UI en 2D."""
        glClearColor(*self.clear_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.engine.setup_2d_orthographic()
        
        # Dibujar título
        TextUtil.draw_text_2d(400, 200, "The Mansion Riddle", self.montserrat_font, size=56, center=True, color=self.title_color)
        
        # Dibujar botón Iniciar
        glColor3fv(self.button_color)
        if self.selected_button == self.start_button:
            glColor3f(*self.button_hover_color)
        draw_pyrect(self.start_button)
        
        # Dibujar botón Salir
        glColor3f(*self.button_exit_color)
        if self.selected_button == self.exit_button:
            glColor3f(*self.button_exit_hover_color)
        draw_pyrect(self.exit_button)
        
        # Dibujar bordes de los botones
        glColor3f(1.0, 1.0, 1.0)
        draw_pyrect_border(self.start_button)
        draw_pyrect_border(self.exit_button)
        
        # Dibujar texto en los botones
        TextUtil.draw_text_2d(self.start_button.centerx, self.start_button.centery, 
                       "Jugar", self.montserrat_font, size=30, center=True, color=self.button_text_color)
        TextUtil.draw_text_2d(self.exit_button.centerx, self.exit_button.centery, 
                       "Salir", self.montserrat_font, size=30, center=True, color=self.button_text_color)
        
        # Dibujar instrucciones
        TextUtil.draw_text_2d(400, 460, "Usa las flechas o el mouse para navegar", 
                       self.default_font, size=24, center=True, color=self.button_text_color)
        TextUtil.draw_text_2d(400, 490, "Presiona ENTER o haz clic para seleccionar", 
                       self.default_font, size=24, center=True, color=self.button_text_color)
