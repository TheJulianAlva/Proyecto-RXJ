from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from utilities import basic_objects as ob
from utilities import materials as Materials

quad = gluNewQuadric()
gluQuadricDrawStyle(quad, GLU_FILL)

posicion_actual = [0.0, 2.0, 0.0]
animation_clock = 0.0

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

current_pose = {

    'pos_x': 0.0,
    'pos_y': 0.0,
    'pos_z': 0.0,
    'root_rotation_y': 0.0,

    # Cabeza y Cuello
    'head_pan': 0.0,  # Rotar cabeza (eje Y)
    'head_tilt': 0.0, # Inclinar cabeza (eje X)
    
    # Torso
    'torso_twist': 0.0, # Girar torso (eje Y)
    'torso_lean': 0.0,  # Inclinarse (eje X)

    # Brazo Derecho
    'r_shoulder_rotate': 20.0,  # Rotar hombro (eje Z)
    'r_shoulder_lift': 0.0,   # Levantar brazo (eje X)

    # Brazo Izquierdo
    'l_shoulder_rotate': -20.0, # Rotar hombro (eje Z)
    'l_shoulder_lift': 0.0,   # Levantar brazo (eje X)

    # Pierna Derecha
    'r_hip_forward': 0.0,   # Pierna (eje X)
    'r_hip_sideways': 0.0, # Pierna (eje Z)

    # Pierna Izquierda
    'l_hip_forward': 0.0,   # Pierna  (eje X)
    'l_hip_sideways': 0.0, # Pierna (eje Z)
}

walk_cycle_anim = [
    {
        'time': 0.0,
        'pose': {
            'pos_y': 0.0,
            'r_hip_forward': 20.0,
            'l_hip_forward': -20.0,
            'r_shoulder_lift': -15.0,
            'l_shoulder_lift': 15.0,
            'torso_twist': -10.0
        }
    },
    {
        'time': 0.5,
        'pose': {
            'pos_y': 0.1,
            'r_hip_forward': -20.0,
            'l_hip_forward': 20.0,
            'r_shoulder_lift': 15.0,
            'l_shoulder_lift': -15.0,
            'torso_twist': 10.0
        }
    },
    {
        'time': 1.0,
        'pose': {
            'pos_y': 0.0,
            'r_hip_forward': 20.0,
            'l_hip_forward': -20.0,
            'r_shoulder_lift': -15.0,
            'l_shoulder_lift': 15.0,
            'torso_twist': -10.0
        }
    }
]

