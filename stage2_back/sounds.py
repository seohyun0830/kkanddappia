import pygame

pygame.mixer.init() # 믹서 초기화

backgroundSound = pygame.mixer.Sound("stage2_back/assets/background_sound.mp3")
jumpSound = pygame.mixer.Sound("stage2_back/assets/jump.wav")
walkingSound = pygame.mixer.Sound("stage2_back/assets/walking_sound.mp3")