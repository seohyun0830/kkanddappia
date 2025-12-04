import pygame
import os
from .setting import ASSETS_PATH

class SoundManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100)

        self.tree_sound = self.load_sound_with_speed('tree_sound1.mp3', speed=2.0)
        self.bomb_sound = self.safe_load_sound('bomb_sound.mp3')

        self.walk_sound = self.load_sound_with_speed('walking_sound.mp3', speed=2.0)
        
        if self.walk_sound:
            self.walk_sound.set_volume(0.5)

    def safe_load_sound(self, filename):
        path = os.path.join(ASSETS_PATH, filename)
        try:
            if os.path.exists(path):
                return pygame.mixer.Sound(path)
            else:
                # 파일이 없을 경우 None 반환 (게임이 꺼지지 않게 함)
                return None
        except Exception as e:
            print(f"Error loading sound {filename}: {e}")
            return None

    # 배속 시키는 함수
    def load_sound_with_speed(self, filename, speed=1.0):
        path = os.path.join(ASSETS_PATH, filename)
        if not os.path.exists(path):
            return None
            
        try:
            pygame.mixer.quit()
            
            target_freq = int(44100 / speed)
            pygame.mixer.init(frequency=target_freq)
            
            sound = pygame.mixer.Sound(path)
            
            pygame.mixer.quit()
            pygame.mixer.init(frequency=44100)
            
            return sound
            
        except Exception as e:
            print(f"Error changing speed for {filename}: {e}")
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100)
            return self.safe_load_sound(filename)

    def play_background_music(self, filename, volume=0.3):
        path = os.path.join(ASSETS_PATH, filename)
        if os.path.exists(path):
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1) # -1은 무한 반복
            except Exception as e:
                print(f"Error loading BGM {filename}: {e}")
    
    def stop_background_music(self):
        pygame.mixer.music.stop()