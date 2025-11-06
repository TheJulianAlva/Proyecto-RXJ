# engine.py
from states.play_state import PlayState
from states.menu_state import MenuState
from OpenGL.GL import *
from OpenGL.GLU import *

class GameEngine:
    def __init__(self):
        self.running = True
        self.state_stack = []
        self.push_state(MenuState(self))
        
        print("GameEngine inicializado.")

    def update(self, delta_time, event_list):
        if self.state_stack:
            self.state_stack[-1].update(delta_time, event_list)

    def draw(self):
        if self.state_stack:
            self.state_stack[-1].draw()

    def push_state(self, state_instance):
        """
        Añade un estado a la CIMA de la pila (ej. abrir Menú de Pausa).
        El nuevo estado se vuelve el activo.
        """
        print(f"GameEngine: Pushing state -> {state_instance.__class__.__name__}")
        self.state_stack.append(state_instance)

    def pop_state(self):
        """
        Quita el estado de la CIMA de la pila (ej. cerrar Menú de Pausa).
        El estado anterior se vuelve el activo.
        """
        if self.state_stack:
            print(f"GameEngine: Popping state -> {self.state_stack[-1].__class__.__name__}")
            self.state_stack.pop()
        # Corregir funcionamiento
        # Si la pila queda vacía, salimos del juego
        #if not self.state_stack:
        #    self.running = False

    def change_state(self, state_instance):
        """
        Reemplaza el estado de la CIMA por uno nuevo (ej. Menú -> Juego).
        Es un 'pop' seguido de un 'push'.
        """
        self.pop_state()
        self.push_state(state_instance)


    def setup_perspective(self):
        """
        Configura la proyección de perspectiva 3D.
        (Lo llamaremos desde PlayState cuando se active)
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (800 / 600), 0.1, 50.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def quit_game(self):
        self.running = False