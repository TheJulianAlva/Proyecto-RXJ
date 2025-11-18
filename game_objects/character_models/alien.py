from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from utilities import basic_objects as ob
from utilities import materials as Materials

quad = gluNewQuadric()
gluQuadricDrawStyle(quad, GLU_FILL)

posicion_actual = [0.0, 2.0, 0.0]
animation_clock = 0.0

# Estos son todos los tipos de movimientos que puede hacer tu monito, tipo "head_pan" hace que mueva la cabeza hacia los lados
# Entonces por ejemplo si quieres que el monito alce el brazo, tienes que modificar el "shoulder_lift"
# el valor que pongas son los angulos que va a rotar el brazo
DEFAULT_POSE= {
    'pos_x': 0.0,
    'pos_y': 0.0,
    'pos_z': 0.0,
    'root_rotation_y': 0.0,
    'head_pan': 0.0,
    'head_tilt': 0.0,
    'torso_twist': 0.0,
    'torso_lean': 0.0,
    'r_shoulder_rotate': 20.0,
    'r_shoulder_lift': 0.0,
    'l_shoulder_rotate': -20.0,
    'l_shoulder_lift': 0.0,
    'r_hip_forward': 0.0,
    'r_hip_sideways': 0.0,
    'l_hip_forward': 0.0,
    'l_hip_sideways': 0.0,
}

current_pose = dict(DEFAULT_POSE)


# Esta es la animación que tiene los puntos claves para la animación
walk_cycle_anim = [
    {
        'time': 0.0,
        'pose': {
            'pos_y': 0.0, 'r_hip_forward': 20.0, 'l_hip_forward': -20.0,
            'r_shoulder_lift': -15.0, 'l_shoulder_lift': 15.0, 'torso_twist': -10.0
        }
    },
    {
        'time': 0.5,
        'pose': {
            'pos_y': 0.1, 'r_hip_forward': -20.0, 'l_hip_forward': 20.0,
            'r_shoulder_lift': 15.0, 'l_shoulder_lift': -15.0, 'torso_twist': 10.0
        }
    },
    {
        'time': 1.0,
        'pose': {
            'pos_y': 0.0, 'r_hip_forward': 20.0, 'l_hip_forward': -20.0,
            'r_shoulder_lift': -15.0, 'l_shoulder_lift': 15.0, 'torso_twist': -10.0
        }
    }
]

salute_cycle_anim = [
    {
        'time': 0.0, 
        'pose': {
            'r_shoulder_rotate': 20.0,
            'l_shoulder_rotate': -20.0,
            'l_shoulder_lift': 0.0,
        }
    },
    
    {
        'time': 0.5, 
        'pose': {
            'l_shoulder_lift': 95.0 
        }
    },
    {
        'time': 1.0, 
        'pose': {
            'l_shoulder_lift': 115.0, 
            'l_shoulder_rotate': 0.0 
        }
    },
    
   
    {
        'time': 1.3, 
        'pose': {
            'l_shoulder_lift': 115.0, 
            'l_shoulder_rotate': 15.0 
        }
    },
    {
        'time': 1.6, 
        'pose': {
            'l_shoulder_lift': 115.0,
            'l_shoulder_rotate': -5.0 
        }
    },
    {
        'time': 1.9, 
        'pose': {
            'l_shoulder_lift': 115.0, 
            'l_shoulder_rotate': 15.0 
        }
    },
    {
        'time': 2.2, 
        'pose': {
            'l_shoulder_lift': 115.0,
            'l_shoulder_rotate': -5.0 
        }
    },
    {
        'time': 2.5, 
        'pose': {
            'l_shoulder_lift': 115.0,
            'l_shoulder_rotate': 0.0 
        }
    },
    
    {
        'time': 3.0, 
        'pose': {
            'l_shoulder_lift': 95.0, 
            'l_shoulder_rotate': -20.0, 
            'r_shoulder_rotate': 20.0,
        }
    },
    {
        'time': 3.5, 
        'pose': {
            'l_shoulder_lift': 0.0, 
            'r_shoulder_rotate': 20.0, 
            'l_shoulder_rotate': -20.0, 
        }
    },
    {
        'time': 8.0, 
        'pose': {
            'r_shoulder_rotate': 20.0,
            'l_shoulder_rotate': -20.0,
            'l_shoulder_lift': 0.0,
        }
    },
]

current_animation = salute_cycle_anim

def lerp(val_a, val_b, t):
    """
    Interpola linealmente (LERP) entre a y b usando t (0.0 a 1.0)
    """
    return val_a + (val_b - val_a) * t