idle_cycle_anim = [
    {
        'time': 0.0,
        'pose': {
            'pos_y': 0.0,
            'r_shoulder_lift': 10.0,
            'l_shoulder_lift': 10.0,
            'torso_tean': -10.0
        }
    },
    {
        'time': 1.0,
        'pose': {
            'pos_y': 0.0,
            'r_shoulder_lift': -10.0,
            'l_shoulder_lift': -10.0,
            'torso_tean': 10.0
        }
    },
    {
        'time': 1.5,
        'pose': {
            'pos_y': 0.0,
            'head_pan': 30.0,
            'head_tilt': -10.0,
            'r_shoulder_lift': 0.0,
            'l_shoulder_lift': 0.0,
            'r_shoulder_rotate': 95.0,
            'l_shoulder_rotate': -95.0,
            'torso_tean': 0.0,
            'r_hip_sideways': 15.0,
            'l_hip_sideways': -5.0,
        }
    },
    {
        'time': 2.0,
        'pose': {
            'pos_y': 0.0,
            'head_pan': 30.0,
            'head_tilt': -10.0,
            'r_shoulder_lift': 0.0,
            'l_shoulder_lift': 0.0,
            'r_shoulder_rotate': 95.0,
            'l_shoulder_rotate': -95.0,
            'torso_tean': 0.0,
            'r_hip_sideways': 15.0,
            'l_hip_sideways': -5.0,
        }
    },
    {
        'time': 3.0,
        'pose': {
            'pos_y': 0.0,
            'head_pan': -30.0,
            'head_tilt': -10.0,
            'r_shoulder_lift': 0.0,
            'l_shoulder_lift': 0.0,
            'r_shoulder_rotate': 105.0,
            'l_shoulder_rotate': -105.0,
            'torso_tean': 0.0,
            'r_hip_sideways': 15.0,
            'l_hip_sideways': -5.0,
        }
    },
    {
        'time': 3.5,
        'pose': {
            'pos_y': 0.0,
            'head_pan': -30.0,
            'head_tilt': -10.0,
            'r_shoulder_lift': 0.0,
            'l_shoulder_lift': 0.0,
            'r_shoulder_rotate': 105.0,
            'l_shoulder_rotate': -105.0,
            'torso_tean': 0.0,
            'r_hip_sideways': 15.0,
            'l_hip_sideways': -5.0,
        }
    },
    {
        'time': 4.5,
        'pose': {
            'pos_y': 0.0,
            'head_pan': 0.0,
            'head_tilt': 0.0,
            'r_shoulder_lift': 0.0,
            'l_shoulder_lift': 0.0,
            'r_shoulder_rotate': 20.0,
            'l_shoulder_rotate': -20.0,
            'torso_tean': 0.0,
            'r_hip_sideways': 0.0,
            'l_hip_sideways': 0.0,
        }
    },
    {
        'time': 5.0,
        'pose': {
            'pos_y': 0.0,
            'r_shoulder_lift': -10.0,
            'l_shoulder_lift': -10.0,
            'torso_tean': 10.0
        }
    },
    {
        'time': 6.0,
        'pose': {
            'pos_y': 0.0,
            'r_shoulder_lift': 10.0,
            'l_shoulder_lift': 10.0,
            'torso_tean': -10.0
        }
    },
    {
        'time': 7.0,
        'pose': {
            'pos_y': 0.0,
            'r_shoulder_lift': -10.0,
            'l_shoulder_lift': -10.0,
            'torso_tean': 10.0
        }
    },
    {
        'time': 8.0,
        'pose': {
            'pos_y': 0.0,
            'r_shoulder_lift': 10.0,
            'l_shoulder_lift': 10.0,
            'torso_tean': -10.0
        }
    },
    {
        'time': 9.0,
        'pose': {
            'pos_y': 0.0,
            'r_shoulder_lift': -10.0,
            'l_shoulder_lift': -10.0,
            'torso_tean': 10.0
        }
    },
    {
        'time': 10.0,
        'pose': {
            'pos_y': 0.0,
            'r_shoulder_lift': 10.0,
            'l_shoulder_lift': 10.0,
            'torso_tean': -10.0
        }
    }
]


current_animation = idle_cycle_anim

def lerp(val_a, val_b, t):
    """
    Interpola linealmente (LERP) entre a y b usando t (0.0 a 1.0)
    """
    return val_a + (val_b - val_a) * t

def update_animation(delta_time):
    """
    Esta función se llama en cada fotograma.
    Actualiza el 'current_pose' basándose en el 'current_animation'.
    'delta_time' es el tiempo (en segundos) desde el último fotograma.
    """
    global animation_clock, current_animation, current_pose, DEFAULT_POSE

    if not current_animation:
        return

    animation_clock += delta_time
    
    # 2. Manejar el bucle de la animación
    animation_duration = current_animation[-1]['time'] # Tiempo del último keyframe
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
            
    # Si no encontramos un 'siguiente' (estamos al final), usamos el primero para el bucle
    if keyframe_next['time'] <= keyframe_prev['time']:
        keyframe_next = current_animation[0]

    time_between_frames = keyframe_next['time'] - keyframe_prev['time']
    if time_between_frames < 0:
        time_between_frames += animation_duration
        
    time_into_segment = animation_clock - keyframe_prev['time']
    t = time_into_segment / time_between_frames if time_between_frames != 0 else 0.0

    # 5. Interpolar TODOS los valores de la pose y guardarlos en current_pose
    for joint_name in current_pose.keys():
        
        default_val = DEFAULT_POSE[joint_name] 

        val_a = keyframe_prev['pose'].get(joint_name, default_val)
        val_b = keyframe_next['pose'].get(joint_name, val_a)
        
        if keyframe_next == current_animation[0]:
             val_b = current_animation[0]['pose'].get(joint_name, val_a)

        current_pose[joint_name] = lerp(val_a, val_b, t)

