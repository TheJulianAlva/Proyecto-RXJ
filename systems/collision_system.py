import math

class CollisionSystem:
    """
    Sistema estático para resolver colisiones entre el jugador y el entorno.
    """
    
    @staticmethod
    def resolve_movement(player, target_dx, target_dz, solid_colliders):
        """
        Intenta mover al jugador verificando colisiones en cada eje.
        Permite 'deslizarse' por las paredes.
        
        :param player: Objeto Player (debe tener método get_aabb()).
        :param target_dx: Movimiento deseado en X.
        :param target_dz: Movimiento deseado en Z.
        :param solid_colliders: Lista de objetos AABB (paredes).
        :return: Una tupla (final_dx, final_dz) con el movimiento permitido.
        """
        
        player_box = player.get_aabb()
        
        # --- EJE X ---
        allowed_dx = target_dx
        if target_dx != 0:
            future_box_x = player_box.move(target_dx, 0)
            
            for wall in solid_colliders:
                if future_box_x.check_collision(wall):
                    allowed_dx = 0
                    break
        
        # --- EJE Z ---
        allowed_dz = target_dz
        if target_dz != 0:
            future_box_z = player_box.move(0, target_dz)
            
            for wall in solid_colliders:
                if future_box_z.check_collision(wall):
                    allowed_dz = 0
                    break
                    
        return allowed_dx, allowed_dz
    
    @staticmethod
    def cast_ray(origin, angle_y, interactables, max_distance = 1):
        """
        Comprueba si un rayo choca con algún objeto interactuable.
        Retorna el objeto o None.
        :param origin: Coordenadas de Player.
        :param angle_y: Rotación en y de Player.
        :param interactables: lista con elementos interactuables.
        :param max_distance: Distancia máxima para poder interactuar.
        :return: 
        """
        rads = math.radians(angle_y)
        dir_x = math.sin(rads)
        dir_z = math.cos(rads)
        
        closest_obj = None
        min_dist = max_distance
        
        for obj in interactables:
            dx = obj.position[0] - origin[0]
            dz = obj.position[2] - origin[2]
            dist_sq = dx*dx + dz*dz
            
            if dist_sq > max_distance * max_distance:
                continue
            
            # Comprobación de ángulo (¿Está frente a mí?)
            to_obj_x = dx / math.sqrt(dist_sq)
            to_obj_z = dz / math.sqrt(dist_sq)
            producto_punto = (dir_x * to_obj_x) + (dir_z * to_obj_z)
            
            if producto_punto > 0.75: # Umbral de "puntería"
                actual_dist = math.sqrt(dist_sq)
                if actual_dist < min_dist:
                    min_dist = actual_dist
                    closest_obj = obj
        
        return closest_obj
    
    
    @staticmethod
    def check_ray_aabb_intersection(origin, angle_y, aabb, max_distance=2.0):
        """
        Verifica si un rayo intersecta con un AABB específico (Algoritmo Slabs 2D).
        
        :param origin: Lista [x, y, z] del origen del rayo.
        :param angle_y: Angulo del rayo en y.
        :param aabb: Instancia de la clase AABB a comprobar.
        :param max_distance: Distancia máxima del rayo.
        :return: True si hay intersección, False si no.
        """
        rads = math.radians(angle_y)
        dir_x = math.sin(rads)
        dir_z = math.cos(rads)
        
        # Evitar división por cero
        if abs(dir_x) < 1e-6: dir_x = 1e-6
        if abs(dir_z) < 1e-6: dir_z = 1e-6

        # Algoritmo Slabs (Intersección Rayo-Caja en 2D)
        t1 = (aabb.min_x - origin[0]) / dir_x
        t2 = (aabb.max_x - origin[0]) / dir_x
        t3 = (aabb.min_z - origin[2]) / dir_z
        t4 = (aabb.max_z - origin[2]) / dir_z

        t_min = max(min(t1, t2), min(t3, t4))
        t_max = min(max(t1, t2), max(t3, t4))

        # Si t_max < 0, la caja está detrás del rayo
        if t_max < 0:
            return False

        # Si t_min > t_max, el rayo no cruza la caja
        if t_min > t_max:
            return False
            
        # Si t_min > max_distance, la caja está demasiado lejos
        if t_min > max_distance:
            return False

        return True
