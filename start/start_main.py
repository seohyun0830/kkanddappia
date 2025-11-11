import pygame
from button.images import btn_background
from .images import background, background2
from button.isClicked import f_isClicked

def f_start(window):
    font = pygame.font.Font(None, 100)

    FONT = pygame.font.Font(None, 200)

    play = True
    while play:
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                play = False
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                xPos, yPos = pygame.mouse.get_pos()
                if f_isClicked(800, 600, xPos, yPos) == 1:
                    play = False
                    return 1
        window.blit(background, (0,0))
        window.blit(btn_background, (800, 600)) 
        window.blit(font.render(f"START", True, (255, 255, 255)), (850, 620))

        window.blit(FONT.render(f"KKANDDAPPIA!", True, (255, 255, 255)), (100, 200))
        pygame.display.update()

def f_modeSelect(window):
    font = pygame.font.Font(None, 100)

    play = True
    while play:
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                play = False
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                xPos, yPos = pygame.mouse.get_pos()
                if f_isClicked(120, 400, xPos, yPos) == 1:
                    play = False
                    return 1
                elif f_isClicked(720, 400, xPos, yPos) == 1:
                    play = False
                    return 2
        window.blit(background2, (0,0))
        window.blit(btn_background, (120, 400)) 
        window.blit(btn_background, (720, 400)) 
        window.blit(font.render(f"EASY", True, (255, 255, 255)), (170, 420))
        window.blit(font.render(f"HARD", True, (255, 255, 255)), (770, 420))

        pygame.display.update()

360