def draw():
    global posicion_actual
    glPushMatrix()
    glTranslatef(posicion_actual[0], posicion_actual[1], posicion_actual[2])
    _draw_body(quad)
    glPopMatrix()

def _draw_body(quad):
    glTranslatef(current_pose['pos_x'], current_pose['pos_y'], current_pose['pos_z'])
    glRotatef(current_pose['root_rotation_y'], 0, 1, 0)

    # --- body ---
    glPushMatrix()
    try:
        _draw_torso_and_core(quad)
        
        # --- head ---
        glPushMatrix()
        try:
            glTranslatef(0, 2.8, 0) 
            _draw_head_and_neck(quad)
        finally:
            glPopMatrix()

        # --- arms ---
        glPushMatrix()
        try:
            _draw_arm_right(quad)
        finally:
            glPopMatrix()
            
        glPushMatrix()
        try:
            _draw_arm_left(quad)
        finally:
            glPopMatrix()

    finally:
        glPopMatrix()

    # --- legs ---
    glPushMatrix()
    try:
        _draw_leg_right(quad)
    finally:
        glPopMatrix()
    
    glPushMatrix()
    try:
        _draw_leg_left(quad)
    finally:
        glPopMatrix()

def _draw_head_and_neck(quad):
    glRotatef(current_pose['head_pan'], 0, 1, 0)
    glRotatef(current_pose['head_tilt'], 1, 0, 0)
    # head
    Materials.apply_material(Materials.MAT_FABRIC)
    glColor3fv(Materials.C_GREY)
    ob.draw_sphere(quad=quad, scale=[1.5, 1.5, 1.5], translate=[0, 1.2, 0], slices=12, stacks=12) # Ajustado Y
    # mask
    Materials.apply_material(Materials.MAT_PLASTIC)
    glColor3fv(Materials.C_DARK_GREY)
    ob.draw_half_sphere(quad=quad, scale=[0.1, 0.1, 0.35], translate=[0.0, 0.5, -1.3], rotation=[-110, 1, 0, 0])
    ob.draw_half_sphere(quad=quad, scale=[0.35, 0.1, 0.1], translate=[0.0, 0.8, -1.4], rotation=[-90, 1, 0, 0])
    ob.draw_half_sphere(quad=quad, scale=[0.35, 0.1, 0.1], translate=[0.0, 0.5, -1.3], rotation=[-110, 1, 0, 0])
    #face
    _draw_face()
    # neck
    Materials.apply_material(Materials.MAT_FABRIC)
    glColor3fv(Materials.C_LIGHT_ORANGE)
    ob.draw_cylinder(quad=quad, scale=[0.7, 0.7, 0.5],translate=[0, 0, 0], slices=8)

def _draw_torso_and_core(quad):
    glRotatef(current_pose['torso_twist'], 0, 1, 0)
    glRotatef(current_pose['torso_lean'], 1, 0, 0)
    
    # body
    Materials.apply_material(Materials.MAT_FABRIC)
    glColor3fv(Materials.C_LIGHT_ORANGE)
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

def _draw_arm_right(quad):
    Materials.apply_material(Materials.MAT_PLASTIC)
    glColor3fv(Materials.C_LIGHT_ORANGE)
    glTranslatef(1.35, 2.4, 0)
    glRotatef(current_pose['r_shoulder_rotate'], 0, 0, 1)
    glRotatef(current_pose['r_shoulder_lift'], 1, 0, 0)
    
    # shoulder
    ob.draw_sphere(quad=quad, scale=[0.7, 0.55, 0.55], translate=[-0.1, -0.2, 0], rotation=[-25, 0, 0, 1], slices=10, stacks=10)
    # arm
    ob.draw_sphere(quad=quad, scale=[0.38, 0.9, 0.38], translate=[0, -1.0, 0], slices=8, stacks=8)
    # hand
    ob.draw_sphere(quad=quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0], slices=8, stacks=8)

