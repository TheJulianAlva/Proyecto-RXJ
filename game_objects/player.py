from OpenGL.GL import *
from systems.input_manager import InputManager
from utilities import basic_objects as Objects
import math


class Player:
    def __init__(self, x, y, z, skin_class):
        self.position = [x, y, z]
        self.rotation_y = 0.0
        self.movement_speed = 9.0
        self.rotate_speed = 280
        self.input_manager = InputManager.instance()
        self.skin = skin_class()

        self.is_walking = False

    def move(self, amount):
        rads = math.radians(self.rotation_y)
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
        self.is_walking = False 
        
        if self.input_manager.is_action_held("move_forward"):
            self.move(self.movement_speed * delta_time)
            self.is_walking = True
            
        if self.input_manager.is_action_held("move_backward"):
            self.move(-self.movement_speed * delta_time)
            self.is_walking = True
            
        if self.input_manager.is_action_held("rotate_left"):
            self.rotate(self.rotate_speed * delta_time)
            
        if self.input_manager.is_action_held("rotate_right"):
            self.rotate(-self.rotate_speed * delta_time)

        # --- Lógica de Interacción ---
        if self.input_manager.was_action_pressed("interact"):
            self._check_interaction()

        if self.is_walking:
            self.skin.set_state("walk")
        else:
            self.skin.set_state("idle")
            
        if hasattr(self.skin, "update_animation"):
            self.skin.update_animation(delta_time)
        
    def _check_interaction(self):
        print("¡Jugador intentó interactuar!")
        pass

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.rotation_y, 0, 1, 0)
        self.skin.draw()
        glPopMatrix()
