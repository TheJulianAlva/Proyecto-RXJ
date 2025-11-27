import pygame
import os

class AudioManager:
    """Singleton para manejar música y efectos simples."""
    _instance = None

    @staticmethod
    def instance():
        if AudioManager._instance is None:
            AudioManager._instance = AudioManager()
        return AudioManager._instance

    def __init__(self):
        if AudioManager._instance is not None:
            raise Exception("AudioManager es un singleton. Usa .instance()")
        # Inicializar el mezclador de pygame con valores razonables
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Advertencia: No se pudo inicializar pygame.mixer: {e}")
        self.current_music = None
        self.is_playing = False
        self.volume = 0.6
        # SFX management
        self.sounds = {}  # name -> pygame.mixer.Sound
        self.sfx_channels = {}  # name -> Channel

    def play_music_loop(self, file_path, loops=-1, volume=0.6):
        """Carga y reproduce música en loop (-1 infinito)."""
        if not os.path.exists(file_path):
            print(f"AudioManager: archivo de audio no encontrado: {file_path}")
            return False
        try:
            # Si hay música previa, detenerla
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()

            pygame.mixer.music.load(file_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops=loops)
            self.current_music = file_path
            self.is_playing = True
            self.volume = volume
            return True
        except Exception as e:
            print(f"AudioManager: Error al reproducir música {file_path}: {e}")
            return False

    def stop_music(self):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        self.is_playing = False

    def pause_music(self):
        try:
            pygame.mixer.music.pause()
        except Exception:
            pass
        self.is_playing = False

    def unpause_music(self):
        try:
            pygame.mixer.music.unpause()
        except Exception:
            pass
        # Si no había música cargada, reintentar cargar current_music
        if pygame.mixer.music.get_busy() == 0 and self.current_music:
            try:
                pygame.mixer.music.load(self.current_music)
                pygame.mixer.music.play(loops=-1)
            except Exception:
                pass
        self.is_playing = True

    def set_volume(self, value: float):
        """Establece el volumen de la música (0.0 - 1.0)."""
        try:
            v = max(0.0, min(1.0, float(value)))
            pygame.mixer.music.set_volume(v)
            self.volume = v
        except Exception:
            pass

    def get_volume(self) -> float:
        """Devuelve el volumen actual (0.0 - 1.0)."""
        try:
            return float(self.volume)
        except Exception:
            try:
                return float(pygame.mixer.music.get_volume())
            except Exception:
                return 0.0

    # --- Sound effects (SFX) ---
    def load_sound(self, name: str, file_path: str):
        """Carga un efecto de sonido en memoria y lo cachea por nombre."""
        try:
            if not os.path.exists(file_path):
                print(f"AudioManager: SFX no encontrado: {file_path}")
                return None
            snd = pygame.mixer.Sound(file_path)
            self.sounds[name] = snd
            return snd
        except Exception as e:
            print(f"AudioManager: Error cargando SFX {file_path}: {e}")
            return None

    def unload_sound(self, name: str):
        """
        Descarga un efecto de sonido de la memoria y detiene su reproducción si está activo.
        Útil para liberar memoria cuando un sonido ya no se necesita.
        """
        self.stop_sound(name)
        
        if name in self.sounds:
            del self.sounds[name]



    def play_sound(self, name: str, loops: int = 0, volume: float = 1.0):
        """Reproduce un SFX por nombre. 'loops' permite repetir varias veces."""
        snd = self.sounds.get(name)
        if snd is None:
            print(f"AudioManager: SFX '{name}' no cargado.")
            return None
        try:
            snd.set_volume(max(0.0, min(1.0, float(volume))))
            ch = snd.play(loops=loops)
            # Guardar el canal si queremos poder pararlo luego
            if ch:
                self.sfx_channels[name] = ch
            return ch
        except Exception as e:
            print(f"AudioManager: Error reproduciendo SFX '{name}': {e}")
            return None

    def play_loop_sound(self, name: str, volume: float = 1.0):
        """Reproduce un SFX en loop infinito y guarda el channel."""
        return self.play_sound(name, loops=-1, volume=volume)

    def stop_sound(self, name: str):
        """Detiene un SFX en reproducción por nombre si existe canal activo."""
        ch = self.sfx_channels.get(name)
        if ch:
            try:
                ch.stop()
            except Exception:
                pass
            self.sfx_channels.pop(name, None)
        else:
            # Intentar detener usando Sound.stop() si está cargado
            snd = self.sounds.get(name)
            if snd:
                try:
                    snd.stop()
                except Exception:
                    pass

    def toggle_music(self):
        if self.is_playing:
            self.pause_music()
        else:
            self.unpause_music()

    def is_music_playing(self):
        return self.is_playing
