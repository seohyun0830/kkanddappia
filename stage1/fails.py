import sys
import os

import pygame
from .images import magma_back, water_back
from button.isClicked import f_isClicked
from button.images import btn_background

def f_magma(window):
    font = pygame.font.Font(None, 90)

    play  = True
    xPos, yPos = -1, -1
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                xPos, yPos = pygame.mouse.get_pos()
        window.blit(magma_back, (0,0))
        window.blit(btn_background, (800, 600))
        window.blit(font.render(f"RESTART", True, (255, 255, 255)), (850, 620))

        res = f_isClicked(800, 600, xPos, yPos)
        if res == 1:
            play = False

        pygame.display.update()
    return 10
    

def f_water(window):
    font = pygame.font.Font(None, 90)

    play  = True
    xPos, yPos = -1, -1
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                xPos, yPos = pygame.mouse.get_pos()
        window.blit(water_back, (0,0))
        window.blit(btn_background, (800, 600))
        window.blit(font.render(f"RESTART", True, (255, 255, 255)), (850, 620))

        res = f_isClicked(window, xPos, yPos)
        if res == 1:
            play = False

        pygame.display.update()
    return 10