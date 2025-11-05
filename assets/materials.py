"""
Archivo central para definir todas las propiedades de 
materiales de iluminación en el juego.
"""

from OpenGL.GL import *

# --- COLORES BASE ---
C_GREEN = [0.1, 0.6, 0.1]
C_PLAYER_BLUE = [0.0, 0.5, 1.0]
C_WHITE = [1.0, 1.0, 1.0]

# --- MATERIALES ---
MAT_GREEN = {
    "ambient": [C_GREEN[0]*0.3, C_GREEN[1]*0.3, C_GREEN[2]*0.3, 1.0],
    "diffuse": [C_GREEN[0], C_GREEN[1], C_GREEN[2], 1.0],
    "specular": [0.2, 0.2, 0.2, 1.0],
    "shininess": 10.0
}

MAT_PLAYER = {
    "ambient": [C_PLAYER_BLUE[0]*0.3, C_PLAYER_BLUE[1]*0.3, C_PLAYER_BLUE[2]*0.3, 1.0],
    "diffuse": [C_PLAYER_BLUE[0], C_PLAYER_BLUE[1], C_PLAYER_BLUE[2], 1.0],
    "specular": [C_WHITE[0]*0.5, C_WHITE[1]*0.5, C_WHITE[2]*0.5, 1.0],
    "shininess": 50.0
}

# --- FUNCIÓN DE UTILIDAD ---
def apply_material(material):
    """
    Aplica un diccionario de material definido 
    a las propiedades actuales de OpenGL.
    """
    glMaterialfv(GL_FRONT, GL_AMBIENT, material["ambient"])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material["diffuse"])
    glMaterialfv(GL_FRONT, GL_SPECULAR, material["specular"])
    glMaterialf(GL_FRONT, GL_SHININESS, material["shininess"])