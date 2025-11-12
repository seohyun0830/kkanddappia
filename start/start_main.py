import pygame
from button.images import btn_background
from .images import background, background2
from button.isClicked import f_isClicked

def f_start(window):
    font = pygame.font.Font('DungGeunMO.ttf', 100)

    FONT = pygame.font.Font('DungGeunMO.ttf', 200)
    FONT_bold = pygame.font.Font('DungGeunMO.ttf', 200)
    FONT_bold.set_bold(True)
    play = True
    while play:
        xPos, yPos = pygame.mouse.get_pos()
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                play = False
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if f_isClicked(800, 600, xPos, yPos) == 1:
                    play = False
                    return 1
        window.blit(background, (0,0))
        window.blit(btn_background, (800, 600)) 
        if (f_isClicked(800, 600, xPos, yPos) == 1):
            window.blit(font.render(f"START", False, (0, 0, 0)), (850, 600))
        else:
            window.blit(font.render(f"START", False, (255, 255, 255)), (850, 600))

        window.blit(FONT_bold.render(f"깐따삐아!", False, (0, 0, 0)), (155, 210))
        window.blit(FONT.render(f"깐따삐아!", False, (255, 255, 255)), (150, 200))

        pygame.display.update()

def f_modeSelect(window):
    font = pygame.font.Font('DungGeunMO.ttf', 100)

    play = True
    while play:
        xPos, yPos = pygame.mouse.get_pos()
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                play = False
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if f_isClicked(120, 400, xPos, yPos) == 1:
                    play = False
                    return 1
                elif f_isClicked(720, 400, xPos, yPos) == 1:
                    play = False
                    return 2
        window.blit(background2, (0,0))
        window.blit(btn_background, (120, 400)) 
        window.blit(btn_background, (720, 400)) 

        if (f_isClicked(120, 400, xPos, yPos) == 1):
            window.blit(font.render(f"EASY", False, (0, 0, 0)), (200, 400))
        else:
            window.blit(font.render(f"EASY", False, (255, 255, 255)), (200, 400))

        if (f_isClicked(720, 400, xPos, yPos) == 1):
            window.blit(font.render(f"HARD", False, (0, 0, 0)), (800, 400))
        else:
            window.blit(font.render(f"HARD", False, (255, 255, 255)), (800, 400))

        pygame.display.update()

360