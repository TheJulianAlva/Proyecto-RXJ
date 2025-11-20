from OpenGL.GL import *
from OpenGL.GLU import *
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
}

# Animaciones
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

class AlienSkin:
    def __init__(self):
        self.quad = gluNewQuadric()
        gluQuadricDrawStyle(self.quad, GLU_FILL)
        
        self.animation_clock = 0.0
        self.current_pose = DEFAULT_POSE.copy()
        
        # Máquina de Estados
        self.animations = {
            "idle": salute_cycle_anim,
            "walk": walk_cycle_anim
        }
        self.current_anim_name = "idle"
        self.current_animation = self.animations["idle"]

    def set_state(self, state_name):
        """Cambia el estado de animación."""
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
        
        animation_duration = self.current_animation[-1]['time']
        if animation_duration == 0: return

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
        if time_between_frames < 0:
            time_between_frames += animation_duration
            
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
        """Dibuja el modelo."""
        self._draw_body()

    def _draw_body(self):
        glTranslatef(self.current_pose['pos_x'], self.current_pose['pos_y']+1.5, self.current_pose['pos_z'])
        glRotatef(self.current_pose['root_rotation_y'], 0, 1, 0)
        
        glPushMatrix()
        glRotatef(self.current_pose['torso_twist'], 0, 1, 0)
        glRotatef(self.current_pose['torso_lean'], 1, 0, 0)
        
        # head
        Materials.apply_material(Materials.MAT_PLASTIC)
        glColor3fv(Materials.C_GREEN)
        glPushMatrix()
        glTranslatef(0, 4, 0)
        glRotatef(self.current_pose['head_pan'], 0, 1, 0)
        glRotatef(self.current_pose['head_tilt'], 1, 0, 0)
        ob.draw_sphere(quad=self.quad, scale=[1.5, 1.5, 1.5], translate=[0, 0, 0])
        self._draw_happy_face()
        glPopMatrix()
        
        # neck
        Materials.apply_material(Materials.MAT_PLASTIC)
        glColor3fv(Materials.C_GREEN)
        ob.draw_cylinder(quad=self.quad, scale=[0.7, 0.7, 0.5],translate=[0, 2.8, 0])
        # body
        ob.draw_half_sphere(quad=self.quad, slices=12, stacks=8, scale=[1.1,0.3,1],translate=[0, 2.29, 0])
        ob.draw_cylinder(quad=self.quad, slices=16, scale=[1.1,1.4,1],translate=[0, 2.3, 0])
        #ears
        ob.draw_cylinder(quad=self.quad, scale=[0.2, 1.3, 0.3], translate=[0.8, 5, 0], rotation=[160, 0, 0, 1])
        ob.draw_cylinder(quad=self.quad, scale=[0.2, 1.3, 0.3], translate=[-0.8, 5, 0], rotation=[190, 0, 0, 1])
        ob.draw_sphere(quad=self.quad, scale=[0.3, 0.3, 0.3], translate=[1.35, 6.5, 0])
        ob.draw_sphere(quad=self.quad, scale=[0.3, 0.3, 0.3], translate=[-1.1, 6.55, 0])
        
        # pants
        ob.draw_sphere(quad=self.quad, scale=[1.2,1.0,1], translate=[0, .9, 0])
        glPopMatrix() 
        
        # --- arms ---
        glPushMatrix()
        glTranslatef(1.35, 2.4, 0)
        glRotatef(self.current_pose['r_shoulder_rotate'], 0, 0, 1) 
        glRotatef(self.current_pose['r_shoulder_lift'], 1, 0, 0)   
        ob.draw_sphere(quad=self.quad, scale=[0.5, 1, 0.6], translate=[0, -0.85, 0])
        ob.draw_sphere(quad=self.quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0])
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-1.35, 2.4, 0)
        glRotatef(-self.current_pose['l_shoulder_lift'], 1, 0, 0)
        glRotatef(self.current_pose['l_shoulder_rotate'], 0, 0, 1) 
        ob.draw_sphere(quad=self.quad, scale=[0.5, 1, 0.6], translate=[0, -0.85, 0])
        ob.draw_sphere(quad=self.quad, scale=[0.48, 0.48, 0.48], translate=[0, -1.9, 0])
        glPopMatrix()
        
        # --- legs ---
        glPushMatrix()
        glTranslatef(0.6, 0.4, 0)
        glRotatef(self.current_pose['r_hip_forward'], 1, 0, 0) 
        glRotatef(self.current_pose['r_hip_sideways'], 0, 0, 1) 
        ob.draw_cylinder(quad=self.quad, scale=[0.4, 1.45, 0.4], translate=[0.0, -0.1, 0.0])
        ob.draw_half_sphere(quad=self.quad, scale=[0.6, 0.6, 1], translate=[0.0, -1.8, 0.3])
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(-0.6, 0.4, 0)
        glRotatef(self.current_pose['l_hip_forward'], 1, 0, 0) 
        glRotatef(self.current_pose['l_hip_sideways'], 0, 0, 1) 
        ob.draw_cylinder(quad=self.quad, scale=[0.4, 1.45, 0.4], translate=[0.0, -0.1, 0.0])
        ob.draw_half_sphere(quad=self.quad, scale=[0.6, 0.6, 1], translate=[0.0, -1.8, 0.3])
        glPopMatrix()

    def _draw_happy_face(self):
        Materials.apply_material(Materials.MAT_METAL)
        glColor3fv(Materials.C_BLACK)

        # Ojos y Boca
        ob.draw_partial_disk(quad=self.quad, scale=[0.4, 0.22, 1], rotation=[220, 0, 0, 1], translate=[0.6, 0.1, 1.55])
        ob.draw_partial_disk(quad=self.quad, scale=[0.4, 0.22, 1], rotation=[320, 0, 0, 1], translate=[-0.5, 0.1, 1.55])
        
        ob.draw_partial_disk(quad=self.quad, inner_radius=0.85, scale=[0.45, 0.45, 1], translate=[0, -0.1, 1.5], rotation=[200, 0, 0, 1], sweep_angle=60)
        ob.draw_partial_disk(quad=self.quad, scale=[0.4, 0.22, 1], rotation=[220, 0, 0, 1], translate=[0.6, 0.1, 1.55])
        ob.draw_partial_disk(quad=self.quad, scale=[0.4, 0.22, 1], rotation=[320, 0, 0, 1], translate=[-0.5, 0.1, 1.55])
        ob.draw_partial_disk(quad=self.quad, inner_radius=0.85, scale=[0.45, 0.45, 1], translate=[0, -0.1, 1.5], rotation=[200, 0, 0, 1], sweep_angle=60)