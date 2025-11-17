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
    _draw_face()
    glPopMatrix()


def _draw_body():
    # head
    Materials.apply_material(Materials.MAT_FABRIC)
    glColor3fv(Materials.C_GREY)
    ob.draw_sphere(quad=quad, scale=[1.5, 1.5, 1.5], translate=[0, 4, 0], slices=12, stacks=12)
    # mask
    Materials.apply_material(Materials.MAT_PLASTIC)
    glColor3fv(Materials.C_DARK_GREY)
    ob.draw_half_sphere(quad=quad, scale=[0.1, 0.1, 0.35], translate=[0.0, 3.3, -1.3], rotation=[-110, 1, 0, 0])
    ob.draw_half_sphere(quad=quad, scale=[0.35, 0.1, 0.1], translate=[0.0, 3.6, -1.4], rotation=[-90, 1, 0, 0])
    ob.draw_half_sphere(quad=quad, scale=[0.35, 0.1, 0.1], translate=[0.0, 3.3, -1.3], rotation=[-110, 1, 0, 0])
    
    # neck
    Materials.apply_material(Materials.MAT_FABRIC)
    glColor3fv(Materials.C_LIGHT_ORANGE)
    ob.draw_cylinder(quad=quad, scale=[0.7, 0.7, 0.5],translate=[0, 2.8, 0], slices=8)
    # body
    ob.draw_half_sphere(quad=quad, slices=12, stacks=8, scale=[1.1,0.3,1],translate=[0, 2.29, 0])
    ob.draw_cylinder(quad=quad, slices=16, scale=[1.1,1.4,1],translate=[0, 2.3, 0], top_radius=0.8)
    ## chest
    ob.draw_sphere(quad=quad, scale=[0.6, 0.45, 0.20], translate=[-0.5, 2.1, 0.75], rotation=[-25.0, 0, 1, 1], slices=6, stacks=6)
    ob.draw_sphere(quad=quad, scale=[0.6, 0.45, 0.20], translate=[0.5, 2.1, 0.75], rotation=[25.0, 0, 1, 1], slices=6, stacks=6)
    ## core
    ob.draw_sphere(quad=quad, scale=[0.35, 0.25, 0.15], translate=[-0.22, 1.45, 0.8], rotation=[-20.0, 0, 1, 0], slices=6, stacks=6)
    ob.draw_sphere(quad=quad, scale=[0.3, 0.25, 0.15], translate=[-0.2, 1.15, 0.8], rotation=[-20.0, 0, 1, 0], slices=6, stacks=6)
    ob.draw_sphere(quad=quad, scale=[0.35, 0.25, 0.15], translate=[0.22, 1.45, 0.8], rotation=[20.0, 0, 1, 0], slices=6, stacks=6)
    ob.draw_sphere(quad=quad, scale=[0.3, 0.25, 0.15], translate=[0.2, 1.15, 0.8], rotation=[20.0, 0, 1, 0], slices=6, stacks=6)
    # pants
    Materials.apply_material(Materials.MAT_METAL)
    glColor3fv(Materials.C_GREY)
    ob.draw_sphere(quad=quad, scale=[1.0,0.6,0.8], translate=[0, 0.60, 0], slices=12, stacks=12)
        
    # arms
    Materials.apply_material(Materials.MAT_PLASTIC)
    glColor3fv(Materials.C_LIGHT_ORANGE)
    glPushMatrix()
    glTranslatef(1.35, 2.4, 0)
    glRotatef(20, 0, 0, 1)
    ob.draw_sphere(quad=quad, scale=[0.7, 0.55, 0.55], translate=[-0.1, -0.2, 0], rotation=[-25, 0, 0, 1], slices=10, stacks=10)
    ob.draw_sphere(quad=quad, scale=[0.38, 0.9, 0.38], translate=[0, -1.0, 0], slices=8, stacks=8)
    ob.draw_sphere(quad=quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0], slices=8, stacks=8)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-1.35, 2.4, 0)
    glRotatef(-20, 0, 0, 1)
    ob.draw_sphere(quad=quad, scale=[0.7, 0.55, 0.55], translate=[0.1, -0.2, 0], rotation=[25, 0, 0, 1], slices=10, stacks=10)
    #ob.draw_cylinder(quad=quad, scale=[0.38, 1.7, 0.38], translate=[0, -0.3, 0], slices=6)
    ob.draw_sphere(quad=quad, scale=[0.38, 0.9, 0.38], translate=[0, -1.0, 0], slices=8, stacks=8)
    ob.draw_sphere(quad=quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0], slices=8, stacks=8)
    glPopMatrix()

    # legs
    Materials.apply_material(Materials.MAT_METAL)
    glColor3fv(Materials.C_GREY)
    glPushMatrix()
    glTranslatef(0, 0.4, 0)
    ob.draw_cylinder(quad=quad, scale=[0.4, 1.3, 0.4], translate=[0.6, 0.35, 0], base_radius=0.9, slices=6)
    glColor3fv(Materials.C_DARK_GREY)
    ob.draw_cylinder(quad=quad, scale=[0.45, 0.7, 0.45], translate=[0.6, -0.8, 0], top_radius=0.8, slices=6)
    ob.draw_half_sphere(quad=quad, scale=[0.6, 0.6, 0.8], translate=[0.6, -1.8, 0.3], slices=10, stacks=10)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 0.4, 0)
    glColor3fv(Materials.C_GREY)
    ob.draw_cylinder(quad=quad, scale=[0.4, 1.3, 0.4], translate=[-0.6, 0.35, 0], base_radius=0.9, slices=6)
    glColor3fv(Materials.C_DARK_GREY)
    ob.draw_cylinder(quad=quad, scale=[0.45, 0.7, 0.45], translate=[-0.6, -0.8, 0], top_radius=0.8, slices=6)
    ob.draw_half_sphere(quad=quad, scale=[0.6, 0.6, 0.8], translate=[-0.6, -1.8, 0.3], slices=10, stacks=10)
    glPopMatrix()

