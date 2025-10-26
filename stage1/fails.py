import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pygame
from images import magma_back
from restart import f_restart

def magma(window):
    print("running")
    pygame.event.clear()
    play  = True
    while play:
        #for event in pygame.event.get():        
            #if event.type == pygame.QUIT:
                #play = False
        window.blit(magma_back, (0,0))
    # if f_restart(window):
    #     import stage1.stage1_main               # 이 stage 1을 함수로 써야하나보다
    #     play = False

    pygame.display.update()
