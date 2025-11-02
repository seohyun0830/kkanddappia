import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pygame
from .images import magma_back, water_back, magmas, waters
from restart import f_restart

def f_magma(window):
    play  = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
        window.blit(magma_back, (0,0))

        pygame.display.update()

def f_water(window):
    play  = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
        window.blit(water_back, (0,0))

        pygame.display.update()
