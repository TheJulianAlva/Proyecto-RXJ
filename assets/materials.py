"""
Archivo central para definir todas las propiedades de 
materiales de iluminación en el juego.
"""

from OpenGL.GL import *

# --- COLORES BASE ---
C_GREEN = [42/255, 220/255, 90/255]
C_LIGHT_YELLOW = [255/255, 240/255, 120/255]
C_RED = [0.9, 0.3, 0.2]
C_BLUE = [20/255, 90/255, 230/255]
C_YELLOW = [1.0, 0.78, 0.0]
C_WHITE = [0.9, 0.9, 0.9]
C_GREY = [0.65, 0.65, 0.65]
C_DARK_GREY = [0.45, 0.45, 0.45]
C_BLACK = [0.1, 0.1, 0.1]
C_BROWN = [85/255, 50/255, 30/255]
C_LIGHT_ORANGE = [155/255, 120/255, 80/255]

# --- MATERIALES GENÉRICOS ---
MAT_FABRIC = {
    "specular": [0.0, 0.0, 0.0, 1.0],  # Sin reflejo de luz
    "shininess": [0.0]                  # Sin brillo
}

MAT_PLASTIC = {
    "specular": [0.7, 0.7, 0.7, 1.0],  # Un reflejo blanco (color de la luz)
    "shininess": [32.0]                 # Un brillo de tamaño medio
}

MAT_METAL = {
    "specular": [0.9, 0.9, 0.9, 1.0],  # Un reflejo muy fuerte y nítido
    "shininess": [100.0]                # Un brillo muy concentrado
}

# --- FUNCIÓN DE UTILIDAD ---
def apply_material(material):
    """
    Configura las propiedades de brillo del material (especular y shininess).
    Se asume que GL_COLOR_MATERIAL está activado para ambient y diffuse.
    """
    glMaterialfv(GL_FRONT, GL_SPECULAR, material["specular"])
    glMaterialfv(GL_FRONT, GL_SHININESS, material["shininess"])