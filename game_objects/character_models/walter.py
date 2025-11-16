from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from assets import basic_objects as ob
from assets import materials as Materials
import math

quad = gluNewQuadric()
gluQuadricDrawStyle(quad, GLU_FILL)

posicion_actual = [0.0, 0.0, 0.0]

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
    # hat - SOMBRERO NEGRO CON DISCO Y CILINDRO
    Materials.apply_material(Materials.MAT_FABRIC)
    glColor3fv(Materials.C_BLACK)
    ob.draw_sphere(quad=quad, scale=[2, 0.2, 2], translate=[0, 5, 0])
    ob.draw_cylinder(quad=quad, scale=[1, 1.5, 1], translate=[0, 6.5, 0])
    ob.draw_partial_disk(quad=quad, scale=[1, 1, 1], translate=[0, 6.5, 0],rotation=[90,1,0,0],slices=32)

    # head
    Materials.apply_material(Materials.MAT_PLASTIC)
    glColor3fv(Materials.C_LIGHT_YELLOW)
    ob.draw_sphere(quad=quad, scale=[1.5, 1.5, 1.5], translate=[0, 4, 0])
    # neck
    ob.draw_cylinder(quad=quad, scale=[0.7, 0.7, 0.5],translate=[0, 2.8, 0])
    # body - CAMBIADO A AMARILLO
    glColor3fv(Materials.C_YELLOW)
    ob.draw_half_sphere(quad=quad, slices=12, stacks=8, scale=[1.1, 0.3, 1],translate=[0, 2.29, 0])
    ob.draw_cylinder(quad=quad, slices=16, scale=[1.1, 1.4, 1],translate=[0, 2.3, 0], top_radius=0.9)


    # arms - CAMBIADO A AMARILLO
    glPushMatrix()
    glTranslatef(1.35, 2.4, 0)
    glRotatef(20, 0, 0, 1)
    glColor3fv(Materials.C_YELLOW)
    ob.draw_half_sphere(quad=quad, scale=[0.6, 1, 0.6], translate=[0, -0.8, 0])
    ob.draw_cylinder(quad=quad, scale=[0.38, 1.7, 0.38], translate=[0, -0.3, 0])
    glColor3fv(Materials.C_LIGHT_YELLOW)
    ob.draw_sphere(quad=quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0])
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-1.35, 2.4, 0)
    glRotatef(-20, 0, 0, 1)
    glColor3fv(Materials.C_YELLOW)
    ob.draw_half_sphere(quad=quad, scale=[0.6, 1, 0.6], translate=[0, -0.8, 0])
    ob.draw_cylinder(quad=quad, scale=[0.38, 1.7, 0.38], translate=[0, -0.3, 0])
    glColor3fv(Materials.C_LIGHT_YELLOW)
    ob.draw_sphere(quad=quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0])
    glPopMatrix()
    
    # Skirt - CAMBIADO A AMARILLO
    glColor3fv(Materials.C_YELLOW)
    ob.draw_sphere(quad=quad, scale=[1.2, 1, 1], translate=[0, 1, 0])
    
    # legs
    glPushMatrix()
    glTranslatef(0, 0.4, 0)
    glColor3fv(Materials.C_YELLOW)
    ob.draw_cylinder(quad=quad, scale=[0.4, 1.45, 0.4], translate=[0.6, -0.1, 0])
    glColor3fv(Materials.C_WHITE)
    ob.draw_cylinder(quad=quad, scale=[0.43, 0.43, 0.43], translate=[0.6, -1, 0])
    glColor3fv(Materials.C_BLACK)
    ob.draw_half_sphere(quad=quad, scale=[0.6, 0.6, 1], translate=[0.6, -1.8, 0.3])
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 0.4, 0)
    glColor3fv(Materials.C_YELLOW)
    ob.draw_cylinder(quad=quad, scale=[0.4, 1.45, 0.4], translate=[-0.6, -0.1, 0])
    glColor3fv(Materials.C_WHITE)
    ob.draw_cylinder(quad=quad, scale=[0.43, 0.43, 0.43], translate=[-0.6, -1, 0])
    glColor3fv(Materials.C_BLACK)
    ob.draw_half_sphere(quad=quad, scale=[0.6, 0.6, 1], translate=[-0.6, -1.8, 0.3])
    glPopMatrix()

def _draw_happy_face():
    # eyes - ROSTRO
    Materials.apply_material(Materials.MAT_METAL)
    glColor3fv(Materials.C_WHITE)
    ob.draw_partial_disk(quad=quad, scale=[0.25, 0.25, 1], translate=[0.4, 4.2, 1.5])
    ob.draw_partial_disk(quad=quad, scale=[0.25, 0.25, 1], translate=[-0.4, 4.2, 1.5])
    glColor3fv(Materials.C_BLACK)
    ob.draw_partial_disk(quad=quad, scale=[0.12, 0.12, 1], translate=[0.4, 4.2, 1.55])
    ob.draw_partial_disk(quad=quad, scale=[0.12, 0.12, 1], translate=[-0.4, 4.2, 1.55])
    
    #Lentes
    ob.draw_partial_disk(quad=quad, scale=[0.5, 0.5, 1], translate=[0.4, 4.2, 1.55],slices=32,inner_radius=0.8)
    ob.draw_partial_disk(quad=quad, scale=[0.5, 0.5, 1], translate=[-0.4, 4.2, 1.55],slices=32,inner_radius=0.8)
    
    #Nariz
    Materials.apply_material(Materials.MAT_PLASTIC)
    glColor3fv(Materials.C_BLACK)
    ob.draw_partial_disk(quad=quad, inner_radius=0.7, scale=[0.3, 0.2, 1], translate=[0, 3.7, 1.5], rotation=[180, 0, 0, 1], sweep_angle=180)
    
    #Boca
    ob.draw_partial_disk(quad=quad, scale=[0.3, 0.2, 1], translate=[0, 3.0, 1.4], rotation=[45, 1, 0, 0])

    #Barba
    Materials.apply_material(Materials.MAT_FABRIC)
    glColor3fv(Materials.C_BROWN)
    ob.draw_half_sphere(quad=quad, scale=[0.8, 0.9, 0.3], translate=[0, 2.8, 0.8],rotation=[40,1,0,0])

    # cejas
    ob.draw_partial_disk(quad=quad, scale=[0.15, 0.2, 1], translate=[0.35, 4.4, 1.52], rotation=[90, 0, 0, 1], sweep_angle=180)
    ob.draw_partial_disk(quad=quad, scale=[0.15, 0.2, 1], translate=[-0.35, 4.4, 1.52], rotation=[90, 0, 0, 1], sweep_angle=180)
    