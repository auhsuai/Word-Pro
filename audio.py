import os
import threading
import ctypes

class AudioMixin:
    def play_typing_sound(self, sound_type="click"):
        if not getattr(self, 'sound_enabled', True): return
        
        if not hasattr(self, "_sound_counter"): self._sound_counter = 0
        self._sound_counter = (self._sound_counter + 1) % 15 # Increase channels for high speed
        
        alias = f"typing_ch_{self._sound_counter}"
        threading.Thread(target=self._execute_mci_sound, args=(alias, sound_type), daemon=True).start()

    def _execute_mci_sound(self, alias, sound_type):
        try:
            winmm = ctypes.windll.winmm
            
            # Select sound file
            filename = "Space.wav" if sound_type == "space" else "click.wav"
            volume = 850 if sound_type == "space" else 1000 # Balance volumes
            
            sound_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
            if not os.path.exists(sound_file):
                from data import resource_path
                sound_file = resource_path(filename)
            
            if os.path.exists(sound_file):
                winmm.mciSendStringW(f"close {alias}", None, 0, None)
                winmm.mciSendStringW(f"open \"{sound_file}\" type waveaudio alias {alias}", None, 0, None)
                # Set volume (0-1000)
                winmm.mciSendStringW(f"setaudio {alias} volume to {volume}", None, 0, None)
                winmm.mciSendStringW(f"play {alias} from 0", None, 0, None)
            else:
                # Fallback to system sound if file missing
                import winsound
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)
        except: pass

    def toggle_sound(self):
        if hasattr(self, 'sys_menu_toggle_sound'):
            self.sound_enabled = self.sys_menu_toggle_sound.get()