def update_animation(delta_time):
    """
    Actualiza la pose interpolando entre los keyframes de la animación activa.
    """
    global animation_clock, current_animation, current_pose, DEFAULT_POSE

    if not current_animation:
        return

    animation_clock += delta_time
    
    # Manejar el bucle de la animación
    animation_duration = current_animation[-1]['time']
    if animation_clock > animation_duration:
        animation_clock = animation_clock % animation_duration

    keyframe_prev = current_animation[0]
    keyframe_next = current_animation[0]

    for frame in current_animation:
        if frame['time'] <= animation_clock:
            keyframe_prev = frame
        if frame['time'] > animation_clock:
            keyframe_next = frame
            break
            
    # Manejar el salto del último keyframe al primero
    is_looping_segment = keyframe_next['time'] <= keyframe_prev['time']
    
    time_between_frames = keyframe_next['time'] - keyframe_prev['time']
    if time_between_frames < 0:
        time_between_frames += animation_duration
        
    time_into_segment = animation_clock - keyframe_prev['time']
    t = time_into_segment / time_between_frames if time_between_frames != 0 else 0.0

    # Interpolar todos los valores de la pose
    for joint_name in current_pose.keys():
        
        default_val = DEFAULT_POSE[joint_name] 

        val_a = keyframe_prev['pose'].get(joint_name, default_val)
        val_b = keyframe_next['pose'].get(joint_name, val_a)
        
        # Corrección para el bucle (si el siguiente es el primero)
        if is_looping_segment:
             val_b = current_animation[0]['pose'].get(joint_name, default_val) 

        current_pose[joint_name] = lerp(val_a, val_b, t)


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
    glTranslatef(current_pose['pos_x'], current_pose['pos_y'], current_pose['pos_z'])
    glRotatef(current_pose['root_rotation_y'], 0, 1, 0)
    glPushMatrix()
    glRotatef(current_pose['torso_twist'], 0, 1, 0)
    glRotatef(current_pose['torso_lean'], 1, 0, 0)
    # head
    Materials.apply_material(Materials.MAT_PLASTIC)
    glColor3fv(Materials.C_GREEN)
    glPushMatrix()
    glTranslatef(0, 4, 0)
    glRotatef(current_pose['head_pan'], 0, 1, 0)
    glRotatef(current_pose['head_tilt'], 1, 0, 0)
    ob.draw_sphere(quad=quad, scale=[1.5, 1.5, 1.5], translate=[0, 0, 0])
    glPopMatrix()
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
    
    # pants
    ob.draw_sphere(quad=quad, scale=[1.2,1.0,1], translate=[0, .9, 0])
    glPopMatrix() 
    
    # --- arms ---
    glPushMatrix()
    glTranslatef(1.35, 2.4, 0)
    glRotatef(current_pose['r_shoulder_rotate'], 0, 0, 1) # Rotación Z
    glRotatef(current_pose['r_shoulder_lift'], 1, 0, 0)   # Rotación X
    ob.draw_sphere(quad=quad, scale=[0.5, 1, 0.6], translate=[0, -0.85, 0])
    ob.draw_sphere(quad=quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0])
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-1.35, 2.4, 0)
    glRotatef(-current_pose['l_shoulder_lift'], 1, 0, 0)
    glRotatef(current_pose['l_shoulder_rotate'], 0, 0, 1) # Rotación Z (lateral) - APLICADA SEGUNDO
    ob.draw_sphere(quad=quad, scale=[0.5, 1, 0.6], translate=[0, -0.85, 0])
    ob.draw_sphere(quad=quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0])
    glPopMatrix()
    
    # --- legs ---
    glPushMatrix()
    glTranslatef(0.6, 0.4, 0)
    glRotatef(current_pose['r_hip_forward'], 1, 0, 0) # Rotación X (adelante/atrás)
    glRotatef(current_pose['r_hip_sideways'], 0, 0, 1) # Rotación Z (lado a lado)
    ob.draw_cylinder(quad=quad, scale=[0.4, 1.45, 0.4], translate=[0.0, -0.1, 0.0])
    ob.draw_half_sphere(quad=quad, scale=[0.6, 0.6, 1], translate=[0.0, -1.8, 0.3])
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-0.6, 0.4, 0)
    glRotatef(current_pose['l_hip_forward'], 1, 0, 0) # Rotación X (adelante/atrás)
    glRotatef(current_pose['l_hip_sideways'], 0, 0, 1) # Rotación Z (lado a lado)
    ob.draw_cylinder(quad=quad, scale=[0.4, 1.45, 0.4], translate=[0.0, -0.1, 0.0])
    ob.draw_half_sphere(quad=quad, scale=[0.6, 0.6, 1], translate=[0.0, -1.8, 0.3])
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