"""
Motor Principal del Juego (GameEngine)

Propósito:
Este módulo define la clase 'GameEngine', el cerebro que gestiona
el flujo general del juego.

Arquitectura de Pila de Estados (State Stack):
El motor no contiene lógica de juego, sino que administra una pila de
estados; esto permite apilar estados de forma natural,
como un 'PauseState' encima de un 'PlayState'.

El comportamiento del juego (actualización y dibujado) siempre es
delegado al estado que se encuentra en la CIMA de la pila.

Métodos de Control de la Pila:
- push_state(state):    Añade un estado a la cima (ej. pausar).
- pop_state():          Quita el estado de la cima (ej. reanudar).
- change_state(state):  Reemplaza el estado de la cima (ej. Menú -> Juego).

"""
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
        
        if not self.state_stack:
            self.running = False

    def change_state(self, state_instance):
        """
        Reemplaza el estado de la CIMA por uno nuevo (ej. Menú -> Juego).
        Es un 'pop' seguido de un 'push'.
        """
        self.pop_state()
        self.push_state(state_instance)

    def setup_3d_perspective(self):
        """
        Configura el pipeline de OpenGL para renderizado 3D
        con perspectiva, iluminación y test de profundidad.
        """
        glEnable(GL_LIGHTING)
        
        # Materiales: Permite que glColor3f afecte el material
        #glEnable(GL_COLOR_MATERIAL)
        #glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (800 / 600), 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def setup_2d_orthographic(self):
        """
        Configura el pipeline de OpenGL para renderizado 2D (UI)
        con vista ortográfica. Desactiva iluminación y profundidad.
        """
        
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, 800, 600, 0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def quit_game(self):
        self.running = False