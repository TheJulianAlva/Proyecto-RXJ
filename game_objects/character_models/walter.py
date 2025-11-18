from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from assets import basic_objects as ob
from assets import materials as Materials

# Variables globales para el sistema de animación (igual que en tu código)
quad = gluNewQuadric()
gluQuadricDrawStyle(quad, GLU_FILL)

# Añadido desde santo.py
posicion_actual = [0.0, 2.0, 0.0]
animation_clock = 0.0

DEFAULT_POSE = {
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
    
    # --- NUEVOS CONTROLES FACIALES ---
    'r_eyebrow_rotate': 0.0, # Rotación Ceja Derecha
    'l_eyebrow_rotate': 0.0, # Rotación Ceja Izquierda
    'mouth_scale_y': 1.0     # Escala vertical de la boca
}

current_pose = {
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

    # --- NUEVOS CONTROLES FACIALES ---
    'r_eyebrow_rotate': 0.0,
    'l_eyebrow_rotate': 0.0,
    'mouth_scale_y': 1.0
}

# --- INICIO BLOQUE DE ANIMACIONES ---

# Animación de "Actividad de Vida"
idle_cycle_anim = [
    # ... (animación idle existente)
    {
        'time': 0.0,
        'pose': {
            'r_shoulder_lift': 10.0,
            'l_shoulder_lift': 10.0,
            'torso_lean': -5.0,
            'head_tilt': -5.0
        }
    },
    {
        'time': 2.0,
        'pose': {
            'r_shoulder_lift': -5.0,
            'l_shoulder_lift': -5.0,
            'torso_lean': 5.0,
            'head_tilt': 5.0
        }
    },
    {
        'time': 4.0,
        'pose': {
            'r_shoulder_lift': 10.0,
            'l_shoulder_lift': 10.0,
            'torso_lean': -5.0,
            'head_tilt': -5.0
        }
    }
]

wave_animation = [
    # ... (animación wave existente)
]

dance_animation = [
    # ... (animación dance existente)
]

jump_animation = [
    # ... (animación jump existente)
]

# --- NUEVA ANIMACIÓN DE PREOCUPACIÓN / NERVIOSISMO ---
worry_animation = [
    {
        'time': 0.0, # Inicio
        'pose': {
            # Cara preocupada
            'r_eyebrow_rotate': 25.0,  # Ceja derecha arriba (interna)
            'l_eyebrow_rotate': -25.0, # Ceja izquierda arriba (interna)
            'mouth_scale_y': 2.0,      # Boca grande (abierta)
            # Brazos nerviosos (posición 1)
            'r_shoulder_lift': 15.0,
            'l_shoulder_lift': 15.0,
            'torso_lean': -3.0 # Ligera inclinación
        }
    },
    {
        'time': 0.4, # Mitad del movimiento de brazos
        'pose': {
            'r_eyebrow_rotate': 25.0,
            'l_eyebrow_rotate': -25.0,
            'mouth_scale_y': 2.0,
            # Brazos nerviosos (posición 2)
            'r_shoulder_lift': -15.0,
            'l_shoulder_lift': -15.0,
            'torso_lean': 3.0 # Balanceo
        }
    },
    {
        'time': 0.8, # Regreso al inicio para bucle
        'pose': {
            'r_eyebrow_rotate': 25.0,
            'l_eyebrow_rotate': -25.0,
            'mouth_scale_y': 2.0,
            'r_shoulder_lift': 15.0,
            'l_shoulder_lift': 15.0,
            'torso_lean': -3.0
        }
    }
]
# --- NUEVA ANIMACIÓN DE APLAUSO ---
clap_animation = [
    {
        'time': 0.0, # Posición 1: Brazos abiertos
        'pose': {
            'r_shoulder_rotate': 0.0,  # Brazo horizontal
            'l_shoulder_rotate': 0.0,  # Brazo horizontal
            'r_shoulder_lift': 10.0,   # Ligeramente al frente
            'l_shoulder_lift': 10.0,   # Ligeramente al frente (MISMA DIRECCIÓN que el derecho)
            # Resetear cara de preocupación
            'r_eyebrow_rotate': 0.0,
            'l_eyebrow_rotate': 0.0,
            'mouth_scale_y': 1.0
        }
    },
    {
        'time': 0.15, # Posición 2: ¡Aplauso! (Manos "juntas")
        'pose': {
            'r_shoulder_rotate': 0.0,
            'l_shoulder_rotate': 0.0,
            'r_shoulder_lift': -80.0,   # Brazo al frente (lo más que se puede)
            'l_shoulder_lift': -80.0    # Brazo al frente (lo más que se puede)
        }
    },
    {
        'time': 0.4, # Posición 3: Abriendo de nuevo
        'pose': {
            'r_shoulder_rotate': 0.0,
            'l_shoulder_rotate': 0.0,
            'r_shoulder_lift': 10.0,
            'l_shoulder_lift': 10.0
        }
    },
    {
        'time': 0.55, # Posición 4: ¡Segundo Aplauso!
        'pose': {
            'r_shoulder_rotate': 0.0,
            'l_shoulder_rotate': 0.0,
            'r_shoulder_lift': -80.0,
            'l_shoulder_lift': -80.0
        }
    },
    {
        'time': 0.8, # Vuelta al inicio del bucle
        'pose': {
            'r_shoulder_rotate': 0.0,
            'l_shoulder_rotate': 0.0,
            'r_shoulder_lift': 10.0,
            'l_shoulder_lift': 10.0
        }
    }
]
# --- FIN DE ANIMACIONES ---


