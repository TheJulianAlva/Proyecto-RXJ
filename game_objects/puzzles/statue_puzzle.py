from OpenGL.GL import *
from OpenGL.GLU import *
from utilities import basic_objects as Objects
from systems.texture_manager import TextureManager
import math

class StatuePuzzle:
    """
    Puzzle que consiste en varias estatuas que deben ser rotadas
    a una orientación específica para resolver el acertijo.
    """
    def __init__(self, puzzle_data):
        self.pos = puzzle_data.get("position", [0, 0, 0])
        self.solved = False
        
        # Configuración específica de este puzzle
        props = puzzle_data.get("properties", {})
        
        # Definición de las estatuas individuales
        # Ejemplo en JSON: "statues": [{"id": 1, "offset": [0,0,0], "target_angle": 180}]
        self.statues_config = props.get("statues", [])
        
        # Estado actual de cada estatua
        self.statue_states = []
        for s_conf in self.statues_config:
            self.statue_states.append({
                "current_angle": 0.0,    # Ángulo visual actual (para animación)
                "logic_angle": 0.0,      # Ángulo lógico (0, 90, 180, 270)
                "target_angle": s_conf.get("target_angle", 0.0), # La solución
                "offset": s_conf.get("offset", [0, 0, 0]),       # Posición relativa al centro del puzzle
                "is_rotating": False,
                "rotation_target": 0.0
            })
            
        # Recursos
        self.texture_manager = TextureManager.instance()
        # (Aquí podrías cargar una textura específica para la estatua si el JSON lo pide)
        # self.statue_tex = ...
        
        self.interaction_radius = 2.0 # Distancia máxima para interactuar con una estatua
        print(f"StatuePuzzle inicializado con {len(self.statue_states)} estatuas.")

    def update(self, delta_time):
        """
        Actualiza la animación de giro y comprueba si se resolvió.
        """
        if self.solved:
            return # Si ya ganamos, no hacemos nada (o animamos algo especial)

        all_correct = True
        rotation_speed = 180.0 # Grados por segundo
        
        for state in self.statue_states:
            # --- Lógica de Animación ---
            if state["is_rotating"]:
                diff = state["rotation_target"] - state["current_angle"]
                
                # Si estamos cerca, terminamos el giro
                if abs(diff) < 5.0:
                    state["current_angle"] = state["rotation_target"]
                    state["is_rotating"] = False
                else:
                    # Girar hacia el objetivo
                    direction = 1 if diff > 0 else -1
                    state["current_angle"] += direction * rotation_speed * delta_time

            # --- Lógica de Comprobación ---
            # Normalizamos ángulos a 0-360 para comparar
            norm_current = int(state["logic_angle"]) % 360
            norm_target = int(state["target_angle"]) % 360
            
            if norm_current != norm_target:
                all_correct = False
        
        # Si recorrimos todas y todas están bien...
        if all_correct and not self.solved:
            self.solved = True
            print("¡PUZZLE RESUELTO! El mecanismo se activa.")
            # Aquí podrías reproducir un sonido: SoundManager.play("secret_door")

    def draw(self):
        """
        Dibuja todas las estatuas del puzzle.
        """
        # Guardamos la matriz actual (posición del mundo)
        glPushMatrix()
        # Movemos al centro del puzzle (definido en el JSON)
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        
        for state in self.statue_states:
            glPushMatrix()
            
            # 1. Posición relativa de esta estatua específica
            off = state["offset"]
            glTranslatef(off[0], off[1], off[2])
            
            # 2. Rotación de la estatua
            glRotatef(state["current_angle"], 0, 1, 0)
            
            # 3. Dibujar la estatua
            self._draw_single_statue()
            
            glPopMatrix()
            
        glPopMatrix()

    def _draw_single_statue(self):
        """Dibuja el modelo de una sola estatua."""
        # Feedback visual: Si está resuelto se pone verde, si no rojo/gris
        if self.solved:
            glColor3f(0.2, 1.0, 0.2) # Verde victoria
        else:
            glColor3f(0.7, 0.7, 0.7) # Gris piedra
        
        # Base
        Objects.draw_cube(scale=[0.8, 0.2, 0.8], translate=[0, 0.1, 0])
        # Cuerpo (simulado con un cubo alto por ahora)
        # Nota: La "cara" de la estatua está hacia Z+ para que la rotación tenga sentido
        Objects.draw_cube(scale=[0.5, 1.5, 0.5], translate=[0, 1.0, 0])
        # "Nariz" para ver hacia dónde mira
        Objects.draw_cube(scale=[0.2, 0.2, 0.2], translate=[0, 1.5, 0.3]) 

    def interact(self, player_pos):
        """
        Llamado cuando el jugador pulsa 'E'.
        Determina qué estatua está cerca y la gira.
        """
        if self.solved:
            print("El puzzle ya está resuelto.")
            return

        # Convertir posición del puzzle a absoluta para comparar con jugador
        puzzle_x, puzzle_y, puzzle_z = self.pos
        
        closest_statue = None
        min_dist = 999.0
        
        # Buscar la estatua más cercana
        for state in self.statue_states:
            # Posición absoluta de esta estatua
            statue_abs_x = puzzle_x + state["offset"][0]
            statue_abs_z = puzzle_z + state["offset"][2]
            
            # Distancia simple (Euclidiana en 2D, ignoramos altura Y)
            dx = player_pos[0] - statue_abs_x
            dz = player_pos[2] - statue_abs_z
            dist = math.sqrt(dx*dx + dz*dz)
            
            if dist < min_dist:
                min_dist = dist
                closest_statue = state

        # Si encontramos una estatua cerca, la giramos
        if closest_statue and min_dist <= self.interaction_radius:
            if not closest_statue["is_rotating"]:
                print("Girando estatua...")
                closest_statue["logic_angle"] += 90.0
                closest_statue["rotation_target"] += 90.0
                closest_statue["is_rotating"] = True
        else:
            print("Estás demasiado lejos de las estatuas.")

    def is_completed(self):
        return self.solved