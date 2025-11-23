class AABB:
    """
    Caja delimitadora alineada al eje (Axis-Aligned Bounding Box).
    Simplificada Plano XZ por decisión arquitectónica.
    """
    def __init__(self, min_point, max_point):
        """
        :param min_point: Lista [x, y, z] o [x, z] con las coordenadas mínimas.
        :param max_point: Lista [x, y, z] o [x, z] con las coordenadas máximas.
        """
        # Aseguramos que min sea menor que max
        self.min_x = min(min_point[0], max_point[0])
        self.max_x = max(min_point[0], max_point[0])
        
        # Usamos el índice 2 para Z si viene en formato 3D [x,y,z], o 1 si es 2D [x,z]
        z_index = 2 if len(min_point) > 2 else 1
        
        self.min_z = min(min_point[z_index], max_point[z_index])
        self.max_z = max(min_point[z_index], max_point[z_index])

    def check_collision(self, other):
        """
        Comprueba si esta caja colisiona con otra caja AABB.
        Retorna True si hay solapamiento.
        """
        # Teorema de Separación de Ejes (versión simple AABB)
        # Si están separados en X O separados en Z, no chocan.
        if self.max_x < other.min_x or self.min_x > other.max_x:
            return False
        if self.max_z < other.min_z or self.min_z > other.max_z:
            return False
        
        return True

    def move(self, dx, dz):
        """Retorna una NUEVA caja desplazada."""
        new_min = [self.min_x + dx, 0, self.min_z + dz]
        new_max = [self.max_x + dx, 0, self.max_z + dz]
        return AABB(new_min, new_max)

    def __repr__(self):
        return f"AABB(x:[{self.min_x:.2f}, {self.max_x:.2f}], z:[{self.min_z:.2f}, {self.max_z:.2f}])"

