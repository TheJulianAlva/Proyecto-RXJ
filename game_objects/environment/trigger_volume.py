from OpenGL.GL import *

class TriggerVolume:
    """
    Define una caja invisible que, cuando el jugador
    entra en ella, activa un evento (como cambiar la cámara).
    """
    
    def __init__(self, min_point, max_point, target_camera_id):
        """
        Inicializa el volumen.
        
        :param min_point: Una lista [x, y, z] para la esquina mínima de la caja.
        :param max_point: Una lista [x, y, z] para la esquina máxima de la caja.
        :param target_camera_id: El string ID de la cámara que debe activarse.
        """
        self.min_x = min_point[0]
        self.min_y = min_point[1]
        self.min_z = min_point[2]
        self.max_x = max_point[0]
        self.max_y = max_point[1]
        self.max_z = max_point[2]
        
        self.target_camera_id = target_camera_id
        
        # Vértices y aristas guardados meramente para depuración
        # (dibujar temporalmente el área de trigger)

        self._vertices = [
            (self.min_x, self.min_y, self.min_z),
            (self.max_x, self.min_y, self.min_z),
            (self.max_x, self.max_y, self.min_z),
            (self.min_x, self.max_y, self.min_z),
            (self.min_x, self.min_y, self.max_z),
            (self.max_x, self.min_y, self.max_z),
            (self.max_x, self.max_y, self.max_z),
            (self.min_x, self.max_y, self.max_z)
        ]
        
        self._edges = [
            (0, 1), (1, 2), (2, 3), (3, 0), # Cara trasera
            (4, 5), (5, 6), (6, 7), (7, 4), # Cara frontal
            (0, 4), (1, 5), (2, 6), (3, 7)  # Conexiones
        ]

    def is_player_inside(self, player_pos):
        """Comprueba si la posición del jugador está dentro de este volumen."""
        return (self.min_x <= player_pos[0] <= self.max_x and
                self.min_y <= player_pos[1] <= self.max_y and
                self.min_z <= player_pos[2] <= self.max_z)

    def draw(self):
        """
        Dibuja el volumen como una caja 'wireframe' (Modo Inmediato).
        Esto es solo para depuración, para que podamos ver dónde están
        nuestros triggers.
        """
        glPushMatrix()
        # Dibujamos las líneas de un color brillante (ej. amarillo)
        glColor3f(1.0, 1.0, 0.0)

        # Desactivamos la iluminación para esta parte (si la tuviéramos)
        # glDisable(GL_LIGHTING) 
        glBegin(GL_LINES)
        for edge in self._edges:
            for vertex_index in edge:
                glVertex3fv(self._vertices[vertex_index])
        glEnd()
        # glEnable(GL_LIGHTING)
        glPopMatrix()