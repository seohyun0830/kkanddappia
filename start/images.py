import pygame
pygame.mixer.init() # 믹서 초기화

background = pygame.image.load("start/assets/background.png")
background2 = pygame.image.load("start/assets/mode_background.png")

sfx_click = pygame.mixer.Sound("button/assets/click.wav")