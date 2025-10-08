import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pygame
from images import *
from restart import *

def func_fail_magma(window):
    play = True
    while play:
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                play = False
        window.blit(magma_back, (0,0))
        restart_(window)
        pygame.display.update()
