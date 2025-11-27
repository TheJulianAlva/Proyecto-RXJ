import cv2
from OpenGL.GL import *
from utilities.basic_objects import draw_textured_pyrect
import pygame

class VideoPlayer:
    """
    Reproductor de video estándar para OpenGL.
    Ideal para cinemáticas, créditos o fondos animados.
    """
    def __init__(self, video_path, width=800, height=600, loop=False):
        """
        :param video_path: Ruta al archivo de video.
        :param width: Ancho visual en pantalla.
        :param height: Alto visual en pantalla.
        :param loop: Si es True, el video se repite infinitamente.
        """
        self.cap = cv2.VideoCapture(video_path)
        self.width = width
        self.height = height
        self.loop = loop
        
        # Banderas de Estado
        self.has_started = False
        self.has_finished = False
        self.is_playing = False

        # FPS nativos del video
        self.video_fps = self.cap.get(cv2.CAP_PROP_FPS)
        if self.video_fps <= 0: 
            self.video_fps = 30.0 
            
        self.frame_duration = 1.0 / self.video_fps
        self.timer = 0.0
        
        # Crear textura OpenGL
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glBindTexture(GL_TEXTURE_2D, 0)
        
        if not self.cap.isOpened():
            print(f"ERROR: No se pudo cargar el video: {video_path}")
            self.has_finished = True

    def play(self):
        """Inicia la reproducción."""
        self.has_started = True
        self.is_playing = True
        self.has_finished = False

    def stop(self):
        """Detiene el video."""
        self.is_playing = False

    def reset(self):
        """Reinicia el video al principio."""
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.has_started = False
        self.has_finished = False
        self.is_playing = False

    def update(self, delta_time):
        """
        Avanza el video respetando su velocidad original.
        """
        if not self.is_playing or self.has_finished:
            return

        self.timer += delta_time
        if self.timer >= self.frame_duration:
            self.timer -= self.frame_duration
            ret, frame = self.cap.read()
            
            if not ret:
                if self.loop:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                else:
                    self.has_finished = True
                    self.is_playing = False
                    print("Video terminado.")
                return
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            h, w, c = frame_rgb.shape
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, frame_rgb)
            glBindTexture(GL_TEXTURE_2D, 0)


    def draw(self, x, y):
        """
        Dibuja el frame actual en la posición dada (2D).
        """
        if not self.has_started: return
        
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glColor3f(1.0, 1.0, 1.0)
        
        x2 = x + self.width
        y2 = y + self.height
        
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(x, y)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(x2, y)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(x2, y2)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(x, y2)
        glEnd()
        glDisable(GL_TEXTURE_2D)

    def release(self):
        self.cap.release()