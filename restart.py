import pygame
from stage1.images import *

def restart_(window):
    x = 0
    y = 0
    play = True
    while play:
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x > 800 and x < 1020 and y > 600 and y < 672:
                    import stage1.stage1_main
        window.blit(restart_btn, (800, 600))
        pygame.display.update()
