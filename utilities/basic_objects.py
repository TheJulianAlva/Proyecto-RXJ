from OpenGL.GLU import *
from OpenGL.GL import *

# =============================== AUX =================================
def _calculate_crop_uvs(target_w, target_h, img_w, img_h):
    """
    Calcula coordenadas UV para hacer un recorte tipo y mantener la relación de aspecto.
    Retorna (u_min, u_max, v_min, v_max).
    """
    if target_h == 0 or img_h == 0: return (0, 1, 0, 1) # Evitar división por cero

    plane_ratio = target_w / target_h
    img_ratio = img_w / img_h

    u_min, u_max = 0.0, 1.0
    v_min, v_max = 0.0, 1.0

    if plane_ratio > img_ratio:
        # El plano es más ancho que la imagen: Recortar altura (V)
        scale_v = img_ratio / plane_ratio
        center_v = 0.5
        v_min = center_v - (scale_v * 0.5)
        v_max = center_v + (scale_v * 0.5)
    else:
        # El plano es más alto que la imagen: Recortar ancho (U)
        scale_u = plane_ratio / img_ratio
        center_u = 0.5
        u_min = center_u - (scale_u * 0.5)
        u_max = center_u + (scale_u * 0.5)

    return u_min, u_max, v_min, v_max

# ================================= 3D =================================
def draw_plane(size_x=1.0, size_z=1.0, scale=[1, 1, 1], translate=[0, 0, 0], rotation=[0, 0, 0, 1]):
    """
    Dibuja un plano 3D (en el plano XZ, como un suelo).
    """
    glPushMatrix()
    glTranslatef(*translate)
    glRotatef(*rotation)
    glScalef(*scale)

    sx = size_x / 2
    sz = size_z / 2

    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0) # Apuntando hacia arriba
    # Esquina (-X, +Z) -> (0, 0)
    glVertex3f(-sx, 0.0, sz)
    # Esquina (+X, +Z) -> (1, 0)
    glVertex3f(sx, 0.0, sz)
    # Esquina (+X, -Z) -> (1, 1)
    glVertex3f(sx, 0.0, -sz)
    # Esquina (-X, -Z) -> (0, 1)
    glVertex3f(-sx, 0.0, -sz)
    
    glEnd()
    glPopMatrix()

def draw_textured_plane_3d(size_x=1.0, size_z=1.0, scale=[1, 1, 1], translate=[0, 0, 0], rotation=[0, 0, 0, 1]):
    """
    Dibuja un plano 3D (en el plano XZ, como un suelo) con coordenadas de textura.
    ASUME que la textura ya está bindeada (glBindTexture).
    """
    glPushMatrix()
    glTranslatef(*translate)
    glRotatef(*rotation)
    glScalef(*scale)

    sx = size_x / 2
    sz = size_z / 2

    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0) # Apuntando hacia arriba
    # Esquina (-X, +Z) -> (0, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-sx, 0.0, sz)
    # Esquina (+X, +Z) -> (1, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(sx, 0.0, sz)
    # Esquina (+X, -Z) -> (1, 1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(sx, 0.0, -sz)
    # Esquina (-X, -Z) -> (0, 1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-sx, 0.0, -sz)
    
    glEnd()
    glPopMatrix()

