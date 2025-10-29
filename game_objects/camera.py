from OpenGL.GL import *
from OpenGL.GLU import *

class Camera:
    """
    Representa una cámara fija en el mundo 3D.
    Almacena su posición y el punto al que está mirando.
    """
    
    def __init__(self, position, look_at, up_vector=[0, 1, 0]):
        """
        Inicializa la cámara.
        
        :param position: Una lista o tupla [x, y, z] de dónde está la cámara.
        :param look_at: Una lista o tupla [x, y, z] del punto que la cámara está mirando.
        :param up_vector: Una lista o tupla [x, y, z] que define la dirección "arriba".
                          Casi siempre será [0, 1, 0] (eje Y positivo).
        """
        self.position = position
        self.look_at = look_at
        self.up = up_vector

    def apply_view(self):
        """
        Aplica la transformación de vista de esta cámara al pipeline de OpenGL.
        
        Esta función debe llamarse en cada frame ANTES de dibujar
        cualquier objeto del mundo (como el jugador o la mansión).
        """
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        gluLookAt(
            self.position[0], self.position[1], self.position[2],
            self.look_at[0], self.look_at[1], self.look_at[2],
            self.up[0], self.up[1], self.up[2]
        )