# (Puedes cambiar esto para probar la nueva animación)
#current_animation = idle_cycle_anim
#current_animation = worry_animation
current_animation = clap_animation

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
    if animation_duration == 0: # Evitar división por cero si la animación es un solo frame
        animation_clock = 0
        return

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
    _draw_body(quad) # Se pasa 'quad'
    glPopMatrix()

def _draw_body(quad): # Se acepta 'quad'
    """Dibuja el cuerpo de Walter con todas las animaciones aplicadas"""
    
    # Transformaciones raíz añadidas desde santo.py
    glTranslatef(current_pose['pos_x'], current_pose['pos_y'], current_pose['pos_z'])
    glRotatef(current_pose['root_rotation_y'], 0, 1, 0)
    
    # --- TORSO CON ANIMACIONES ---
    glPushMatrix()
    try:
        glRotatef(current_pose['torso_twist'], 0, 1, 0)
        glRotatef(current_pose['torso_lean'], 1, 0, 0)
        
        # Sombrero
        Materials.apply_material(Materials.MAT_FABRIC)
        glColor3fv(Materials.C_BLACK)
        ob.draw_sphere(quad=quad, scale=[2, 0.2, 2], translate=[0, 5, 0])
        ob.draw_cylinder(quad=quad, scale=[1, 1.5, 1], translate=[0, 6.5, 0])
        ob.draw_partial_disk(quad=quad, scale=[1, 1, 1], translate=[0, 6.5, 0], rotation=[90, 1, 0, 0], slices=32)

        # Cabeza con animaciones
        _draw_head(quad) # Se pasa 'quad'
        
        # Cuello
        Materials.apply_material(Materials.MAT_PLASTIC)
        glColor3fv(Materials.C_LIGHT_YELLOW)
        ob.draw_cylinder(quad=quad, scale=[0.7, 0.7, 0.5], translate=[0, 2.8, 0])
        
        # Cuerpo
        glColor3fv(Materials.C_YELLOW)
        ob.draw_half_sphere(quad=quad, slices=12, stacks=8, scale=[1.1, 0.3, 1], translate=[0, 2.29, 0])
        ob.draw_cylinder(quad=quad, slices=16, scale=[1.1, 1.4, 1], translate=[0, 2.3, 0], top_radius=0.9)
    finally:
        glPopMatrix()

    # --- BRAZOS CON ANIMACIONES ---
    glPushMatrix()
    try:
        _draw_arm_right(quad) # Se pasa 'quad'
    finally:
        glPopMatrix()
        
    glPushMatrix()
    try:
        _draw_arm_left(quad) # Se pasa 'quad'
    finally:
        glPopMatrix()


    # --- PIERNAS CON ANIMACIONES ---
    glPushMatrix()
    try:
        _draw_leg_right(quad) # Se pasa 'quad'
    finally:
        glPopMatrix()
        
    glPushMatrix()
    try:
        _draw_leg_left(quad) # Se pasa 'quad'
    finally:
        glPopMatrix()
    
    # Falda
    glColor3fv(Materials.C_YELLOW)
    ob.draw_sphere(quad=quad, scale=[1.2, 1, 1], translate=[0, 1, 0])

