import pygame

pygame.mixer.init() # 믹서 초기화

# 360 * 108
btn_background = pygame.image.load("button/assets/btn_background.png")

sfx_click = pygame.mixer.Sound("button/assets/click.wav")