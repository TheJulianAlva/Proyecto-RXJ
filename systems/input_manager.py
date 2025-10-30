import pygame

class InputManager:
    """
    Singleton que gestiona todas las entradas del usuario.
    
    Abstrae las teclas físicas (ej. K_w) en "acciones" lógicas 
    (ej. "move_forward").
    
    Maneja tanto acciones "mantenidas" (para movimiento) como 
    acciones "presionadas" (para eventos de una sola vez).
    
    Se accede a la instancia única a través de:
    InputManager.instance()
    """
    
    _instance = None # Instancia única

    @staticmethod
    def instance():
        """Devuelve la instancia única del InputManager."""
        if InputManager._instance is None:
            InputManager._instance = InputManager()
        return InputManager._instance

    def __init__(self):
        """Constructor 'privado'. Usa .instance() en su lugar."""
        if InputManager._instance is not None:
            raise Exception("InputManager es un singleton. Usa .instance() para obtenerlo.")
        
        self.key_map = {}          # Mapa de "accion" -> tecla (ej. "move_forward": K_w)
        self.actions_held = {}     # Estado de acciones mantenidas (ej. "move_forward": True)
        self.actions_pressed = {}  # Estado de acciones de un solo pulso (ej. "interact": True)
        
        self.quit_attempted = False
        print("InputManager inicializado.")

    def setup_bindings(self):
        """
        Define las asignaciones de teclas.
        (En un juego más grande, esto se leería de un archivo de configuración).
        """
        # Acciones Mantenidas (para movimiento)
        self.key_map["move_forward"] = pygame.K_w
        self.key_map["move_backward"] = pygame.K_s
        self.key_map["rotate_left"] = pygame.K_a
        self.key_map["rotate_right"] = pygame.K_d
        
        # Acciones Presionadas (para eventos únicos)
        self.key_map["interact"] = pygame.K_e
        self.key_map["quit"] = pygame.K_ESCAPE

        # Inicializa los diccionarios de estado
        held_actions = ["move_forward", "move_backward", "rotate_left", "rotate_right"]
        pressed_actions = ["interact", "quit"]
        
        self.actions_held = {action: False for action in held_actions}
        self.actions_pressed = {action: False for action in pressed_actions}

    def process_inputs(self, event_list):
        """
        Esta es la función principal. Debe ser llamada UNA VEZ por fotograma.
        Procesa la lista de eventos de PyGame y actualiza todos los estados de acción.
        """
        
        # 1. Resetear todas las acciones "presionadas"
        for action in self.actions_pressed:
            self.actions_pressed[action] = False
            
        # 2. Procesar la lista de eventos de PyGame
        for event in event_list:
            if event.type == pygame.QUIT:
                self.quit_attempted = True
                
            if event.type == pygame.KEYDOWN:
                # Comprobar si esta tecla activa una acción "presionada"
                for action, key in self.key_map.items():
                    if action in self.actions_pressed and event.key == key:
                        self.actions_pressed[action] = True
            
            if self.actions_pressed["quit"]:
                self.quit_attempted = True

        # 3. Procesar todas las acciones "mantenidas"
        key_states = pygame.key.get_pressed()
        for action, key in self.key_map.items():
            if action in self.actions_held:
                self.actions_held[action] = key_states[key]

    # --- Métodos de Consulta ---
    # El resto del juego usará estos métodos para preguntar por acciones
    
    def is_action_held(self, action_name):
        """Devuelve True si la acción (ej. "move_forward") está siendo mantenida."""
        return self.actions_held.get(action_name, False)

    def was_action_pressed(self, action_name):
        """Devuelve True si la acción (ej. "interact") se presionó ESTE fotograma."""
        return self.actions_pressed.get(action_name, False)

    def did_quit(self):
        """Devuelve True si el usuario intentó cerrar la ventana."""
        return self.quit_attempted