from OpenGL.GL import *
from OpenGL.GLU import *
from systems.input_manager import InputManager
from utilities import materials as Materials
from game_objects.character_models import alien, santo, walter
from utilities import basic_objects as Objects

class CharacterSelectionPlatform:
    def __init__(self, x, y, z):
        self.position = [x, y, z]
        self.rotation_y = 0.0
        self.selected_index = 0
        self.target_rotation = 0.0
        self.movement_speed = 3.0
        self.rotate_speed = 120
        self.is_moving = False
        self.input_manager = InputManager.instance()
        self.quad = gluNewQuadric()
        gluQuadricNormals(self.quad, GLU_SMOOTH)
        self.characters = [santo, alien, walter]


    def rotate(self, angle):
        self.rotation_y += angle
        if self.rotation_y > 360: self.rotation_y = 0

    def update(self, delta_time):
        self.is_moving = True
        self.characters[0].update_animation(delta_time)
        self.characters[1].update_animation(delta_time)
        self.characters[2].update_animation(delta_time)
        if self.rotation_y == self.target_rotation:
            self.is_moving = False
            return
        if self.rotation_y < self.target_rotation:
            self.rotate(angle=self.rotate_speed*delta_time)
        else:
            self.rotate(angle=-self.rotate_speed*delta_time)
        

        
    def get_rotation(self):
        return self.rotation_y
    
    def set_rotation(self, angle):
        self.rotation_y = angle
    
    def set_target_rotation(self, angle):
        self.target_rotation = angle



    def draw(self):
        self._configure_light()
        glPushMatrix()
        glRotatef(self.rotation_y, 0.0, 1.0, 0.0)
        self._draw_platform()
        self._draw_characters()
        glPopMatrix()

    def _configure_light(self):
        """Configura la luz 0 según el modo actual (light_mode)."""
        glEnable(GL_LIGHT0)
        # Propiedades básicas de la luz (blanca)
        light_ambient = [0.2, 0.2, 0.2, 1.0]
        light_diffuse = [0.2, 0.2, 0.2, 1.0]
        light_specular = [0.0, 0.0, 0.0, 1.0]
        
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
        
        light_pos_point = [0.0, 20.0, 16.0, 1.0]
        
        # Configuración del Foco
        spot_dir = [0.0, -1.0, -0.6] # Apuntando hacia abajo y al frente
        spot_cutoff = 15.0          # Ángulo de 30 grados
        spot_exponent = 0.0        # Enfoque del haz de luz
        
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos_point) # Un foco debe ser puntual
        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, spot_cutoff)
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, spot_dir)
        glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, spot_exponent)
    
    def _draw_platform(self):
        glPushMatrix()
        Materials.apply_material(material=Materials.MAT_METAL)
        glColor3fv(Materials.C_BLUE)
        Objects.draw_cylinder(quad=self.quad, scale=[10.0, 10.0, 10.0], translate=[0.0, 0.0, 0.0])
        Objects.draw_partial_disk(quad=self.quad, scale=[10.0, 10.0, 1.0], translate=[0.0, 0.0, 0.0], rotation=[90, 1.0, 0.0, 0.0])
        glPopMatrix()

    def _draw_characters(self):
        glPushMatrix()
        glTranslatef(0.0, -0.5, 6.0)
        self.characters[0].draw()
        glPopMatrix()
        glPushMatrix()
        glRotatef(120, 0, 1, 0)
        glTranslatef(0.0, -0.5, 6.0)
        self.characters[1].draw()
        glPopMatrix()
        glPushMatrix()
        glRotatef(240, 0, 1, 0)
        glTranslatef(0.0, -0.5, 6.0)
        self.characters[2].draw()
        glPopMatrix()