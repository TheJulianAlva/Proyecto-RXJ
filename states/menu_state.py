import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
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
        
        # Configuración de la pantalla
        self.display_width, self.display_height = 800, 600
        
        # Configuración de botones
        btn_width, btn_height = 200, 50
        btn_x = (self.display_width - btn_width) / 2
        
        self.start_button = pygame.Rect(btn_x, 250, btn_width, btn_height)
        self.exit_button = pygame.Rect(btn_x, 360, btn_width, btn_height)
        self.selected_button = self.start_button
        
        # Colores
        self.clear_color = (0.0, 0.0, 0.0 , 1.0)  # Fondo más oscuro para mejor contraste
        self.title_color = (1.0, 1.0, 1.0, 1.0)  # Color amarillo para el título
        self.button_color = (0.0, 0.6, 0.0)      # Verde más brillante
        self.button_hover_color = (0.2, 0.8, 0.2) # Verde más claro para hover
        self.button_exit_color = (0.6, 0.0, 0.0)  # Rojo más brillante
        self.button_exit_hover_color = (0.8, 0.2, 0.2) # Rojo más claro para hover
        self.button_text_color = (1.0, 1.0, 1.0)  # Texto blanco en botones
        
        # Fuentes
        self.font_title = pygame.font.Font("fonts/Montserrat-master/Montserrat-master/fonts-underline/ttf/MontserratUnderline-Bold.ttf", 56)  # Fuente más grande para el título
        self.font_button = pygame.font.Font("fonts/Montserrat-master/Montserrat-master/fonts-underline/ttf/MontserratUnderline-Bold.ttf", 32) # Fuente para botones
        
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
        self._draw_text(400, 200, "The Mansion Riddle", self.font_title, center=True, color=self.title_color)
        
        # Dibujar botón Iniciar
        if self.selected_button == self.start_button:
            glColor3f(*self.button_hover_color)
        else:
            glColor3f(*self.button_color)
        self._draw_rect(self.start_button)
        
        # Dibujar botón Salir
        if self.selected_button == self.exit_button:
            glColor3f(*self.button_exit_hover_color)
        else:
            glColor3f(*self.button_exit_color)
        self._draw_rect(self.exit_button)
        
        # Dibujar bordes de los botones
        glColor3f(1.0, 1.0, 1.0)
        self._draw_rect_border(self.start_button)
        self._draw_rect_border(self.exit_button)
        
        # Dibujar texto en los botones
        self._draw_text(self.start_button.centerx, self.start_button.centery -10, 
                       "JUGAR", self.font_button, center=True, color=self.button_text_color)
        self._draw_text(self.exit_button.centerx, self.exit_button.centery -10, 
                       "SALIR", self.font_button, center=True, color=self.button_text_color)
        
        # Dibujar instrucciones
        self._draw_text(400, 460, "Usa las flechas o el mouse para navegar", 
                       pygame.font.Font(None, 24), center=True, color=(0.8, 0.8, 0.8))
        self._draw_text(400, 490, "Presiona ENTER o haz clic para seleccionar", 
                       pygame.font.Font(None, 24), center=True, color=(0.8, 0.8, 0.8))

    def _draw_rect(self, rect):
        """
        Función para dibujar un pygame.Rect relleno con GL_QUADS.

        :param rect: El rectángulo a dibujar.
        :type rect: pygame.Rect
        """
        glBegin(GL_QUADS)
        glVertex2f(rect.left, rect.top)
        glVertex2f(rect.right, rect.top)
        glVertex2f(rect.right, rect.bottom)
        glVertex2f(rect.left, rect.bottom)
        glEnd()

    def _draw_rect_border(self, rect):
        """
        Función para dibujar el borde de un pygame.Rect con GL_LINES.

        :param rect: El rectángulo cuyo borde se va a dibujar.
        :type rect: pygame.Rect
        """
        glLineWidth(2.0)  # Hacer el borde más grueso
        glBegin(GL_LINE_LOOP)
        glVertex2f(rect.left, rect.top)
        glVertex2f(rect.right, rect.top)
        glVertex2f(rect.right, rect.bottom)
        glVertex2f(rect.left, rect.bottom)
        glEnd()
        glLineWidth(1.0)  # Restaurar grosor de línea por defecto

    def _draw_text(self, x, y, text_string, font, center=False, color=(1.0, 1.0, 1.0)):
        """
        Renderiza una cadena de texto de Pygame en la pantalla de OpenGL.

        :param x: La coordenada X (posición raster) donde comenzará el texto.
        :type x: int | float
        :param y: La coordenada Y (posición raster) donde comenzará el texto.
        :type y: int | float
        :param text_string: La cadena de texto a renderizar.
        :type text_string: str
        :param font: El objeto de fuente de Pygame a utilizar.
        :type font: pygame.font.Font
        :param center: Si es True, centra el texto en las coordenadas x,y.
        :type center: bool
        :param color: Color del texto en formato RGB (valores de 0.0 a 1.0).
        :type color: tuple
        """
        # Convertir color de OpenGL (0-1) a Pygame (0-255)
        pygame_color = tuple(int(c * 255) for c in color)
        
        text_surface = font.render(text_string, True, pygame_color, (0, 0, 0, 0))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        width, height = text_surface.get_size()
        
        # Ajustar posición si se solicita centrado
        if center:
            x -= width / 2
            y -= height / 2
            
        glRasterPos2f(x, y)
        glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)