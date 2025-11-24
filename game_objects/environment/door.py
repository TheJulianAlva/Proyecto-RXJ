from OpenGL.GL import *
from utilities import basic_objects as Objects
from game_objects.environment.collider import AABB

class Door:
    """
    Representa una puerta física en el nivel.
    Actúa como un obstáculo sólido hasta que se interactúa con ella.
    Si está desbloqueada, su interacción señala el fin del nivel.
    """
    def __init__(self, position, size, rotation, tex_id, is_locked=True):
        """
        :param position: [x, y, z] Posición central de la puerta.
        :param size: [ancho, alto, grosor] Dimensiones.
        :param rotation: [angulo, x, y, z] Orientación inicial.
        :param tex_id: ID de la textura.
        :param is_locked: Si True, la puerta no permite el paso.
        """
        self.position = position
        self.size = size
        self.rotation = rotation
        self.tex_id = tex_id
        self.is_locked = is_locked
        half_x = self.size[0] / 2.0
        half_z = self.size[2] / 2.0
        min_point = [position[0] - half_x, position[1], position[2] - half_z]
        max_point = [position[0] + half_x, position[1] + self.size[1], position[2] + half_z]
        self.collider = AABB(min_point, max_point)

    def unlock(self):
        """Permite que la puerta sea usada para salir."""
        self.is_locked = False
        print("Click... La puerta se ha desbloqueado.")

    def interact(self):
        """
        Intenta usar la puerta.
        Retorna True si la puerta se usó exitosamente (cambio de nivel).
        Retorna False si está cerrada.
        """
        if self.is_locked:
            print("Está cerrada con llave. Parece que falta resolver algo...")
            # Aquí podrías reproducir sonido: sfx_locked.wav
            return False

        print("Cruzando la puerta...")
        # Aquí podrías reproducir sonido: sfx_door_open.wav
        return True

    def draw(self):
        """Dibuja la puerta estática."""
        if self.tex_id != -1:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.tex_id)
            glColor3f(1.0, 1.0, 1.0)
        else:
            glDisable(GL_TEXTURE_2D)
            glColor3f(0.4, 0.25, 0.1) # Marrón

        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation[0], self.rotation[1], self.rotation[2], self.rotation[3])
        
        # Dibujamos la puerta cerrada
        Objects.draw_textured_box(size=self.size)
        
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)
    
