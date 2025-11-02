import pygame
from stage1.stage1_main import f_stage1
from stage1 import fails

pygame.init()

# 화면 크기
window_width = 1200
window_height = 800         
window = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("Kkanddappia!")


stage1 = f_stage1(window)
if (stage1 == 1):
    fails.f_magma(window)
                
pygame.quit()