import sys
import os

import pygame
from .images import magma_back, water_back
from button.isClicked import f_isClicked
from button.images import btn_background

def f_magma(window):
    font = pygame.font.Font('DungGeunMO.ttf', 90)

    play  = True
    xPos, yPos = -1, -1
    while play:
        xPos, yPos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.MOUSEBUTTONDOWN:        
                    if f_isClicked(800, 600, xPos, yPos) == 1:
                        play = False
                        return 10
        window.blit(magma_back, (0,0))
        window.blit(btn_background, (800, 600))
        if (f_isClicked(800, 600, xPos, yPos) == 1):
            window.blit(font.render(f"RESTART", False, (0, 0, 0)), (820, 600))
        else:
            window.blit(font.render(f"RESTART", False, (255, 255, 255)), (820, 600))


        pygame.display.update()
    return 10
    

def f_water(window):
    font = pygame.font.Font('DungGeunMO.ttf', 90)

    play  = True
    while play:
        xPos, yPos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:        
                if f_isClicked(window, xPos, yPos) == 1:
                    play = False
                    return 10
                
        window.blit(water_back, (0,0))
        window.blit(btn_background, (800, 600))
        if (f_isClicked(800, 600, xPos, yPos) == 1):
            window.blit(font.render(f"RESTART", False, (0, 0, 0)), (830, 600))
        else:
            window.blit(font.render(f"RESTART", False, (255, 255, 255)), (830, 600))

        pygame.display.update()
