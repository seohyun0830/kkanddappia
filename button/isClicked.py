import pygame
from stage1.images import *

def f_isClicked(btnX, btnY, xPos, yPos):
    if xPos > btnX and xPos < btnX + 360 and yPos > btnY and yPos < btnY + 108:
        return 1
    pygame.display.update()