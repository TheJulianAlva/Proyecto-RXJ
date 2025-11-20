import json
import os

class DataManager:
    """
    Singleton que gestiona la carga de todos los archivos de datos JSON.
    
    Carga la configuración global y el texto del idioma al inicio.
    Proporciona métodos para cargar datos de escenas bajo demanda.
    Separa la lógica del juego (Python) de los datos (JSON).
    """
    _instance = None
    
    @staticmethod
    def instance():
        """Devuelve la instancia única del DataManager."""
        if DataManager._instance is None:
            DataManager._instance = DataManager()
        return DataManager._instance

    def __init__(self):
        """
        Constructor 'privado'. Carga los datos globales.
        Usa .instance() en su lugar.
        """
        if DataManager._instance is not None:
            raise Exception("DataManager es un singleton. Usa .instance() para obtenerlo.")
        
        self.config = {}
        self.text = {}
        
        self._load_global_data()
        print("DataManager inicializado.")

    def _load_json(self, file_path):
        """
        Función auxiliar privada para cargar y parsear un archivo JSON.
        Devuelve un dict vacío si falla.
        """
        try:
            # Usamos encoding='utf-8' para soportar acentos y 'ñ'
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error CRÍTICO: El archivo JSON no se encontró: {file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error CRÍTICO: El archivo JSON está mal formado: {file_path}")
            return {}
        except Exception as e:
            print(f"Error CRÍTICO al cargar JSON {file_path}: {e}")
            return {}

    def _load_global_data(self):
        """
        Carga los archivos de configuración y texto que
        siempre son necesarios.
        """
        # 1. Cargar la configuración principal
        self.config = self._load_json("data/config.json")
        if not self.config:
            print("ADVERTENCIA: 'data/config.json' no se pudo cargar. Se usarán valores por defecto.")
        
        # 2. Cargar el archivo de texto basado en el idioma del config
        # .get() es seguro, si "language" no existe, usa "es"
        lang = self.config.get("language", "es")
        self.text = self._load_json(f"data/text_{lang}.json")
        if not self.text:
            print(f"ADVERTENCIA: 'data/text_{lang}.json' no se pudo cargar.")

    # --- Métodos Públicos ---

    def get_config(self):
        """
        Devuelve el diccionario de configuración completo (cargado de config.json).
        """
        return self.config

    def get_text_dict(self):
        """
        Devuelve el diccionario de texto completo del idioma actual.
        """
        return self.text

    def load_scene_data(self, scene_name):
        """
        Carga y devuelve los datos de un archivo de escena específico
        de la carpeta 'data/scenes/'.
        
        :param scene_name: El nombre del archivo JSON (ej. "scene_selection")
        :return: Un diccionario con los datos de la escena.
        """
        print(f"Cargando datos de escena: {scene_name}")
        return self._load_json(f"data/scenes/{scene_name}.json")
    
    def save_game_data(self, data_dict):
        """
        Guarda un diccionario de datos en 'data/game_config.json'.
        Sobrescribe el archivo anterior.
        """
        file_path = "data/game_config.json"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, indent=4)
            print(f"Partida guardada exitosamente en {file_path}")
            return True
        except Exception as e:
            print(f"Error CRÍTICO al guardar partida: {e}")
            return False

    def load_game_data(self):
        """
        Carga los datos de progreso del jugador.
        Devuelve un diccionario vacío {} si no existe archivo de guardado.
        """
        file_path = "data/game_config.json"
        
        if not os.path.exists(file_path):
            print("No se encontró archivo de guardado. Se creará uno nuevo al guardar.")
            return {} # Retorna vacío para que el juego use valores por defecto
            
        return self._load_json(file_path)