def _draw_head(quad): # Se acepta 'quad'
    """Dibuja la cabeza con animaciones"""
    glPushMatrix()
    glTranslatef(0, 4, 0)
    glRotatef(current_pose['head_pan'], 0, 1, 0)
    glRotatef(current_pose['head_tilt'], 1, 0, 0)
    
    # Cabeza
    Materials.apply_material(Materials.MAT_PLASTIC)
    glColor3fv(Materials.C_LIGHT_YELLOW)
    ob.draw_sphere(quad=quad, scale=[1.5, 1.5, 1.5], translate=[0, 0, 0])
    
    # Cara
    _draw_face(quad) # Se pasa 'quad'
    
    glPopMatrix()

# --- FUNCIÓN _draw_face MODIFICADA ---
def _draw_face(quad): # Se acepta 'quad'
    """Dibuja la cara de Walter (con parpadeo y animación facial)"""
    
    # --- Lógica de Parpadeo Constante ---
    time_ms = glutGet(GLUT_ELAPSED_TIME)
    blink_cycle_time = 4000 # Parpadea cada 4 segundos
    blink_duration = 150 # El parpadeo dura 150ms
    time_in_cycle = time_ms % blink_cycle_time
    
    eye_scale_y = 1.0 # Ojo abierto por defecto
    if time_in_cycle < blink_duration:
        eye_scale_y = 0.1 # Ojo cerrado (escalado a 10%)
    # --- Fin Lógica de Parpadeo ---

    # Ojos (con parpadeo)
    Materials.apply_material(Materials.MAT_METAL)
    
    # Ojo derecho (con parpadeo)
    glPushMatrix()
    glTranslatef(0.4, 0.2, 1.5) # Posición del ojo
    glScalef(1.0, eye_scale_y, 1.0) # Escala para parpadear
    glColor3fv(Materials.C_WHITE)
    ob.draw_partial_disk(quad=quad, scale=[0.25, 0.25, 1], translate=[0, 0, 0])
    glColor3fv(Materials.C_BLACK)
    ob.draw_partial_disk(quad=quad, scale=[0.12, 0.12, 1], translate=[0, 0, 0.05])
    glPopMatrix()
    
    # Ojo izquierdo (con parpadeo)
    glPushMatrix()
    glTranslatef(-0.4, 0.2, 1.5) # Posición del ojo
    glScalef(1.0, eye_scale_y, 1.0) # Escala para parpadear
    glColor3fv(Materials.C_WHITE)
    ob.draw_partial_disk(quad=quad, scale=[0.25, 0.25, 1], translate=[0, 0, 0])
    glColor3fv(Materials.C_BLACK)
    ob.draw_partial_disk(quad=quad, scale=[0.12, 0.12, 1], translate=[0, 0, 0.05])
    glPopMatrix()

    # Lentes (se dibujan fuera del Push/Pop de escala para que no parpadeen)
    glColor3fv(Materials.C_BLACK)
    ob.draw_partial_disk(quad=quad, scale=[0.5, 0.5, 1], translate=[0.4, 0.2, 1.55], slices=32, inner_radius=0.8)
    ob.draw_partial_disk(quad=quad, scale=[0.5, 0.5, 1], translate=[-0.4, 0.2, 1.55], slices=32, inner_radius=0.8)
    
    # Nariz
    Materials.apply_material(Materials.MAT_PLASTIC)
    glColor3fv(Materials.C_BLACK)
    ob.draw_partial_disk(quad=quad, inner_radius=0.7, scale=[0.3, 0.2, 1], translate=[0, -0.3, 1.5], rotation=[180, 0, 0, 1], sweep_angle=180)
    
    # --- Boca (con animación) ---
    glPushMatrix()
    glTranslatef(0, -1.0, 1.4) # Posición de la boca
    # Aplicar escala de animación (Y)
    glScalef(1.0, current_pose['mouth_scale_y'], 1.0) 
    ob.draw_partial_disk(quad=quad, scale=[0.3, 0.2, 1], translate=[0, 0, 0], rotation=[45, 1, 0, 0])
    glPopMatrix()
    # --- Fin Boca ---

    # Barba
    Materials.apply_material(Materials.MAT_FABRIC)
    glColor3fv(Materials.C_BROWN)
    ob.draw_half_sphere(quad=quad, scale=[0.8, 0.9, 0.3], translate=[0, -1.2, 0.8], rotation=[40, 1, 0, 0])

    # --- Cejas (con animación) ---
    # Ceja Derecha
    glPushMatrix()
    glTranslatef(0.35, 0.4, 1.52) # Posición ceja derecha
    # Aplicar rotación de animación (Z)
    glRotatef(current_pose['r_eyebrow_rotate'], 0, 0, 1) 
    ob.draw_partial_disk(quad=quad, scale=[0.15, 0.2, 1], translate=[0, 0, 0], rotation=[90, 0, 0, 1], sweep_angle=180)
    glPopMatrix()
    
    # Ceja Izquierda
    glPushMatrix()
    glTranslatef(-0.35, 0.4, 1.52) # Posición ceja izquierda
    # Aplicar rotación de animación (Z)
    glRotatef(current_pose['l_eyebrow_rotate'], 0, 0, 1) 
    ob.draw_partial_disk(quad=quad, scale=[0.15, 0.2, 1], translate=[0, 0, 0], rotation=[90, 0, 0, 1], sweep_angle=180)
    glPopMatrix()
    # --- Fin Cejas ---

