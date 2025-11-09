import pygame
from start.start_main import f_start, f_modeSelect
from stage1.stage1_main import f_stage1
from stage1 import fails

pygame.init()

# 화면 크기
window_width = 1200
window_height = 800         
window = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("Kkanddappia!")

stageFlag = 0
mode = -1
while stageFlag != -1:
    # stageFlag가 0번대 : 시작화면
    if (stageFlag == 0):
        start = f_start(window)
        if (start == 0):
            stageFlag = -1
        elif (start == 1):
            stageFlag = 1
    if (stageFlag == 1):
        mode = f_modeSelect(window) # 1: easy, 2: hard
        if (mode == 0):
            stageFlag = -1
        elif (mode != -1):
            stageFlag = 10

    elif (stageFlag == 10):
        stage1 = f_stage1(window)
        if (stage1 == 0):
            stageFlag = -1
        elif (stage1 == 1):
            stageFlag = fails.f_magma(window)
        elif (stage1 == 2):
            stageFlag = fails.f_water(window)
        elif (stage1 == -1):
            stageFlag = 20
    elif (stageFlag == 20):
        print("2스테이지")
        break

pygame.quit()