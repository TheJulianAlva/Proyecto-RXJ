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