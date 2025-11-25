from OpenGL.GL import *
from utilities import basic_objects as Objects
from game_objects.environment.collider import AABB

class Pedestal:
    def __init__(self, position, size, phrase, correct_statue_id, tex_id=-1):
        self.position = position
        self.size = size
        self.phrase = phrase
        self.correct_statue_id = correct_statue_id
        self.tex_id = tex_id
        self.default_base_color = (0.6, 0.6, 0.6)
        self.highlight_color = None
        
        half_x, half_z = self.size[0]/2, self.size[2]/2
        min_p = [position[0]-half_x, position[1], position[2]-half_z]
        max_p = [position[0]+half_x, position[1]+self.size[1], position[2]+half_z]
        self.collider = AABB(min_p, max_p)

    def get_AABB(self):
        return self.collider

    def set_position(self, new_position):
        """Actualiza la posición y su collider asociado."""
        self.position = list(new_position)
        half_x = self.size[0] / 2.0
        half_z = self.size[2] / 2.0
        self.collider.min_x = self.position[0] - half_x
        self.collider.max_x = self.position[0] + half_x
        self.collider.min_z = self.position[2] - half_z
        self.collider.max_z = self.position[2] + half_z

    def set_highlight_color(self, color):
        """Define el color de resaltado de la base (None para desactivar)."""
        self.highlight_color = color

    def draw(self):
        glPushMatrix()
        if self.tex_id != -1:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.tex_id)
            glColor3f(1.0, 1.0, 1.0)
        else:
            glDisable(GL_TEXTURE_2D)
            glColor3f(0.6, 0.6, 0.6)

        glDisable(GL_LIGHTING)
        glTranslatef(*self.position)
        base_color = self.highlight_color if self.highlight_color else self.default_base_color
        glColor3f(*base_color)
        Objects.draw_textured_box(self.size, translate=self.position)
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)
        glPopMatrix()

        