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

        self.cameras = {} # Diccionario para guardar las cámaras por ID
        self.active_camera = None

    def load_cameras(self, level_data):
        """
        Carga y crea todas las instancias de cámara.
        
        """
        cameras_config = level_data.get("cameras", [])
        self.cameras = {camera_config.get("id"): Camera(camera_config.get("position", (0, 15, 10)), camera_config.get("look_at", (0, 0, 0))) for camera_config in cameras_config}
        
        print(f"Cargadas {len(self.cameras)} cámaras.")
        
        self.set_active_camera("cam_1")

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