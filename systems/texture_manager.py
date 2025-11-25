import pygame
from OpenGL.GL import *

class TextureManager:
    """
    Singleton que administra la carga, el caché y la descarga
    de las texturas de OpenGL.
    
    Esto previene cargar la misma textura varias veces y maneja
    la liberación de memoria VRAM.
    """
    _instance = None
    
    @staticmethod
    def instance():
        if TextureManager._instance is None:
            TextureManager._instance = TextureManager()
        return TextureManager._instance

    def __init__(self):
        if TextureManager._instance is not None:
            raise Exception("TextureManager es un singleton. Usa .instance()")
        
        # El caché central de texturas
        # Guarda: { "nombre_textura": texture_id }
        self.textures = {}
        print("TextureManager inicializado.")

    def get_texture(self, texture_name, image_path=None):
        """
        Obtiene el ID de una textura.
        Si la textura no está cargada (no está en el caché),
        la carga desde 'image_path'.
        
        :param texture_name: El nombre clave de la textura (ej. "pared_ladrillo")
        :param image_path: La ruta al archivo (ej. "assets/textures/wall_brick.png")
        :return: El ID (int) de la textura en OpenGL, or -1 si falla.
        """
        # 1. Comprobar si ya está en el caché
        if texture_name in self.textures:
            return self.textures[texture_name]
        
        # 2. Si no, y si nos dieron una ruta, cargarla
        if image_path:
            return self.load_texture(texture_name, image_path)
        
        # 3. Si no está y no hay ruta, es un error
        print(f"Advertencia: Se pidió la textura '{texture_name}' pero no está cargada y no se proveyó una ruta.")
        return -1

    def load_texture(self, texture_name, image_path):
        """
        Carga una textura, la guarda en el caché y devuelve el ID.
        Si ya existe, simplemente devuelve el ID.
        """
        if texture_name in self.textures:
            return self.textures[texture_name]
        
        try:
            surface = pygame.image.load(image_path)
        except pygame.error as e:
            print(f"Error al cargar la imagen {image_path}: {e}")
            return -1

        print(f"Cargando textura: {image_path} (Nombre: {texture_name})")

        # Convertir a string de bytes (El 'True' voltea la imagen para OpenGL)
        image_data = pygame.image.tostring(surface, "RGBA", True)
        width, height = surface.get_width(), surface.get_height()

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        # Configuración de filtros (usa GL_LINEAR para suavizado)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        
        # Configuración de repetición (cómo se manejan las coords. > 1.0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        # Enviar datos de la imagen a la GPU
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 
                     0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        
        glBindTexture(GL_TEXTURE_2D, 0) # Des-bindear
        
        # Guardar en el caché
        self.textures[texture_name] = texture_id
        
        return texture_id

    def unload_texture(self, texture_name):
        """
        Libera una textura de la memoria VRAM y la quita del caché.
        """
        if texture_name in self.textures:
            texture_id = self.textures.pop(texture_name) # Quitar del dict
            glDeleteTextures(1, [texture_id]) # Liberar de la GPU
            print(f"Textura '{texture_name}' (ID: {texture_id}) descargada.")
        else:
            print(f"Advertencia: Se intentó descargar la textura '{texture_name}' pero no estaba cargada.")