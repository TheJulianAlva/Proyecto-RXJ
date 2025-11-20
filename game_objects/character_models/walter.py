from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from utilities import basic_objects as ob
from utilities import materials as Materials

# --- Constantes de Animación ---
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
    # Faciales
    'r_eyebrow_rotate': 0.0, 
    'l_eyebrow_rotate': 0.0, 
    'mouth_scale_y': 1.0
}

idle_cycle_anim = [
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

clap_cycle_anim = [
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


class WalterSkin:
    def __init__(self):
        self.quad = gluNewQuadric()
        gluQuadricDrawStyle(self.quad, GLU_FILL)
        
        self.animation_clock = 0.0
        self.current_pose = DEFAULT_POSE.copy()
        
        self.animations = {
            "idle": clap_cycle_anim,
            "walk": walk_cycle_anim
        }
        self.current_anim_name = "idle"
        self.current_animation = self.animations["idle"]

    def set_state(self, state_name):
        if self.current_anim_name != state_name:
            if state_name in self.animations:
                self.current_anim_name = state_name
                self.current_animation = self.animations[state_name]
                self.animation_clock = 0.0

    def update_animation(self, delta_time):
        if not self.current_animation: return

        self.animation_clock += delta_time
        
        animation_duration = self.current_animation[-1]['time']
        if animation_duration == 0: 
            self.animation_clock = 0
            return

        if self.animation_clock > animation_duration:
            self.animation_clock = self.animation_clock % animation_duration

        keyframe_prev = self.current_animation[0]
        keyframe_next = self.current_animation[0]

        for frame in self.current_animation:
            if frame['time'] <= self.animation_clock:
                keyframe_prev = frame
            if frame['time'] > self.animation_clock:
                keyframe_next = frame
                break
            
        if keyframe_next['time'] <= keyframe_prev['time']:
            keyframe_next = self.current_animation[0]

        time_between_frames = keyframe_next['time'] - keyframe_prev['time']
        if time_between_frames < 0: time_between_frames += animation_duration
        
        time_into_segment = self.animation_clock - keyframe_prev['time']
        t = time_into_segment / time_between_frames if time_between_frames != 0 else 0.0

        for joint_name in self.current_pose.keys():
            default_val = DEFAULT_POSE[joint_name] 
            val_a = keyframe_prev['pose'].get(joint_name, default_val)
            val_b = keyframe_next['pose'].get(joint_name, val_a)
            if keyframe_next == self.current_animation[0]:
                 val_b = self.current_animation[0]['pose'].get(joint_name, val_a)
            self.current_pose[joint_name] = self.lerp(val_a, val_b, t)

    def lerp(self, val_a, val_b, t):
        return val_a + (val_b - val_a) * t

    def draw(self):
        """Dibuja el cuerpo de Walter con todas las animaciones aplicadas"""
        glTranslatef(self.current_pose['pos_x'], self.current_pose['pos_y']+1.5, self.current_pose['pos_z'])
        glRotatef(self.current_pose['root_rotation_y'], 0, 1, 0)
        
        # --- TORSO ---
        glPushMatrix()
        try:
            glRotatef(self.current_pose['torso_twist'], 0, 1, 0)
            glRotatef(self.current_pose['torso_lean'], 1, 0, 0)
            
            # Sombrero
            Materials.apply_material(Materials.MAT_FABRIC)
            glColor3fv(Materials.C_BLACK)
            ob.draw_sphere(quad=self.quad, scale=[2, 0.2, 2], translate=[0, 5, 0])
            ob.draw_cylinder(quad=self.quad, scale=[1, 1.5, 1], translate=[0, 6.5, 0])
            ob.draw_partial_disk(quad=self.quad, scale=[1, 1, 1], translate=[0, 6.5, 0], rotation=[90, 1, 0, 0], slices=32)

            # Cabeza
            self._draw_head()
            
            # Cuello
            Materials.apply_material(Materials.MAT_PLASTIC)
            glColor3fv(Materials.C_LIGHT_YELLOW)
            ob.draw_cylinder(quad=self.quad, scale=[0.7, 0.7, 0.5], translate=[0, 2.8, 0])
            
            # Cuerpo
            glColor3fv(Materials.C_YELLOW)
            ob.draw_half_sphere(quad=self.quad, slices=12, stacks=8, scale=[1.1, 0.3, 1], translate=[0, 2.29, 0])
            ob.draw_cylinder(quad=self.quad, slices=16, scale=[1.1, 1.4, 1], translate=[0, 2.3, 0], top_radius=0.9)
        finally:
            glPopMatrix()

        # --- BRAZOS ---
        glPushMatrix()
        try:
            self._draw_arm_right()
        finally:
            glPopMatrix()
            
        glPushMatrix()
        try:
            self._draw_arm_left()
        finally:
            glPopMatrix()


        # --- PIERNAS ---
        glPushMatrix()
        try:
            self._draw_leg_right()
        finally:
            glPopMatrix()
            
        glPushMatrix()
        try:
            self._draw_leg_left()
        finally:
            glPopMatrix()
        
        # Pantalon
        glColor3fv(Materials.C_YELLOW)
        ob.draw_sphere(quad=self.quad, scale=[1.2, 1, 1], translate=[0, 1, 0])

    def _draw_head(self):
        glPushMatrix()
        glTranslatef(0, 4, 0)
        glRotatef(self.current_pose['head_pan'], 0, 1, 0)
        glRotatef(self.current_pose['head_tilt'], 1, 0, 0)
        
        # Cabeza
        Materials.apply_material(Materials.MAT_PLASTIC)
        glColor3fv(Materials.C_LIGHT_YELLOW)
        ob.draw_sphere(quad=self.quad, scale=[1.5, 1.5, 1.5], translate=[0, 0, 0])
        
        # Cara
        self._draw_face()
        
        glPopMatrix()

    def _draw_face(self):
        # Lógica de Parpadeo
        time_ms = glutGet(GLUT_ELAPSED_TIME)
        blink_cycle_time = 4000
        blink_duration = 150
        time_in_cycle = time_ms % blink_cycle_time
        
        eye_scale_y = 1.0
        if time_in_cycle < blink_duration:
            eye_scale_y = 0.1

        # Ojos
        Materials.apply_material(Materials.MAT_METAL)
        
        # Derecho
        glPushMatrix()
        glTranslatef(0.4, 0.2, 1.5)
        glScalef(1.0, eye_scale_y, 1.0)
        glColor3fv(Materials.C_WHITE)
        ob.draw_partial_disk(quad=self.quad, scale=[0.25, 0.25, 1], translate=[0, 0, 0])
        glColor3fv(Materials.C_BLACK)
        ob.draw_partial_disk(quad=self.quad, scale=[0.12, 0.12, 1], translate=[0, 0, 0.05])
        glPopMatrix()
        
        # Izquierdo
        glPushMatrix()
        glTranslatef(-0.4, 0.2, 1.5)
        glScalef(1.0, eye_scale_y, 1.0)
        glColor3fv(Materials.C_WHITE)
        ob.draw_partial_disk(quad=self.quad, scale=[0.25, 0.25, 1], translate=[0, 0, 0])
        glColor3fv(Materials.C_BLACK)
        ob.draw_partial_disk(quad=self.quad, scale=[0.12, 0.12, 1], translate=[0, 0, 0.05])
        glPopMatrix()

        # Lentes
        glColor3fv(Materials.C_BLACK)
        ob.draw_partial_disk(quad=self.quad, scale=[0.5, 0.5, 1], translate=[0.4, 0.2, 1.55], slices=32, inner_radius=0.8)
        ob.draw_partial_disk(quad=self.quad, scale=[0.5, 0.5, 1], translate=[-0.4, 0.2, 1.55], slices=32, inner_radius=0.8)
        
        # Nariz
        Materials.apply_material(Materials.MAT_PLASTIC)
        glColor3fv(Materials.C_BLACK)
        ob.draw_partial_disk(quad=self.quad, inner_radius=0.7, scale=[0.3, 0.2, 1], translate=[0, -0.3, 1.5], rotation=[180, 0, 0, 1], sweep_angle=180)
        
        # Boca
        glPushMatrix()
        glTranslatef(0, -1.0, 1.4)
        glScalef(1.0, self.current_pose['mouth_scale_y'], 1.0) 
        ob.draw_partial_disk(quad=self.quad, scale=[0.3, 0.2, 1], translate=[0, 0, 0], rotation=[45, 1, 0, 0])
        glPopMatrix()

        # Barba
        Materials.apply_material(Materials.MAT_FABRIC)
        glColor3fv(Materials.C_BROWN)
        ob.draw_half_sphere(quad=self.quad, scale=[0.8, 0.9, 0.3], translate=[0, -1.2, 0.8], rotation=[40, 1, 0, 0])

        # Cejas
        glPushMatrix()
        glTranslatef(0.35, 0.4, 1.52)
        glRotatef(self.current_pose['r_eyebrow_rotate'], 0, 0, 1) 
        ob.draw_partial_disk(quad=self.quad, scale=[0.15, 0.2, 1], translate=[0, 0, 0], rotation=[90, 0, 0, 1], sweep_angle=180)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(-0.35, 0.4, 1.52)
        glRotatef(self.current_pose['l_eyebrow_rotate'], 0, 0, 1) 
        ob.draw_partial_disk(quad=self.quad, scale=[0.15, 0.2, 1], translate=[0, 0, 0], rotation=[90, 0, 0, 1], sweep_angle=180)
        glPopMatrix()

    def _draw_arm_right(self):
        glTranslatef(1.35, 2.4, 0)
        glRotatef(self.current_pose['r_shoulder_rotate'], 0, 0, 1)
        glRotatef(self.current_pose['r_shoulder_lift'], 1, 0, 0)
        
        Materials.apply_material(Materials.MAT_PLASTIC)
        glColor3fv(Materials.C_YELLOW)
        ob.draw_half_sphere(quad=self.quad, scale=[0.6, 1, 0.6], translate=[0, -0.8, 0])
        ob.draw_cylinder(quad=self.quad, scale=[0.38, 1.7, 0.38], translate=[0, -0.3, 0])
        glColor3fv(Materials.C_LIGHT_YELLOW)
        ob.draw_sphere(quad=self.quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0])

    def _draw_arm_left(self):
        glTranslatef(-1.35, 2.4, 0)
        glRotatef(self.current_pose['l_shoulder_rotate'], 0, 0, 1)
        glRotatef(self.current_pose['l_shoulder_lift'], 1, 0, 0)
        
        Materials.apply_material(Materials.MAT_PLASTIC)
        glColor3fv(Materials.C_YELLOW)
        ob.draw_half_sphere(quad=self.quad, scale=[0.6, 1, 0.6], translate=[0, -0.8, 0])
        ob.draw_cylinder(quad=self.quad, scale=[0.38, 1.7, 0.38], translate=[0, -0.3, 0])
        glColor3fv(Materials.C_LIGHT_YELLOW)
        ob.draw_sphere(quad=self.quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0])

    def _draw_leg_right(self):
        glTranslatef(0.6, 0.4, 0)
        glRotatef(self.current_pose['r_hip_forward'], 1, 0, 0)
        glRotatef(self.current_pose['r_hip_sideways'], 0, 0, 1)
        
        glColor3fv(Materials.C_YELLOW)
        ob.draw_cylinder(quad=self.quad, scale=[0.4, 1.45, 0.4], translate=[0, -0.1, 0])
        glColor3fv(Materials.C_WHITE)
        ob.draw_cylinder(quad=self.quad, scale=[0.43, 0.43, 0.43], translate=[0, -1, 0])
        glColor3fv(Materials.C_BLACK)
        ob.draw_half_sphere(quad=self.quad, scale=[0.6, 0.6, 1], translate=[0, -1.8, 0.3])

    def _draw_leg_left(self):
        glTranslatef(-0.6, 0.4, 0)
        glRotatef(self.current_pose['l_hip_forward'], 1, 0, 0)
        glRotatef(self.current_pose['l_hip_sideways'], 0, 0, 1)

        glColor3fv(Materials.C_YELLOW)
        ob.draw_cylinder(quad=self.quad, scale=[0.4, 1.45, 0.4], translate=[0, -0.1, 0])
        glColor3fv(Materials.C_WHITE)
        ob.draw_cylinder(quad=self.quad, scale=[0.43, 0.43, 0.43], translate=[0, -1, 0])
        glColor3fv(Materials.C_BLACK)
        ob.draw_half_sphere(quad=self.quad, scale=[0.6, 0.6, 1], translate=[0, -1.8, 0.3])