def draw_crop_plane_3d(size_x=1.0, size_z=1.0, img_w=100, img_h=100, scale=[1, 1, 1], translate=[0, 0, 0], rotation=[0, 0, 0, 1]):
    """
    Dibuja un plano 3D (en el plano XZ) texturizado manteniendo la relación de aspectos.
    ASUME que la textura ya está bindeada (glBindTexture).

    :param size_x: Tamaño del plano en el eje X.
    :param size_z: Tamaño del plano en el eje Z.
    :param img_w: Ancho original de la imagen (textura) en píxeles.
    :param img_h: Alto original de la imagen (textura) en píxeles.
    :param scale: Lista [x, y, z] para el escalado.
    :param translate: Lista [x, y, z] para la posición.
    :param rotation: Lista [angulo, x, y, z] para la rotación (glRotatef).
    """
    u_min, u_max, v_min, v_max = _calculate_crop_uvs(size_x, size_z, img_w, img_h)

    glPushMatrix()
    glTranslatef(*translate)
    glRotatef(*rotation)
    glScalef(*scale)

    sx = size_x / 2
    sz = size_z / 2

    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)

    # Esquina (-X, +Z) -> UV(min, min)
    glTexCoord2f(u_min, v_min) 
    glVertex3f(-sx, 0.0, sz)

    # Esquina (+X, +Z) -> UV(max, min)
    glTexCoord2f(u_max, v_min)
    glVertex3f(sx, 0.0, sz)

    # Esquina (+X, -Z) -> UV(max, max)
    glTexCoord2f(u_max, v_max)
    glVertex3f(sx, 0.0, -sz)

    # Esquina (-X, -Z) -> UV(min, max)
    glTexCoord2f(u_min, v_max)
    glVertex3f(-sx, 0.0, -sz)
    
    glEnd()
    glPopMatrix()

def draw_cube(size=1.0, scale=[1, 1, 1], translate=[0, 0, 0], rotation=[0, 0, 0, 1]):
    """
    Dibuja un cubo usando GL.
    """
    glPushMatrix()
    glTranslatef(*translate)
    glRotatef(*rotation)
    glScalef(*scale)

    s = size/2

    glBegin(GL_QUADS)
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(-s, -s,  s)
    glVertex3f( s, -s,  s)
    glVertex3f( s,  s,  s)
    glVertex3f(-s,  s,  s)
    
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(-s, -s, -s)
    glVertex3f(-s,  s, -s)
    glVertex3f( s,  s, -s)
    glVertex3f( s, -s, -s)
    
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-s,  s, -s)
    glVertex3f(-s,  s,  s)
    glVertex3f( s,  s,  s)
    glVertex3f( s,  s, -s)
    
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-s, -s, -s)
    glVertex3f( s, -s, -s)
    glVertex3f( s, -s,  s)
    glVertex3f(-s, -s,  s)
    
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f( s, -s, -s)
    glVertex3f( s,  s, -s)
    glVertex3f( s,  s,  s)
    glVertex3f( s, -s,  s)
    
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(-s, -s, -s)
    glVertex3f(-s, -s,  s)
    glVertex3f(-s,  s,  s)
    glVertex3f(-s,  s, -s)
    glEnd()
    glPopMatrix()

def draw_sphere(quad, scale=[1, 1, 1], translate=[0, 0, 0], rotation=[0, 0, 0, 1],
                radius=1.0, slices=16, stacks=16):
    """
    Dibuja una esfera usando gluSphere con transformaciones.
    """
    glPushMatrix()
    glTranslatef(*translate)
    glRotatef(*rotation)
    glScalef(*scale)
    gluSphere(quad, radius, slices, stacks)
    glPopMatrix()

def draw_half_sphere(quad, scale=[1, 1, 1], translate=[0, 0, 0], rotation=[0, 0, 0, 1],
                    radius=1.0, slices=16, stacks=16):
    """
    Dibuja media esfera usando gluSphere con transformaciones.
    """
    clip_plane = [0.0, 1.0, 0.0, 0.0] 

    glPushMatrix()
    glTranslatef(*translate)
    glRotatef(*rotation)
    glScalef(*scale)
    glClipPlane(GL_CLIP_PLANE0, clip_plane)
    glEnable(GL_CLIP_PLANE0)
    gluSphere(quad, radius, slices, stacks)
    glDisable(GL_CLIP_PLANE0)
    glPopMatrix()

