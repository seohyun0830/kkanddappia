import pygame
from start.start_main import f_start, f_modeSelect
from start.story import f_easy, f_hard, f_story1, f_story2
from stage1.stage1_main import f_stage1
from button.isClicked import f_isFail
from stage1.images import waters, magmas
from stage1.sounds import sfx_water, sfx_magma

from stage2.stage2_main import *
from timer.timer import Timer
from timer.images import overs, sfx_bombSound

STATE_EXIT   = -1  
STATE_START  = 0   
STATE_MODE   = 1   
STATE_EASY   = 5
STATE_HARD   = 6
STATE_STORY1  = 8
STATE_STORY2  = 9
STATE_STAGE1 = 20  # 1스테이지
STATE_STAGE2 = 11  # 2스테이지
STATE_STAGE3 = 30 

##얍

# --- [초기화] ---
pygame.init()
window_width = 1200
window_height = 800         
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Kkanddappia!")

# --- [준비] ---
current_state = STATE_START 
mode = -1                   

MODE = 0
Try = 0
MapInfo, ItemMapInfo, InvenInfo, InvenCnt = 0, 0, 0, [0,0,0,0,0]

FUEL=0

stage2 = Stage2(window) 
timer = Timer()
#아이템 번호
ITEM_ID_TO_NAME = {
    1: 'stone',
    2: 'soil',
    3: 'fossil',
    4: 'paper',   #쪽지로 대체해야함!!
    5: 'ladder'
}

# 2. Stage 2(문자) -> Stage 1(숫자)
ITEM_NAME_TO_ID = {v: k for k, v in ITEM_ID_TO_NAME.items()}

# --- [메인 루프] ---
while current_state != STATE_EXIT:
    # 1. 시작 화면
    if current_state == STATE_START:
        result = f_start(window)
        if result == 0:   current_state = STATE_EXIT
        elif result == 1: current_state = STATE_MODE

    # 2. 모드 선택
    elif current_state == STATE_MODE:
        mode = f_modeSelect(window)
        if mode == 0:     current_state = STATE_EXIT
        elif mode == 1:  
            current_state = STATE_EASY 
            stage2.is_easy_mode = True  
        elif mode == 2:  
            current_state = STATE_HARD
            stage2.is_easy_mode = False
        MODE = mode
    
    # 스토리 연결
    elif current_state == STATE_EASY:
        current_state = f_easy(window)
    elif current_state == STATE_HARD:
        current_state = f_hard(window)
    elif current_state == STATE_STORY1:
        current_state = f_story1(window)
    elif current_state == STATE_STORY2:
        current_state = f_story2(window)
        start_ticks = pygame.time.get_ticks()

    # 3. 1스테이지 플레이
    elif current_state == STATE_STAGE1:
        ret_val = f_stage1(window, MODE, Try, MapInfo, ItemMapInfo, InvenInfo, InvenCnt, timer) 
        
        if isinstance(ret_val, tuple):
            result = ret_val[0]
            MapInfo = ret_val[1]
            ItemMapInfo = ret_val[2]
            InvenInfo = ret_val[3]   # [1, 1, 5, 2...]
            InvenCnt = ret_val[4]  # 전체 아이템 갯수
        else:
            result = ret_val
        
        if (result is not None):
            pygame.mixer.music.stop()
        
        if result == 0:
            current_state = STATE_EXIT
        elif result == 1:
            sfx_magma.play()
            if (f_isFail(window, magmas) == True):
                current_state = STATE_STAGE2
                timer.reset()
        elif result == 2:  
            sfx_water.play()
            if (f_isFail(window, waters) == True):
                current_state = STATE_STAGE2
                timer.reset()
        elif result == 3:
            sfx_bombSound.play()
            if (f_isFail(window, overs) == True):
                current_state = STATE_STAGE2
                timer.reset()
     
        elif result == -1:
            current_state = STATE_STAGE2
            Try += 1
            
            imported_items = []

            for i, count in enumerate(InvenCnt):
                item_id = i + 1

                if count > 0 and item_id in ITEM_ID_TO_NAME:
                    name = ITEM_ID_TO_NAME[item_id]
                    imported_items.extend([name] * count)

            stage2.update_resources(imported_items)
    
    # 4. 2스테이지 플레이
    elif current_state == STATE_STAGE2:
        if Try == 0:
            timer.reset()
        result = stage2.run(timer)

        if isinstance(result, tuple):
            next_stage, count = result  # 튜플 분해
            
            if next_stage == "stage3":
                FUEL = count  # 연료 개수 저장
                print(f"Stage 2 클리어! 획득한 연료: {FUEL}개")
                
                current_state = STATE_STAGE3 # 3스테이지로 이동 (상수 정의 필요)
        
        if result == "stage1":
            # [클리어/이동] Stage 2 -> Stage 1 복귀
            current_state = STATE_STAGE1
            
            # --- [★핵심: Stage 2 -> 1 데이터 복구] ---
            # Stage 2의 인벤토리를 가져옵니다.
            s2_inventory = stage2.inventory
            
            #new_inven_info = [] # Stage 1용 리스트 (숫자)
            #new_ladder_count = 0 # Stage 1용 사다리 개수
            InvenCnt =[0, 0, 0, 0, 0]
            print(s2_inventory)
            for item_name in s2_inventory:
                # Stage 1에서 쓰는 아이템만 변환 (우주선 부품 등은 제외됨)
                if item_name in ITEM_NAME_TO_ID:
                    item_id = ITEM_NAME_TO_ID[item_name]
                    InvenCnt[item_id - 1] += 1

            print(f"[Main] Stage 2 -> 1 복귀: 인벤={InvenInfo}, 각 갯수={InvenCnt}")
        elif result == "timeOUT":
            sfx_bombSound.play()
            if (f_isFail(window, overs) == True):
                current_state = STATE_STAGE2
                timer.reset()
        elif result == "quit" or result == "game_over":
            current_state = STATE_EXIT

# 종료
pygame.quit()