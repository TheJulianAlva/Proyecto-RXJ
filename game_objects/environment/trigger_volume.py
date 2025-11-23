from OpenGL.GL import *
from game_objects.environment.collider import AABB

class TriggerVolume:
    """
    Define una zona invisible que detecta cuándo el jugador entra en ella.
    Utiliza AABB para una detección de colisión precisa.
    """
    
    def __init__(self, min_point, max_point, target_camera_id=None):
        """
        Inicializa el trigger volume.
        
        :param min_point: Lista [x, y, z] con las coordenadas mínimas de la caja.
        :param max_point: Lista [x, y, z] con las coordenadas máximas de la caja.
        :param target_camera_id: (Opcional) El ID de la cámara que se debe activar.
        """
        self.aabb = AABB(min_point, max_point)
        
        self.target_camera_id = target_camera_id
        self.extra_data = {} # Diccionario para guardar info extra del JSON (ej. sonidos)

    def is_player_inside(self, player):
        """
        Comprueba si el jugador está tocando o dentro del volumen.
        
        :param player: La instancia del objeto Player.
        :return: True si el jugador está dentro, False en caso contrario.
        """
        player_box = player.get_aabb()
        return self.aabb.check_collision(player_box)

    def draw(self):
        """
        Dibuja el volumen como una caja de alambre (Wireframe) para depuración.
        """
        glPushMatrix()
        
        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        glColor3f(1.0, 1.0, 0.0)
        min_x, max_x = self.aabb.min_x, self.aabb.max_x
        min_z, max_z = self.aabb.min_z, self.aabb.max_z 
        
        y_bottom = 0.0
        y_top = 5.0
        
        glBegin(GL_LINES)
        
        # --- Líneas de la Base (Y=0) ---
        glVertex3f(min_x, y_bottom, min_z); glVertex3f(max_x, y_bottom, min_z)
        glVertex3f(max_x, y_bottom, min_z); glVertex3f(max_x, y_bottom, max_z)
        glVertex3f(max_x, y_bottom, max_z); glVertex3f(min_x, y_bottom, max_z)
        glVertex3f(min_x, y_bottom, max_z); glVertex3f(min_x, y_bottom, min_z)
        
        # --- Líneas del Techo (Y=5) ---
        glVertex3f(min_x, y_top, min_z); glVertex3f(max_x, y_top, min_z)
        glVertex3f(max_x, y_top, min_z); glVertex3f(max_x, y_top, max_z)
        glVertex3f(max_x, y_top, max_z); glVertex3f(min_x, y_top, max_z)
        glVertex3f(min_x, y_top, max_z); glVertex3f(min_x, y_top, min_z)
        
        # --- Pilares Verticales (Conectando base y techo) ---
        glVertex3f(min_x, y_bottom, min_z); glVertex3f(min_x, y_top, min_z)
        glVertex3f(max_x, y_bottom, min_z); glVertex3f(max_x, y_top, min_z)
        glVertex3f(max_x, y_bottom, max_z); glVertex3f(max_x, y_top, max_z)
        glVertex3f(min_x, y_bottom, max_z); glVertex3f(min_x, y_top, max_z)
        
        glEnd()
        
        glEnable(GL_LIGHTING)
        glPopMatrix()