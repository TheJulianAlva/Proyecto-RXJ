from OpenGL.GLU import *
from OpenGL.GL import *

# ================================= 3D =================================
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
