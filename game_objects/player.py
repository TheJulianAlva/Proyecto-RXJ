from OpenGL.GL import *
from systems.input_manager import InputManager
from systems.audio_manager import AudioManager
from systems.collision_system import CollisionSystem
from game_objects.environment.collider import AABB
import math


class Player:
    def __init__(self, x, y, z, skin_class):
        self.position = [x, y, z]
        self.rotation_y = 0.0
        self.width_collider = 1.0
        self.depth_collider = 1.0
        self.movement_speed = 9.0
        self.rotate_speed = 280
        self.input_manager = InputManager.instance()
        self.skin = skin_class()

        self.is_walking = False
        self.was_walking = False
        self.audio = AudioManager.instance()

    def get_aabb(self):
        """
        Retorna la caja de colisión (AABB) actual del jugador.
        """
        half_w = self.width_collider / 2
        half_d = self.depth_collider / 2
        
        min_point = [self.position[0] - half_w, self.position[2] - half_d]
        max_point = [self.position[0] + half_w, self.position[2] + half_d]
        
        return AABB(min_point, max_point)

    def move(self, amount):
        rads = math.radians(self.rotation_y)
        self.position[0] += amount * math.sin(rads)
        self.position[2] += amount * math.cos(rads)

    def rotate(self, angle):
        self.rotation_y += angle
        if self.rotation_y > 360: self.rotation_y = 0

    def update(self, delta_time, level):
        """
        Aquí es donde el jugador reacciona a los inputs,
        frame por frame.
        """
        # region Lógica de Movimiento (entradas)
        self.is_walking = False 
        move_amount = 0.0
        
        if self.input_manager.is_action_held("move_forward"):
            move_amount += self.movement_speed * delta_time
            self.is_walking = True

        if self.input_manager.is_action_held("move_backward"):
            move_amount -= self.movement_speed * delta_time
            self.is_walking = True
        
        target_dx = 0.0
        target_dz = 0.0
        
        if self.is_walking:
            rads = math.radians(self.rotation_y)
            target_dx = move_amount * math.sin(rads)
            target_dz = move_amount * math.cos(rads)

        if self.input_manager.is_action_held("rotate_left"):
            self.rotate(self.rotate_speed * delta_time)
            
        if self.input_manager.is_action_held("rotate_right"):
            self.rotate(-self.rotate_speed * delta_time)
        # endregion

        # region Lógica de Colisión
        if level and self.is_walking:
            final_dx, final_dz = CollisionSystem.resolve_movement(
                self, 
                target_dx, 
                target_dz, 
                level.solid_colliders
            )
            self.position[0] += final_dx
            self.position[2] += final_dz
        else:
            self.position[0] += target_dx
            self.position[2] += target_dz
        # endregion

        # region Lógica de Interacción
        if self.input_manager.was_action_pressed("interact"):
            self._check_interaction()
        # endregion

        # region Lógica de Animación
        if self.is_walking:
            self.skin.set_state("walk")
        else:
            self.skin.set_state("idle")
            
        if hasattr(self.skin, "update_animation"):
            self.skin.update_animation(delta_time)
        # endregion

        # region Lógica de Sonido
        if self.is_walking and not self.was_walking:
            try:
                self.audio.play_loop_sound("footsteps", volume=0.5)
            except Exception:
                pass
        elif not self.is_walking and self.was_walking:
            try:
                self.audio.stop_sound("footsteps")
            except Exception:
                pass
        # endregion

        self.was_walking = self.is_walking
        
    def _check_interaction(self):
        print("¡Jugador intentó interactuar!")
        pass

    def draw(self):
        glPushMatrix()
        try:
            glTranslatef(self.position[0], self.position[1], self.position[2])
            glRotatef(self.rotation_y, 0, 1, 0)
            self.skin.draw()
        finally:
            glPopMatrix()