# --- FIN DE FUNCIÓN MODIFICADA ---


def _draw_arm_right(quad): # Se acepta 'quad'
    """Dibuja el brazo derecho con animaciones"""
    # El push/pop matrix se maneja en _draw_body
    glTranslatef(1.35, 2.4, 0)
    glRotatef(current_pose['r_shoulder_rotate'], 0, 0, 1)
    glRotatef(current_pose['r_shoulder_lift'], 1, 0, 0)
    
    Materials.apply_material(Materials.MAT_PLASTIC)
    glColor3fv(Materials.C_YELLOW)
    ob.draw_half_sphere(quad=quad, scale=[0.6, 1, 0.6], translate=[0, -0.8, 0])
    ob.draw_cylinder(quad=quad, scale=[0.38, 1.7, 0.38], translate=[0, -0.3, 0])
    glColor3fv(Materials.C_LIGHT_YELLOW)
    ob.draw_sphere(quad=quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0])

def _draw_arm_left(quad): # Se acepta 'quad'
    """Dibuja el brazo izquierdo con animaciones"""
    # El push/pop matrix se maneja en _draw_body
    glTranslatef(-1.35, 2.4, 0)
    glRotatef(current_pose['l_shoulder_rotate'], 0, 0, 1)
    glRotatef(current_pose['l_shoulder_lift'], 1, 0, 0)
    
    Materials.apply_material(Materials.MAT_PLASTIC)
    glColor3fv(Materials.C_YELLOW)
    ob.draw_half_sphere(quad=quad, scale=[0.6, 1, 0.6], translate=[0, -0.8, 0])
    ob.draw_cylinder(quad=quad, scale=[0.38, 1.7, 0.38], translate=[0, -0.3, 0])
    glColor3fv(Materials.C_LIGHT_YELLOW)
    ob.draw_sphere(quad=quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0])

def _draw_leg_right(quad): # Se acepta 'quad'
    """Dibuja la pierna derecha con animaciones"""
    # El push/pop matrix se maneja en _draw_body
    glTranslatef(0.6, 0.4, 0)
    glRotatef(current_pose['r_hip_forward'], 1, 0, 0)
    glRotatef(current_pose['r_hip_sideways'], 0, 0, 1)
    
    glColor3fv(Materials.C_YELLOW)
    ob.draw_cylinder(quad=quad, scale=[0.4, 1.45, 0.4], translate=[0, -0.1, 0])
    glColor3fv(Materials.C_WHITE)
    ob.draw_cylinder(quad=quad, scale=[0.43, 0.43, 0.43], translate=[0, -1, 0])
    glColor3fv(Materials.C_BLACK)
    ob.draw_half_sphere(quad=quad, scale=[0.6, 0.6, 1], translate=[0, -1.8, 0.3])

def _draw_leg_left(quad): # Se acepta 'quad'
    """Dibuja la pierna izquierda con animaciones"""
    # El push/pop matrix se maneja en _draw_body
    glTranslatef(-0.6, 0.4, 0)
    glRotatef(current_pose['l_hip_forward'], 1, 0, 0)
    glRotatef(current_pose['l_hip_sideways'], 0, 0, 1)

    glColor3fv(Materials.C_YELLOW)
    ob.draw_cylinder(quad=quad, scale=[0.4, 1.45, 0.4], translate=[0, -0.1, 0])
    glColor3fv(Materials.C_WHITE)
    ob.draw_cylinder(quad=quad, scale=[0.43, 0.43, 0.43], translate=[0, -1, 0])
    glColor3fv(Materials.C_BLACK)
    ob.draw_half_sphere(quad=quad, scale=[0.6, 0.6, 1], translate=[0, -1.8, 0.3])