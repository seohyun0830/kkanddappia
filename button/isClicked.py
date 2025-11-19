import pygame
from stage1.images import *
from .images import btn_background

def f_isClicked(btnX, btnY, xPos, yPos):
    if xPos > btnX and xPos < btnX + 360 and yPos > btnY and yPos < btnY + 108:
        return 1

def f_isFail(window, reson):
    font = pygame.font.Font('DungGeunMO.ttf', 90)
    fps = pygame.time.Clock()

    play  = True
    xPos, yPos = -1, -1
    while play:
        fps.tick(60)

        xPos, yPos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:  
                    if res:
                        play = False
                        return 10
        window.blit(reson, (0,0))
        window.blit(btn_background, (800, 600))
        res = f_isClicked(800, 600, xPos, yPos)
        if (res):
            window.blit(font.render(f"RESTART", False, (0, 0, 0)), (820, 600))
        else:
            window.blit(font.render(f"RESTART", False, (255, 255, 255)), (820, 600))

        pygame.display.update()