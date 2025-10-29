from game_objects.camera import Camera 

class CameraManager:
    """
    Singleton que gestiona todas las cámaras fijas del juego.
    
    Se accede a la instancia única a través de:
    CameraManager.instance()
    """

    
    _instance = None # Variable de clase para guardar la instancia única

    @staticmethod
    def instance():
        """
        Devuelve la instancia única del CameraManager.
        Si no existe, la crea.
        """
        if CameraManager._instance is None:
            CameraManager._instance = CameraManager()
        return CameraManager._instance

    def __init__(self):
        """
        Constructor 'privado'. No lo llames directamente.
        Usa .instance() en su lugar.
        """
        if CameraManager._instance is not None:
            raise Exception("CameraManager es un singleton. Usa .instance() para obtenerlo.")
        
        print("CameraManager inicializado.")

        
        self.cam1 = Camera(position=[10, 15, 10], look_at=[0, 0, 0])
        self.cam2 = Camera(position=[5, 5, -10], look_at=[5, 0, 0])
        self.cam_default = Camera(position=[0, 5, -5], look_at=[0, 0, 0])

        self.cameras = {} # Diccionario para guardar las cámaras por ID
        self.active_camera = None

    def load_cameras(self):
        """
        Carga y crea todas las instancias de cámara.
        
        (Más adelante, podrías leer esto desde un archivo JSON, 
        pero por ahora, las creamos aquí)
        """

        # Las guardamos en el diccionario con un ID de texto
        self.cameras["camera_1"] = self.cam1
        self.cameras["camera_2"] = self.cam2
        self.cameras["camera_default"] = self.cam_default
        
        print(f"Cargadas {len(self.cameras)} cámaras.")
        
        self.set_active_camera("camera_default")

    def set_active_camera(self, camera_id):
        """
        Cambia la cámara activa actual.
        """
        if camera_id in self.cameras:
            self.active_camera = self.cameras[camera_id]
            print(f"Cámara activa cambiada a: {camera_id}")
        else:
            print(f"Error: No se encontró la cámara con ID: {camera_id}")

    def get_active_camera(self):
        """
        Devuelve la instancia de la cámara activa actual.
        """
        return self.active_camera