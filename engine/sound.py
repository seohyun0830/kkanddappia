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

broken_sound = load_sound("sounds/stage3/단선 생길때.mp3", 0.5)
success_bgm = load_sound("sounds/stage3/성공.mp3", 0.7)
fail_bgm = load_sound("sounds/stage3/실패.mp3", 0.7)
<<<<<<< HEAD

normal_bgm = "sounds/stage3/배경음악2.mp3"
low_bgm = "sounds/stage3/저압.mp3"
=======
oxfail_bgm=load_sound("sounds/stage3/산소부족실패.mp3",0.5)
item_pickup = load_sound("sounds/stage3/텔레포트겟.mp3", 0.5)
teleport=load_sound("sounds/stage3/순간이동 성공시.mp3",0.4)
drone_drop = load_sound("sounds/stage3/드론아이템뿌릴때.mp3", 0.5)
normal_bgm = "sounds/stage3/배경음악2.mp3"
low_bgm = "sounds/stage3/저압.mp3"
breath=load_sound("sounds/stage3/숨가쁜소리.mp3",0.4)
beep_error=load_sound("sounds/stage3/삐소리.mp3",0.3)
explosion=load_sound("sounds/stage3/폭발.mp3",0.5)
fire_loop=load_sound("sounds/stage3/불타는소리.mp3",0.5)



>>>>>>> 68ea39ea6b4d0b4b59455b03d254dde54355bff1

high_bgm = load_sound("sounds/stage3/고압.mp3", 0.3)
repair_bgm = load_sound("sounds/stage3/단선수리.mp3", 0.3)
fuel_bgm = load_sound("sounds/stage3/연료먹었을때.mp3", 0.3)
fuel_appear = load_sound("sounds/stage3/연료생길때마다.mp3", 0.3)
