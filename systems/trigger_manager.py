from game_objects.environment.trigger_volume import TriggerVolume 

class TriggerManager:
    """
    Singleton que gestiona todos los trigger volumes del juego.
    
    Se accede a la instancia única a través de:
    TriggerManager.instance()
    """

    
    _instance = None # Variable de clase para guardar la instancia única

    @staticmethod
    def instance():
        """
        Devuelve la instancia única del TriggerManager.
        Si no existe, la crea.
        """
        if TriggerManager._instance is None:
            TriggerManager._instance = TriggerManager()
        return TriggerManager._instance

    def __init__(self):
        """
        Constructor 'privado'. No lo llames directamente.
        Usa .instance() en su lugar.
        """
        if TriggerManager._instance is not None:
            raise Exception("TriggerManager es un singleton. Usa .instance() para obtenerlo.")
        
        print("TriggerManager inicializado.")
        self.triggers = []


    def load_triggers(self, level_data):
        
        triggers_config = level_data.get("triggers", [])
        
        for t_data in triggers_config:
            trigger = TriggerVolume(
                min_point=t_data["box_min"],
                max_point=t_data["box_max"],
                target_camera_id=t_data.get("target_camera_id")
            )
            trigger.extra_data = t_data
            self.triggers.append(trigger)
            
        print(f"Triggers cargados: {len(self.triggers)}")


    def check_triggers(self, player):
        """
        Revisa si el jugador colisiona con algún TriggerVolume.
        Debe ser llamado desde PlayState.update().
        """
        for trigger in self.triggers:
            if trigger.is_player_inside(player):
                return trigger.target_camera_id
        return None

    def unload_triggers(self):
        self.triggers = []