def draw_cylinder(quad, scale=[1, 1, 1], translate=[0, 0, 0], rotation=[0, 0, 0, 1],
                  base_radius=1.0, top_radius=1.0, height=1.0, slices=16, stacks=1):
    """
    Dibuja un cilindro usando gluCylinder con transformaciones.
    Si top_radius es 0, se dibuja un cono.
    """
    glPushMatrix()
    glTranslatef(*translate)
    glRotatef(*rotation)
    glScalef(*scale)
    glRotatef(90, 1, 0, 0)
    gluCylinder(quad, base_radius, top_radius, height, slices, stacks)
    glPopMatrix()

def draw_partial_disk(quad, scale=[1, 1, 1], translate=[0, 0, 0], rotation=[0, 0, 0, 1],
                      inner_radius=0.0, outer_radius=1.0, slices=16, loops=1, 
                      start_angle=0.0, sweep_angle=360.0):
    """
    Dibuja un disco parcial (o un disco completo si sweep_angle=360).
    """
    glPushMatrix()
    glTranslatef(*translate)
    glRotatef(*rotation)
    glScalef(*scale)
    gluPartialDisk(quad, inner_radius, outer_radius, slices, loops, start_angle, sweep_angle)
    glPopMatrix()


# ================================= 2D =================================

def draw_pyrect(rect):
    """
    Función para dibujar un pygame.Rect relleno con GL_QUADS.

    :param rect: El rectángulo a dibujar.
    :type rect: pygame.Rect
    """
    glBegin(GL_QUADS)
    glVertex2f(rect.left, rect.top)
    glVertex2f(rect.right, rect.top)
    glVertex2f(rect.right, rect.bottom)
    glVertex2f(rect.left, rect.bottom)
    glEnd()

def draw_pyrect_border(rect):
    """
    Función para dibujar el borde de un pygame.Rect con GL_LINES.

    :param rect: El rectángulo cuyo borde se va a dibujar.
    :type rect: pygame.Rect
    """
    glLineWidth(2.0) # Hacer el borde más grueso
    glBegin(GL_LINE_LOOP)
    glVertex2f(rect.left, rect.top)
    glVertex2f(rect.right, rect.top)
    glVertex2f(rect.right, rect.bottom)
    glVertex2f(rect.left, rect.bottom)
    glEnd()
    glLineWidth(1.0)

def draw_textured_pyrect(rect):
    """
    Dibuja un pygame.Rect relleno con una textura.
    ASUME que la textura ya está bindeada (glBindTexture).
    """
    glBegin(GL_QUADS)
    # Top-Left
    glTexCoord2f(0.0, 1.0)
    glVertex2f(rect.left, rect.top)
    # Top-Right
    glTexCoord2f(1.0, 1.0)
    glVertex2f(rect.right, rect.top)
    # Bottom-Right
    glTexCoord2f(1.0, 0.0)
    glVertex2f(rect.right, rect.bottom)
    # Bottom-Left
    glTexCoord2f(0.0, 0.0)
    glVertex2f(rect.left, rect.bottom)
    glEnd()

def draw_crop_pyrect(rect, img_w, img_h):
    """
    Dibuja un pygame.Rect texturizado manteniendo la relación de aspecto (efecto Crop/Cover).
    ASUME que la textura ya está bindeada.

    :param rect: Objeto pygame.Rect que define el área de dibujo.
    :param img_w: Ancho original de la imagen (textura) en píxeles.
    :param img_h: Alto original de la imagen (textura) en píxeles.
    """
    u_min, u_max, v_min, v_max = _calculate_crop_uvs(rect.width, rect.height, img_w, img_h)

    glBegin(GL_QUADS)
    
    # Top-Left
    glTexCoord2f(u_min, v_max) 
    glVertex2f(rect.left, rect.top)
    
    # Top-Right
    glTexCoord2f(u_max, v_max)
    glVertex2f(rect.right, rect.top)
    
    # Bottom-Right
    glTexCoord2f(u_max, v_min)
    glVertex2f(rect.right, rect.bottom)
    
    # Bottom-Left
    glTexCoord2f(u_min, v_min)
    glVertex2f(rect.left, rect.bottom)
    glEnd()
