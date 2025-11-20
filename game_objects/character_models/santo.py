from OpenGL.GL import *
from OpenGL.GLU import *
from utilities import basic_objects as ob
from utilities import materials as Materials


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


class SantoSkin:
    def __init__(self):
        self.quad = gluNewQuadric()
        gluQuadricDrawStyle(self.quad, GLU_FILL)
        
        self.animation_clock = 0.0
        self.current_pose = DEFAULT_POSE.copy()
        
        quad = gluNewQuadric()
        gluQuadricDrawStyle(quad, GLU_FILL)

        # Máquina de Estados Interna (Diccionario de animaciones)
        self.animations = {
            "idle": idle_cycle_anim, #
            "walk": walk_cycle_anim  #
        }
        self.current_anim_name = "idle"
        self.current_animation = self.animations["idle"]

    def set_state(self, state_name):
        """
        Cambia el estado de animación.
        Si el estado es el mismo que ya se está reproduciendo, no hace nada.
        """
        if self.current_anim_name != state_name:
            if state_name in self.animations:
                self.current_anim_name = state_name
                self.current_animation = self.animations[state_name]
                self.animation_clock = 0.0

    def update_animation(self, delta_time):
        """Actualiza la interpolación de la pose actual."""
        if not self.current_animation:
            return

        self.animation_clock += delta_time
        
        # 2. Manejar el bucle de la animación
        animation_duration = self.current_animation[-1]['time'] # Tiempo del último keyframe
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
                
        # Si no encontramos un 'siguiente' (estamos al final), usamos el primero para el bucle
        if keyframe_next['time'] <= keyframe_prev['time']:
            keyframe_next = self.current_animation[0]

        time_between_frames = keyframe_next['time'] - keyframe_prev['time']
        if time_between_frames < 0:
            time_between_frames += animation_duration
            
        time_into_segment = self.animation_clock - keyframe_prev['time']
        t = time_into_segment / time_between_frames if time_between_frames != 0 else 0.0

        # 5. Interpolar TODOS los valores de la pose y guardarlos en current_pose
        for joint_name in self.current_pose.keys():
            
            default_val = DEFAULT_POSE[joint_name] 

            val_a = keyframe_prev['pose'].get(joint_name, default_val)
            val_b = keyframe_next['pose'].get(joint_name, val_a)
            
            if keyframe_next == self.current_animation[0]:
                val_b = self.current_animation[0]['pose'].get(joint_name, val_a)

            self.current_pose[joint_name] = self.lerp(val_a, val_b, t)

    def lerp(self, val_a, val_b, t):
        """
        Interpola linealmente (LERP) entre a y b usando t (0.0 a 1.0)
        """
        return val_a + (val_b - val_a) * t

    def draw(self):
        """Dibuja el modelo usando la pose calculada."""
        self._draw_body(self.quad)

    def _draw_body(self, quad):
        glTranslatef(self.current_pose['pos_x'], self.current_pose['pos_y']+1.5, self.current_pose['pos_z'])
        glRotatef(self.current_pose['root_rotation_y'], 0, 1, 0)

        # --- body ---
        glPushMatrix()
        try:
            self._draw_torso_and_core(quad)
            
            # --- head ---
            glPushMatrix()
            try:
                glTranslatef(0, 2.8, 0) 
                self._draw_head_and_neck(quad)
            finally:
                glPopMatrix()

            # --- arms ---
            glPushMatrix()
            try:
                self._draw_arm_right(quad)
            finally:
                glPopMatrix()
                
            glPushMatrix()
            try:
                self._draw_arm_left(quad)
            finally:
                glPopMatrix()

        finally:
            glPopMatrix()

        # --- legs ---
        glPushMatrix()
        try:
            self._draw_leg_right(quad)
        finally:
            glPopMatrix()
        
        glPushMatrix()
        try:
            self._draw_leg_left(quad)
        finally:
            glPopMatrix()

    def _draw_head_and_neck(self, quad):
        glRotatef(self.current_pose['head_pan'], 0, 1, 0)
        glRotatef(self.current_pose['head_tilt'], 1, 0, 0)
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
        self._draw_face(self.quad)
        # neck
        Materials.apply_material(Materials.MAT_FABRIC)
        glColor3fv(Materials.C_LIGHT_ORANGE)
        ob.draw_cylinder(quad=quad, scale=[0.7, 0.7, 0.5],translate=[0, 0, 0], slices=8)

    def _draw_torso_and_core(self, quad):
        glRotatef(self.current_pose['torso_twist'], 0, 1, 0)
        glRotatef(self.current_pose['torso_lean'], 1, 0, 0)
        
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

    def _draw_arm_right(self, quad):
        Materials.apply_material(Materials.MAT_PLASTIC)
        glColor3fv(Materials.C_LIGHT_ORANGE)
        glTranslatef(1.35, 2.4, 0)
        glRotatef(self.current_pose['r_shoulder_rotate'], 0, 0, 1)
        glRotatef(self.current_pose['r_shoulder_lift'], 1, 0, 0)
        
        # shoulder
        ob.draw_sphere(quad=quad, scale=[0.7, 0.55, 0.55], translate=[-0.1, -0.2, 0], rotation=[-25, 0, 0, 1], slices=10, stacks=10)
        # arm
        ob.draw_sphere(quad=quad, scale=[0.38, 0.9, 0.38], translate=[0, -1.0, 0], slices=8, stacks=8)
        # hand
        ob.draw_sphere(quad=quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0], slices=8, stacks=8)

    def _draw_arm_left(self, quad):
        Materials.apply_material(Materials.MAT_PLASTIC)
        glColor3fv(Materials.C_LIGHT_ORANGE)
        glTranslatef(-1.35, 2.4, 0)
        glRotatef(self.current_pose['l_shoulder_rotate'], 0, 0, 1)
        glRotatef(self.current_pose['l_shoulder_lift'], 1, 0, 0)
        
        # shoulder
        ob.draw_sphere(quad=quad, scale=[0.7, 0.55, 0.55], translate=[0.1, -0.2, 0], rotation=[25, 0, 0, 1], slices=10, stacks=10)
        # arm
        ob.draw_sphere(quad=quad, scale=[0.38, 0.9, 0.38], translate=[0, -1.0, 0], slices=8, stacks=8)
        # hand
        ob.draw_sphere(quad=quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0], slices=8, stacks=8)

    def _draw_leg_right(self, quad):
        glTranslatef(0.6, 0.4, 0)
        glRotatef(self.current_pose['r_hip_forward'], 1, 0, 0)
        glRotatef(self.current_pose['r_hip_sideways'], 0, 0, 1)

        Materials.apply_material(Materials.MAT_METAL)
        glColor3fv(Materials.C_GREY)
        # leg
        ob.draw_cylinder(quad=quad, scale=[0.4, 1.3, 0.4], translate=[0, 0.35, 0], base_radius=0.9, slices=6)
        glColor3fv(Materials.C_DARK_GREY)
        # boot
        ob.draw_cylinder(quad=quad, scale=[0.45, 0.7, 0.45], translate=[0, -0.8, 0], top_radius=0.8, slices=6)
        ob.draw_half_sphere(quad=quad, scale=[0.6, 0.6, 0.8], translate=[0, -1.8, 0.3], slices=10, stacks=10)

    def _draw_leg_left(self, quad):
        glTranslatef(-0.6, 0.4, 0)
        glRotatef(self.current_pose['l_hip_forward'], 1, 0, 0)
        glRotatef(self.current_pose['l_hip_sideways'], 0, 0, 1)

        Materials.apply_material(Materials.MAT_METAL)
        glColor3fv(Materials.C_GREY)
        # leg
        ob.draw_cylinder(quad=quad, scale=[0.4, 1.3, 0.4], translate=[0, 0.35, 0], base_radius=0.9, slices=6)
        glColor3fv(Materials.C_DARK_GREY)
        # boot
        ob.draw_cylinder(quad=quad, scale=[0.45, 0.7, 0.45], translate=[0, -0.8, 0], top_radius=0.8, slices=6)
        ob.draw_half_sphere(quad=quad, scale=[0.6, 0.6, 0.8], translate=[0, -1.8, 0.3], slices=10, stacks=10)

    def _draw_face(self, quad):
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
        Materials.apply_material(Materials.MAT_FABRIC)
        glColor3fv(Materials.C_LIGHT_ORANGE)
        glTranslatef(-0.6, 1.3, 1.3)
        glRotatef(-15, 0, 1, 0)
        glRotatef(15, 0, 0, 1)
        glScalef(0.4, 0.4, 0.4)
        ob.draw_half_sphere(quad=quad, scale=[1.0, 1.2, 0.4], translate=[0.0, 0.4, 0.0], rotation=[-15, 1, 0, 0], slices=10, stacks=10)
        Materials.apply_material(Materials.MAT_FABRIC)
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
        