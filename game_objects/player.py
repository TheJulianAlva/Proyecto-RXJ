from OpenGL.GL import *
from systems.input_manager import InputManager
from assets import basic_objects as Objects, materials as Materials
import math

class Player:
    def __init__(self, x, y, z):
        self.position = [x, y, z]
        self.rotation_y = 0.0
        self.movement_speed = 3.0
        self.rotate_speed = 150
        self.input_manager = InputManager.instance()

        # Variables de estado para la animación
        self.is_walking = False
        self.walking_animation_timer = 0.0      # Contador de tiempo para la animación
        self.walking_animation_speed = 6.0     # Qué tan rápido se mueven las piernas

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
            self.walking_animation_timer += self.walking_animation_speed * delta_time
        else:
            self.walking_animation_timer = 0.0
    
    def _check_interaction(self):
        print("¡Jugador intentó interactuar!")
        pass


    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.rotation_y, 0, 1, 0)
        Materials.apply_material(material=Materials.MAT_PLASTIC)
        glColor3fv(Materials.C_GREEN)
        
        self._draw()
        
        self._draw_legs()

        glPopMatrix()

    def _draw(self):
        s = 1
        Objects.draw_cube(size=s)

    def _draw_legs(self):
        """
        Dibuja las dos piernas, rotándolas según el temporizador de animación.
        """
        # --- Configuración de Animación ---
        # Usamos math.sin() para obtener un valor suave que oscila entre -1 y 1
        # Lo multiplicamos por un ángulo (ej. 35 grados) para la oscilación de la pierna
        max_angle = 35.0
        leg_angle = math.sin(self.walking_animation_timer) * max_angle

        # --- Dimensiones de la Pierna ---
        w = 0.3  # Ancho (X)
        h = 1.0  # Alto (Y)
        d = 0.3  # Profundidad (Z)

        # --- Pierna Izquierda ---
        glPushMatrix()
        try:
            glTranslatef(-0.3, -0.5, 0)
            glRotatef(leg_angle, 1, 0, 0)
            glColor3f(0.0, 0.4, 0.8)
            Objects.draw_cube(scale=[w, h, d])
        finally:
            glPopMatrix()

        # --- Pierna Derecha ---
        glPushMatrix()
        try:
            glTranslatef(0.3, -0.5, 0)
            glRotatef(-leg_angle, 1, 0, 0)
            glColor3f(0.0, 0.4, 0.8)
            Objects.draw_cube(scale=[w, h, d])
        finally:
            glPopMatrix()
