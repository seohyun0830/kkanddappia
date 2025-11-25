# engine/sound.py
import pygame

pygame.mixer.init()

def play_bgm(path, volume=0.4):
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)  # 무한 반복

def stop_bgm():
    pygame.mixer.music.stop()

def set_bgm_volume(vol):
    pygame.mixer.music.set_volume(vol)

def load_sound(path, volume=1.0):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    return sound

broken_sound = load_sound("sounds/단선 생길때.mp3", 0.5)
success_bgm = load_sound("sounds/성공.mp3", 0.7)
fail_bgm = load_sound("sounds/실패.mp3", 0.7)

normal_bgm = "sounds/배경음악2.mp3"
low_bgm = "sounds/저압.mp3"

high_bgm = load_sound("sounds/고압.mp3", 0.3)
repair_bgm = load_sound("sounds/단선수리.mp3", 0.3)
fuel_bgm = load_sound("sounds/연료먹었을때.mp3", 0.3)
fuel_appear = load_sound("sounds/연료생길때마다.mp3", 0.3)
