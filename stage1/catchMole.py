import pygame

pygame.init()

window_width = 600
window_height = 400

window = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("Kkanddappia!")

background = pygame.image.load("assets/moleMap.png")
moleUp = pygame.image.load("assets/mole_up.png")
moleDown = pygame.image.load("assets/mole_down.png")
hammer = pygame.image.load("assets/hammer.png")

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False


    window.blit(background, (0,0))
    window.blit(moleUp, (85,50))
    window.blit(moleDown, (295,165))
    window.blit(hammer, (300,180))

    pygame.display.update()