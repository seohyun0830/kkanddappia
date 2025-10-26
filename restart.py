import pygame
from stage1.images import *

def f_restart(window):
    x = 0
    y = 0
    window.blit(restart_btn, (800, 600))
    for event in pygame.event.get():        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
        if x > 800 and x < 1020 and y > 600 and y < 672:
            return 1
    pygame.display.update()
