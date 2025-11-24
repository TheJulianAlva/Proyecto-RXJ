from OpenGL.GL import *
from utilities import basic_objects as Objects
from game_objects.environment.collider import AABB

class Statue:
    """
    Representa una estatua u objeto interactuable en el mundo.
    Combina representación visual (draw) con lógica física (AABB).
    """
    def __init__(self, id, position, size, rotation, name, phrase, tex_id):
        """
        :param position: Lista [x, y, z] de la posición central.
        :param rotation: Lista [ángulo, eje_x, eje_y, eje_z] para glRotatef.
        :param size: Lista [ancho, alto, profundidad].
        :param name: Nombre del objeto (para UI).
        :param phrase: Texto que muestra al interactuar.
        :param tex_id: ID de OpenGL de la textura cargada.
        """
        self.id = id
        self.position = position
        self.rotation = rotation
        self.size = size
        self.name = name
        self.phrase = phrase
        self.tex_id = tex_id
        
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
        glTranslatef(*self.position)
        glColor3f(0.6, 0.6, 0.6)
        Objects.draw_cube(self.size[0], translate=[0, 1.5, 0])
        
        if self.tex_id != -1:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.tex_id)
            glColor3f(1.0, 1.0, 1.0)
        else:
            glDisable(GL_TEXTURE_2D)
            glColor3f(0.6, 0.6, 0.6)
        offset_y = self.size[0] + self.size[1] / 2
        glRotatef(*self.rotation)
        Objects.draw_textured_plane_3d(self.size[0]+2, self.size[1], translate= [0.0, offset_y, 0.0], rotation=[90, 1, 0, 0])
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        
    def interact(self):
        """
        Método opcional para manejar la interacción.
        """
        print(f"[{self.name}]: {self.phrase}")
        # Aquí podrías disparar un evento de UI para mostrar el texto en pantalla