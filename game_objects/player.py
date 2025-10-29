from OpenGL.GL import *
from systems.input_manager import InputManager
import math

class Player:
    def __init__(self, x, y, z):
        self.position = [x, y, z]
        self.rotation_y = 0.0
        self.movement_speed = 0.05
        self.rotate_speed = 2.5
        self.input_manager = InputManager.instance()

    def move(self, amount):
        rads = math.radians(self.rotation_y)
        #move_x = amount * math.sin(rads)
        #move_z = amount * math.cos(rads)
        self.position[0] += amount * math.sin(rads)
        self.position[2] += amount * math.cos(rads)

    def rotate(self, angle):
        self.rotation_y += angle
        if self.rotation_y > 360: self.rotation_y = 0

    def update(self, delta_time):
        """
        Aquí es donde el jugador reacciona a los inputs,
        frame por frame.
        """
        
        # --- Lógica de Movimiento ---
        
        if self.input_manager.is_action_held("move_forward"):
            self.move(self.movement_speed * delta_time) 
            
        if self.input_manager.is_action_held("move_backward"):
            self.move(-self.movement_speed * delta_time)
            
        if self.input_manager.is_action_held("rotate_left"):
            self.rotate(self.rotate_speed * delta_time)
            
        if self.input_manager.is_action_held("rotate_right"):
            self.rotate(-self.rotate_speed * delta_time)

        # --- Lógica de Interacción ---
        if self.input_manager.was_action_pressed("interact"):
            self._check_interaction()
    
    def _check_interaction(self):
        print("¡Jugador intentó interactuar!")
        pass


    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.rotation_y, 0, 1, 0)

        glColor3f(0.0, 0.5, 1.0)
        self._draw()
        glPopMatrix()

    def _draw(self):
        s = 0.5

        glBegin(GL_QUADS)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-s, -s,  s)
        glVertex3f( s, -s,  s)
        glVertex3f( s,  s,  s)
        glVertex3f(-s,  s,  s)
        
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(-s, -s, -s)
        glVertex3f(-s,  s, -s)
        glVertex3f( s,  s, -s)
        glVertex3f( s, -s, -s)
        
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(-s,  s, -s)
        glVertex3f(-s,  s,  s)
        glVertex3f( s,  s,  s)
        glVertex3f( s,  s, -s)
        
        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(-s, -s, -s)
        glVertex3f( s, -s, -s)
        glVertex3f( s, -s,  s)
        glVertex3f(-s, -s,  s)
        
        glColor3f(1.0, 0.0, 1.0)
        glVertex3f( s, -s, -s)
        glVertex3f( s,  s, -s)
        glVertex3f( s,  s,  s)
        glVertex3f( s, -s,  s)
        
        glColor3f(0.0, 1.0, 1.0)
        glVertex3f(-s, -s, -s)
        glVertex3f(-s, -s,  s)
        glVertex3f(-s,  s,  s)
        glVertex3f(-s,  s, -s)
        glEnd()