def _draw_face():
    # eyes
    glPushMatrix()
    Materials.apply_material(Materials.MAT_FABRIC)
    glColor3fv(Materials.C_LIGHT_ORANGE)
    glTranslatef(0.6, 4.1, 1.3)
    glRotatef(15, 0, 1, 0)
    glRotatef(-15, 0, 0, 1)
    glScalef(0.4, 0.4, 0.4)
    ob.draw_half_sphere(quad=quad, scale=[1.0, 1.2, 0.4], translate=[0.0, 0.4, 0.0], rotation=[-15, 1, 0, 0], slices=10, stacks=10)
    Materials.apply_material(Materials.MAT_FABRIC)
    glColor3fv(Materials.C_WHITE)
    ob.draw_half_sphere(quad=quad, scale=[1.0, 1.2, 0.4], translate=[0.0, 0.4, 0.0], rotation=[-195, 1, 0, 0], slices=10, stacks=10)
    glColor3fv(Materials.C_BLACK)
    ob.draw_half_sphere(quad=quad, scale=[0.5, 0.6, 0.2], translate=[-0.15, 0.3, 0.4], rotation=[-195, 1, 0, 0], slices=10, stacks=10)
    glPopMatrix()
    
    glPushMatrix()
    Materials.apply_material(Materials.MAT_PLASTIC)
    glColor3fv(Materials.C_LIGHT_ORANGE)
    glTranslatef(-0.6, 4.1, 1.3)
    glRotatef(-15, 0, 1, 0)
    glRotatef(15, 0, 0, 1)
    glScalef(0.4, 0.4, 0.4)
    ob.draw_half_sphere(quad=quad, scale=[1.0, 1.2, 0.4], translate=[0.0, 0.4, 0.0], rotation=[-15, 1, 0, 0], slices=10, stacks=10)
    Materials.apply_material(Materials.MAT_METAL)
    glColor3fv(Materials.C_WHITE)
    ob.draw_half_sphere(quad=quad, scale=[1.0, 1.2, 0.4], translate=[0.0, 0.4, 0.0], rotation=[-195, 1, 0, 0], slices=10, stacks=10)
    glColor3fv(Materials.C_BLACK)
    ob.draw_half_sphere(quad=quad, scale=[0.5, 0.6, 0.2], translate=[0.15, 0.3, 0.4], rotation=[-195, 1, 0, 0], slices=10, stacks=10)
    glPopMatrix()
    
    # nose
    Materials.apply_material(Materials.MAT_PLASTIC)
    glColor3fv(Materials.C_LIGHT_ORANGE)
    ob.draw_half_sphere(quad=quad, scale=[0.2, 0.1, 0.1], translate=[0.0, 3.6, 1.45], rotation=[90, 1, 0, 0], slices=8, stacks=8)
    
    # mouth
    ob.draw_half_sphere(quad=quad, scale=[0.5, 0.2, 0.35], translate=[0.0, 3.15, 1.2], rotation=[110, 1, 0, 0], slices=6, stacks=6)
    Materials.apply_material(Materials.MAT_METAL)
    glColor3fv(Materials.C_BLACK)
    ob.draw_half_sphere(quad=quad, scale=[0.2, 0.1, 0.05], translate=[0.0, 3.15, 1.35], rotation=[110, 1, 0, 0], slices=4, stacks=4)
    glPushMatrix()
    glTranslatef(0.15, 3.15, 1.35)
    glRotatef(20, 0, 0, 1)
    ob.draw_half_sphere(quad=quad, scale=[0.15, 0.1, 0.05], translate=[0.0, 0.0, 0.0], rotation=[110, 1, 0, 0], slices=4, stacks=4)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-0.15, 3.15, 1.35)
    glRotatef(-20, 0, 0, 1)
    ob.draw_half_sphere(quad=quad, scale=[0.15, 0.1, 0.05], translate=[0.0, 0.0, 0.0], rotation=[110, 1, 0, 0], slices=4, stacks=4)
    glPopMatrix()
    
