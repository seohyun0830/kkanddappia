import pygame
from start.start_main import f_start, f_modeSelect
from start.story import f_easy, f_hard, f_story1, f_story2
from stage1.stage1_main import f_stage1
from button.isClicked import f_isFail
from stage1.images import water_back, magma_back

from stage2.stage2_main import *

##왜 또 그러니##

STATE_EXIT   = -1  
STATE_START  = 0   
STATE_MODE   = 1   
STATE_EASY   = 5
STATE_HARD   = 6
STATE_STORY1  = 8
STATE_STORY2  = 9
STATE_STAGE1 = 20  # 1스테이지
STATE_STAGE2 = 11  # 2스테이지

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
MapInfo, ItemMapInfo, InvenInfo, LadderInfo = 0, 0, 0, 0

stage2 = Stage2(window) 

#아이템 번호
ITEM_ID_TO_NAME = {
    1: 'stone',
    2: 'soil',
    3: 'fossil',
    4: 'wood',   #쪽지로 대체해야함!!
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

    # 3. 1스테이지 플레이
    elif current_state == STATE_STAGE1:
        ret_val = f_stage1(window, MODE, Try, MapInfo, ItemMapInfo, InvenInfo, LadderInfo) 
        
        if isinstance(ret_val, tuple):
            result = ret_val[0]
            MapInfo = ret_val[1]
            ItemMapInfo = ret_val[2]
            InvenInfo = ret_val[3]   # [1, 1, 5, 2...]
            LadderInfo = ret_val[4]  # 사다리 개수
        else:
            result = ret_val

        if result == 0:    
            current_state = STATE_EXIT
        elif result == 1:  
            current_state = f_isFail(window, magma_back)
        elif result == 2:  
            current_state = f_isFail(window, water_back)
        
        elif result == -1: # [클리어] Stage 1 -> Stage 2 이동
            current_state = STATE_STAGE2
            Try += 1
            
            # --- [Stage 1 -> 2 데이터 전달] ---
            imported_items = []
            
            # 인벤토리 리스트 변환 (숫자 -> 문자)
            if isinstance(InvenInfo, list):
                for item_id in InvenInfo:
                    if item_id in ITEM_ID_TO_NAME:
                        imported_items.append(ITEM_ID_TO_NAME[item_id])
            
            # 사다리 개수만큼 추가 (만약 InvenInfo 리스트에 사다리가 포함 안 되어 있다면)
            # Stage 1 코드에 따라 다르지만, 보통 중복 방지를 위해 리스트에 없으면 여기서 추가합니다.
            # 리스트에 5가 이미 있다면 위 루프에서 추가되었을 것입니다.
            # 혹시 모르니 LadderInfo가 있는데 리스트엔 없다면 추가하는 안전장치:
            ladder_in_list = imported_items.count('ladder')
            if LadderInfo > ladder_in_list:
                imported_items.extend(['ladder'] * (LadderInfo - ladder_in_list))

            stage2.reset_game_data(imported_items)
    
    # 4. 2스테이지 플레이
    elif current_state == STATE_STAGE2:
        result = stage2.run()
        
        if result == "stage1":
            # [클리어/이동] Stage 2 -> Stage 1 복귀
            current_state = STATE_STAGE1
            
            # --- [★핵심: Stage 2 -> 1 데이터 복구] ---
            # Stage 2의 인벤토리를 가져옵니다.
            s2_inventory = stage2.inventory
            
            new_inven_info = [] # Stage 1용 리스트 (숫자)
            new_ladder_count = 0 # Stage 1용 사다리 개수
            
            for item_name in s2_inventory:
                # Stage 1에서 쓰는 아이템만 변환 (우주선 부품 등은 제외됨)
                if item_name in ITEM_NAME_TO_ID:
                    item_id = ITEM_NAME_TO_ID[item_name]
                    new_inven_info.append(item_id)
                    
                    if item_name == 'ladder':
                        new_ladder_count += 1
            
            # Stage 1 변수 업데이트!
            InvenInfo = new_inven_info
            LadderInfo = new_ladder_count
            
            print(f"[Main] Stage 2 -> 1 복귀: 인벤={InvenInfo}, 사다리={LadderInfo}")

        elif result == "quit" or result == "game_over":
            current_state = STATE_EXIT

# 종료
pygame.quit()



'''

STATE_EXIT   = -1  
STATE_START  = 0   
STATE_MODE   = 1   
STATE_EASY   = 5
STATE_HARD   = 6
STATE_STORY1  = 8
STATE_STORY2  = 9
STATE_STAGE1 = 20  # 1스테이지
STATE_STAGE2 = 11  # 2스테이지

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
MapInfo, ItemMapInfo, InvenInfo, LadderInfo = 0, 0, 0, 0

# Stage 2 객체 생성 (한 번만 생성해서 데이터 유지)
stage2 = Stage2(window) 

# 아이템 번호
ITEM_ID_TO_NAME = {
    1: 'stone',
    2: 'soil',
    3: 'fossil',
    4: 'wood',   #임시!!!
    5: 'ladder'
}

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
            stage2.is_easy_mode = True  # Stage 2에 난이도 전달
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

    # 3. 1스테이지 플레이
    elif current_state == STATE_STAGE1:
        # 리턴값을 받아서 성공/실패 여부 판단
        ret_val = f_stage1(window, MODE, Try, MapInfo, ItemMapInfo, InvenInfo, LadderInfo) 
        
        # 1) 튜플이면 성공 (결과, 맵정보, 아이템정보, 인벤토리, 사다리수)
        if isinstance(ret_val, tuple):
            result = ret_val[0]
            MapInfo = ret_val[1]
            ItemMapInfo = ret_val[2]
            InvenInfo = ret_val[3]   # [1, 1, 2...] 리스트
            LadderInfo = ret_val[4]  # 사다리 개수
        # 2) 정수면 실패/종료
        else:
            result = ret_val

        if result == 0:    
            current_state = STATE_EXIT
        elif result == 1:  
            current_state = f_isFail(window, magma_back)
        elif result == 2:  
            current_state = f_isFail(window, water_back)
        
        elif result == -1: # [클리어!] -> Stage 2로 이동
            current_state = STATE_STAGE2
            Try += 1
            
            # --- [아이템 연동 로직] ---
            imported_items = []
            
            # (1) 인벤토리 리스트 변환 (숫자 -> 문자열)
            if isinstance(InvenInfo, list):
                for item_id in InvenInfo:
                    if item_id in ITEM_ID_TO_NAME:
                        imported_items.append(ITEM_ID_TO_NAME[item_id])
            
            # (2) 사다리 개수만큼 아이템 추가
            if LadderInfo > 0:
                imported_items.extend(['ladder'] * LadderInfo)
            
            # (3) 변환된 아이템을 들고 Stage 2 초기화
            print(f"Stage 1 -> 2 아이템 이동: {imported_items}")
            stage2.reset_game_data(imported_items)
    
    # 4. 2스테이지 플레이
    elif current_state == STATE_STAGE2:
        result = stage2.run()
        
        if result == "stage1":
            current_state = STATE_STAGE1 # 다시 1스테이지로

        elif result == "quit" or result == "game_over":
            current_state = STATE_EXIT

# 종료
pygame.quit()

'''

'''

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

stage2 = Stage2(window)

ITEM_ID_TO_NAME = {
    1: 'stone',
    2: 'soil',
    3: 'fossil',
    4: 'wood',
    5: 'ladder'
}

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
        result=stage2.run()
        
        if result=="stage1":
            current_state=STATE_STAGE1

        elif result=="quit" or result=="game_over":
            current_state=STATE_EXIT

# 종료 처리
pygame.quit()
'''