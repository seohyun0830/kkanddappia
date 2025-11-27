import pygame
from start.start_main import f_start, f_modeSelect
from start.story import f_easy, f_hard, f_story1, f_story2
from stage1.stage1_main import f_stage1
from button.isClicked import f_isFail
from stage1.images import water_back, magma_back

from stage2.stage2_main import *

# --- [상수 정의] 상태를 나타내는 숫자들에 이름을 붙입니다 ---
STATE_EXIT   = -1  # 게임 종료  
STATE_START  = 0   # 시작 화면
STATE_MODE   = 1   # 난이도 선택
STATE_EASY   = 5
STATE_HARD   = 6
STATE_STORY1  = 8
STATE_STORY2  = 9
STATE_STAGE1 = 20  # 1스테이지 게임 플레이
STATE_STAGE2 = 11  # 2스테이지 (예정)

# --- [초기화] ---
pygame.init()
window_width = 1200
window_height = 800         
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Kkanddappia!")

# --- [메인 루프] ---
current_state = STATE_START # 현재 상태 (기존 stageFlag)
mode = -1                   # 난이도 (1: Easy, 2: Hard)

MODE = 0
Try = 0
MapInfo, ItemMapInfo, InvenInfo, LadderInfo = 0, 0, 0, 0
while current_state != STATE_EXIT:
    # 1. 시작 화면
    if current_state == STATE_START:
        result = f_start(window)
        if result == 0:   current_state = STATE_EXIT
        elif result == 1: current_state = STATE_MODE

    # 2. 모드(난이도) 선택 화면
    elif current_state == STATE_MODE:
        mode = f_modeSelect(window)
        if mode == 0:     current_state = STATE_EXIT
        elif mode == 1:  current_state = STATE_EASY # 모드 선택 완료 -> 1스테이지로
        elif mode == 2:  current_state = STATE_HARD
        MODE = mode                                 # 1: easy 2: hard
    
    # 스토리 연결
    elif current_state == STATE_EASY:
        current_state = f_easy(window)
    elif current_state == STATE_HARD:
        current_state = f_hard(window)
    elif current_state == STATE_STORY1:
        current_state = f_story1(window)
    elif current_state == STATE_STORY2:
        current_state = f_story2(window)
    # 3. 1스테이지 플레이
    if current_state == STATE_STAGE1:
        # (나중에 f_stage1에 mode를 넘겨줘야 할 수도 있습니다)
        result, MapInfo, ItemMapInfo, InvenInfo, LadderInfo = f_stage1(window, MODE, Try, MapInfo, ItemMapInfo, InvenInfo, LadderInfo) 
        
        if result == 0:    # 게임 종료 (X버튼)
            current_state = STATE_EXIT
            
        elif result == 1:  # 마그마 실패
            # f_isFail 함수가 "재시작하면 11", "나가면 -1 or 0"을 반환한다고 가정
            current_state = f_isFail(window, magma_back)
            
        elif result == 2:  # 지하수 실패
            current_state = f_isFail(window, water_back)

        elif result == -1: # 스테이지 클리어 (성공)
            current_state = STATE_STAGE2
            Try += 1   
    
    # 4. 2스테이지 (예정)
    elif current_state == STATE_STAGE2:
        stage2 = Stage2(window)
        result=stage2.run()
        
        if result=="stage1":
            current_state=STATE_STAGE1

        elif result=="quit" or result=="game_over":
            current_state=STATE_EXIT

# 종료 처리
pygame.quit()