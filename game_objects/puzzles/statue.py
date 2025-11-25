from OpenGL.GL import *
from utilities import basic_objects as Objects
from game_objects.environment.collider import AABB

class Statue:
    """
    Representa una estatua u objeto interactuable en el mundo.
    Combina representación visual (draw) con lógica física (AABB).
    """
    def __init__(self, id, position, size, rotation, name, tex_id):
        """
        :param position: Lista [x, y, z] de la posición central.
        :param rotation: Lista [ángulo, eje_x, eje_y, eje_z] para glRotatef.
        :param size: Lista [ancho, alto, profundidad].
        :param name: Nombre del objeto (para UI).
        :param phrase: Texto que muestra al interactuar.
        :param tex_id: ID de OpenGL de la textura cargada.
        """
        self.id = id
        self.position = list(position)
        self.rotation = rotation
        self.size = size
        self.name = name
        self.tex_id = tex_id
        self.default_base_color = (0.6, 0.6, 0.6)
        self.highlight_color = None
        
        half_x = size[0] / 2.0
        half_z = size[2] / 2.0
        
        min_point = [position[0] - half_x, position[1], position[2] - half_z]
        max_point = [position[0] + half_x, position[1] + size[1], position[2] + half_z]
        
        self.collider = AABB(min_point, max_point)

    def get_AABB(self):
        return self.collider

    def update(self, delta_time):
        """
        Lógica de actualización por frame.
        """
        pass

    def draw(self):
        """
        Dibuja la estatua.
        """
        glPushMatrix()
        glDisable(GL_LIGHTING)
        glTranslatef(*self.position)
        if self.tex_id != -1:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.tex_id)
            glColor3f(1.0, 1.0, 1.0)
        else:
            glDisable(GL_TEXTURE_2D)
            glColor3f(0.6, 0.6, 0.6)
        offset_y = self.size[0] + self.size[1] / 2
        glRotatef(*self.rotation)
        Objects.draw_textured_plane_3d(self.size[0]+2, self.size[1], rotation=[90, 1, 0, 0])
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)
        glPopMatrix()

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
        
    def interact(self):
        """
        Método opcional para manejar la interacción.
        """
        print(f"[{self.name}]")