def _draw_arm_left(quad):
    Materials.apply_material(Materials.MAT_PLASTIC)
    glColor3fv(Materials.C_LIGHT_ORANGE)
    glTranslatef(-1.35, 2.4, 0)
    glRotatef(current_pose['l_shoulder_rotate'], 0, 0, 1)
    glRotatef(current_pose['l_shoulder_lift'], 1, 0, 0)
    
    # shoulder
    ob.draw_sphere(quad=quad, scale=[0.7, 0.55, 0.55], translate=[0.1, -0.2, 0], rotation=[25, 0, 0, 1], slices=10, stacks=10)
    # arm
    ob.draw_sphere(quad=quad, scale=[0.38, 0.9, 0.38], translate=[0, -1.0, 0], slices=8, stacks=8)
    # hand
    ob.draw_sphere(quad=quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0], slices=8, stacks=8)

def _draw_leg_right(quad):
    glTranslatef(0.6, 0.4, 0)
    glRotatef(current_pose['r_hip_forward'], 1, 0, 0)
    glRotatef(current_pose['r_hip_sideways'], 0, 0, 1)

    Materials.apply_material(Materials.MAT_METAL)
    glColor3fv(Materials.C_GREY)
    # leg
    ob.draw_cylinder(quad=quad, scale=[0.4, 1.3, 0.4], translate=[0, 0.35, 0], base_radius=0.9, slices=6)
    glColor3fv(Materials.C_DARK_GREY)
    # boot
    ob.draw_cylinder(quad=quad, scale=[0.45, 0.7, 0.45], translate=[0, -0.8, 0], top_radius=0.8, slices=6)
    ob.draw_half_sphere(quad=quad, scale=[0.6, 0.6, 0.8], translate=[0, -1.8, 0.3], slices=10, stacks=10)

def _draw_leg_left(quad):
    glTranslatef(-0.6, 0.4, 0)
    glRotatef(current_pose['l_hip_forward'], 1, 0, 0)
    glRotatef(current_pose['l_hip_sideways'], 0, 0, 1)

    Materials.apply_material(Materials.MAT_METAL)
    glColor3fv(Materials.C_GREY)
    # leg
    ob.draw_cylinder(quad=quad, scale=[0.4, 1.3, 0.4], translate=[0, 0.35, 0], base_radius=0.9, slices=6)
    glColor3fv(Materials.C_DARK_GREY)
    # boot
    ob.draw_cylinder(quad=quad, scale=[0.45, 0.7, 0.45], translate=[0, -0.8, 0], top_radius=0.8, slices=6)
    ob.draw_half_sphere(quad=quad, scale=[0.6, 0.6, 0.8], translate=[0, -1.8, 0.3], slices=10, stacks=10)


def _draw_face():
    # eyes
    glPushMatrix()
    Materials.apply_material(Materials.MAT_FABRIC)
    glColor3fv(Materials.C_LIGHT_ORANGE)
    glTranslatef(0.6, 1.3, 1.3)
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
    glTranslatef(-0.6, 1.3, 1.3)
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
    ob.draw_half_sphere(quad=quad, scale=[0.2, 0.1, 0.1], translate=[0.0, 0.8, 1.45], rotation=[90, 1, 0, 0], slices=8, stacks=8)
    
    # mouth
    ob.draw_half_sphere(quad=quad, scale=[0.5, 0.2, 0.35], translate=[0.0, 0.35, 1.2], rotation=[110, 1, 0, 0], slices=6, stacks=6)
    Materials.apply_material(Materials.MAT_METAL)
    glColor3fv(Materials.C_BLACK)
    ob.draw_half_sphere(quad=quad, scale=[0.2, 0.1, 0.05], translate=[0.0, 0.35, 1.35], rotation=[110, 1, 0, 0], slices=4, stacks=4)
    glPushMatrix()
    glTranslatef(0.15, 0.35, 1.35)
    glRotatef(20, 0, 0, 1)
    ob.draw_half_sphere(quad=quad, scale=[0.15, 0.1, 0.05], translate=[0.0, 0.0, 0.0], rotation=[110, 1, 0, 0], slices=4, stacks=4)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-0.15, 0.35, 1.35)
    glRotatef(-20, 0, 0, 1)
    ob.draw_half_sphere(quad=quad, scale=[0.15, 0.1, 0.05], translate=[0.0, 0.0, 0.0], rotation=[110, 1, 0, 0], slices=4, stacks=4)
    glPopMatrix()
    
