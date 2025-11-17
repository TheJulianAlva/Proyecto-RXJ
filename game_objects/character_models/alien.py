from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from assets import basic_objects as ob
from assets import materials as Materials

quad = gluNewQuadric()
gluQuadricDrawStyle(quad, GLU_FILL)

posicion_actual = [0.0, 2.0, 0.0]

def draw():
    global posicion_actual
    glPushMatrix()
    glTranslatef(posicion_actual[0], posicion_actual[1], posicion_actual[2])
    
    #body
    _draw_body()
    #face
    _draw_happy_face()
    glPopMatrix()


def _draw_body():
    # head
    Materials.apply_material(Materials.MAT_PLASTIC)
    glColor3fv(Materials.C_GREEN)
    ob.draw_sphere(quad=quad, scale=[1.5, 1.5, 1.5], translate=[0, 4, 0])
    # neck
    ob.draw_cylinder(quad=quad, scale=[0.7, 0.7, 0.5],translate=[0, 2.8, 0])
    # body
    ob.draw_half_sphere(quad=quad, slices=12, stacks=8, scale=[1.1,0.3,1],translate=[0, 2.29, 0])
    ob.draw_cylinder(quad=quad, slices=16, scale=[1.1,1.4,1],translate=[0, 2.3, 0])
    #ears
    ob.draw_cylinder(quad=quad, scale=[0.2, 1.3, 0.3], translate=[0.8, 5, 0], rotation=[160, 0, 0, 1])
    ob.draw_cylinder(quad=quad, scale=[0.2, 1.3, 0.3], translate=[-0.8, 5, 0], rotation=[190, 0, 0, 1])
    ob.draw_sphere(quad=quad, scale=[0.3, 0.3, 0.3], translate=[1.35, 6.5, 0])
    ob.draw_sphere(quad=quad, scale=[0.3, 0.3, 0.3], translate=[-1.1, 6.55, 0])
        
    # arms
    glPushMatrix()
    glTranslatef(1.35, 2.4, 0)
    glRotatef(20, 0, 0, 1)
    ob.draw_sphere(quad=quad, scale=[0.5, 1, 0.6], translate=[0, -0.85, 0])
    ob.draw_sphere(quad=quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0])
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-1.35, 2.4, 0)
    glRotatef(-20, 0, 0, 1)
    ob.draw_sphere(quad=quad, scale=[0.5, 1, 0.6], translate=[0, -0.85, 0])
    ob.draw_sphere(quad=quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0])
    glPopMatrix()
    
    # pants
    ob.draw_sphere(quad=quad, scale=[1.2,1.0,1], translate=[0, .9, 0])

    # legs
    glPushMatrix()
    glTranslatef(0, 0.4, 0)
    ob.draw_cylinder(quad=quad, scale=[0.4, 1.45, 0.4], translate=[0.6, -0.1, 0])
    ob.draw_half_sphere(quad=quad, scale=[0.6, 0.6, 1], translate=[0.6, -1.8, 0.3])
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 0.4, 0)
    ob.draw_cylinder(quad=quad, scale=[0.4, 1.45, 0.4], translate=[-0.6, -0.1, 0])
    ob.draw_half_sphere(quad=quad, scale=[0.6, 0.6, 1], translate=[-0.6, -1.8, 0.3])
    glPopMatrix()

def _draw_happy_face():
    
    Materials.apply_material(Materials.MAT_METAL)
    glColor3fv(Materials.C_BLACK)

    ob.draw_partial_disk(quad=quad, scale=[0.4, 0.22, 1], rotation=[220, 0, 0, 1], translate=[0.6, 4.1, 1.55])
    ob.draw_partial_disk(quad=quad, scale=[0.4, 0.22, 1], rotation=[320, 0, 0, 1], translate=[-0.5, 4.1, 1.55])
    
    ob.draw_partial_disk(quad=quad, inner_radius=0.85, scale=[0.45, 0.45, 1], translate=[0, 3.9, 1.5], rotation=[200, 0, 0, 1], sweep_angle=60)
    ob.draw_partial_disk(quad=quad, scale=[0.4, 0.22, 1], rotation=[220, 0, 0, 1], translate=[0.6, 4.1, 1.55])
    ob.draw_partial_disk(quad=quad, scale=[0.4, 0.22, 1], rotation=[320, 0, 0, 1], translate=[-0.5, 4.1, 1.55])
    ob.draw_partial_disk(quad=quad, inner_radius=0.85, scale=[0.45, 0.45, 1], translate=[0, 3.9, 1.5], rotation=[200, 0, 0, 1], sweep_angle=60)
