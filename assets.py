#assets.py
#이미지,폰트,타이머
import pygame
from constants import IRON_GATE,BROKEN

pipe_images = {}
bg_img = None

#파이프 이미지 11개 배열로 저장
def load_pipe_images():
    global pipe_images, bg_img
    for i in range(1, 12):
        pipe_images[i] = pygame.image.load(f'images/pipe{i}.jpg').convert()
    pipe_images[IRON_GATE] = pygame.image.load('images/irongate.jpg').convert()
    pipe_images[BROKEN] = pygame.image.load('images/broken.jpg').convert()
    bg_img = pygame.image.load('images/bg_img.jpg').convert() 

pressure_regulator_img = None
needle_img = None

def load_pressure_images():
    global pressure_regulator_img, needle_img
    pressure_regulator_img = pygame.image.load('images/pressure.png').convert_alpha()
    needle_img = pygame.image.load('images/needle.png').convert_alpha()
