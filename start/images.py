import pygame
pygame.mixer.init() # 믹서 초기화

background = pygame.image.load("start/assets/background.png")
background2 = pygame.image.load("start/assets/mode_background.png")

talking = pygame.image.load("start/assets/talking.png")

grandma = pygame.image.load("start/assets/grandma.png")
bedroom = pygame.image.load("start/assets/bedroom.png")
outside = pygame.image.load("start/assets/outside.jpg")
outside = pygame.transform.smoothscale(outside, (1200, 800))

sfx_click = pygame.mixer.Sound("button/assets/click.wav")
sfx_type = pygame.mixer.Sound("start/assets/type.mp3")
sfx_siren = pygame.mixer.Sound("start/assets/siren.mp3")
sfx_arrive = pygame.mixer.Sound("start/assets/arrive.mp3")