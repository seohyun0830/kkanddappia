import pygame
import sys
import builtins

#1,2
from start.start_main import f_start, f_modeSelect
from start.story import f_easy, f_hard, f_story1, f_story2
from stage1.stage1_main import f_stage1
from button.isClicked import f_isFail
from stage1.images import waters, magmas
from stage1.sounds import sfx_water, sfx_magma
from stage2.stage2_main import Stage2   
from timer.timer import Timer
from timer.images import overs, sfx_bombSound

# 3,4
from engine import assets
from stage3 import Stage3
from stage4.stage4 import Stage4
from stage3.story import Stage3Story    
from stage4to3.stage4to3 import Stage4To3
from stage2_back.stage2_back_main import Stage2Back
from engine.fuel_manager import fuel_manager


STATE_EXIT   = -1  
STATE_START  = 0   
STATE_MODE   = 1   
STATE_EASY   = 5
STATE_HARD   = 6
STATE_STORY1 = 8
STATE_STORY2 = 9
STATE_STAGE1 = 20  # 1스테이지
STATE_STAGE2 = 11  # 2스테이지
STATE_STAGE3 = 30  

ITEM_ID_TO_NAME = {
    1: 'stone', 2: 'soil', 3: 'fossil', 4: 'paper', 5: 'ladder'
}
# 2. Stage 2(문자) -> Stage 1(숫자)
ITEM_NAME_TO_ID = {v: k for k, v in ITEM_ID_TO_NAME.items()}

def main():
    pygame.init()
    pygame.mixer.init()
    
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Kkanttappia!")
    builtins.shared_screen = screen

    # 3, 4스테이지용 에셋 로드
    assets.load_all()

    mode = -1                  
    MODE = 0
    Try = -1
    MapInfo, ItemMapInfo, InvenInfo, InvenCnt = 0, 0, 0, [0,0,0,0,0]    
    current_state = STATE_START 
   
    # 1, 2스테이지 객체
    stage2 = Stage2(screen) 
    timer = Timer()

    # 3스테이지 튜토리얼
    game_state = {"stage3_tutorial_done": False}

   
    while current_state != STATE_EXIT:
        
        if current_state == STATE_START:
            result = f_start(screen)
            if result == 0:   current_state = STATE_EXIT
            elif result == 1: current_state = STATE_MODE

        elif current_state == STATE_MODE:
            mode = f_modeSelect(screen)
            if mode == 0:     current_state = STATE_EXIT
            elif mode == 1:  #이지
                current_state = STATE_EASY 
                stage2.is_easy_mode = True 
                game_difficulty="easy" 
            elif mode == 2:  #하드
                current_state = STATE_HARD
                stage2.is_easy_mode = False
                game_difficulty="hard"
            MODE = mode
        
        elif current_state == STATE_EASY:
            current_state = f_easy(screen)
        elif current_state == STATE_HARD:
            current_state = f_hard(screen)
        elif current_state == STATE_STORY1:
            current_state = f_story1(screen)
        elif current_state == STATE_STORY2:
            current_state = f_story2(screen)
            timer.reset()

        # ---------------------------------------
        #Stage 1 
        # ---------------------------------------
        elif current_state == STATE_STAGE1:
            ret_val = f_stage1(screen, MODE, Try, MapInfo, ItemMapInfo, InvenInfo, InvenCnt, timer) 
            
            if isinstance(ret_val, tuple):
                result = ret_val[0]
                MapInfo = ret_val[1]
                ItemMapInfo = ret_val[2]
                InvenInfo = ret_val[3]   
                InvenCnt = ret_val[4]
            else:
                result = ret_val
            
            if (result is not None): 
                pygame.mixer.music.stop()
            
            if result == 0: current_state = STATE_EXIT
            elif result == 1: 
                sfx_magma.play()
                if f_isFail(screen, magmas):
                    current_state = STATE_STAGE2
                    timer.reset()
                    Try = 0
                    stage2.reset_game_data()
            elif result == 2:
                sfx_water.play()
                if f_isFail(screen, waters):
                    current_state = STATE_STAGE2
                    timer.reset()
                    Try = 0
                    stage2.reset_game_data()
            elif result == 3: 
                sfx_bombSound.play()
                if f_isFail(screen, overs):
                    current_state = STATE_STAGE2
                    timer.reset()
                    Try = 0
                    stage2.reset_game_data()
            elif result == -1: 
                current_state = STATE_STAGE2
                Try += 2
                # 아이템 연동
                imported_items = []
                for i, count in enumerate(InvenCnt):
                    item_id = i + 1
                    if count > 0 and item_id in ITEM_ID_TO_NAME:
                        imported_items.extend([ITEM_ID_TO_NAME[item_id]] * count)
                stage2.update_resources(imported_items)
        
        # ---------------------------------------
        # Stage 2 
        # ---------------------------------------
        elif current_state == STATE_STAGE2:
            if Try == -1: 
                timer.reset()
            result = stage2.run(timer)

            if isinstance(result, tuple):
                next_stage, count = result
                if next_stage == "stage3":  #3스테이지 이동
                    fuel_manager.set_fuel(count*10+70) # 연료 
                    print(f"Stage 2 클리어! 획득한 연료: {count}개")
                    
                    story = Stage3Story(screen)
                    story.run()
                    pygame.event.clear()
                    current_state = STATE_STAGE3 

            elif result == "stage1":
                current_state = STATE_STAGE1
                
                # --- [핵심: Stage 2 -> 1 데이터 복구] ---
                s2_inventory = stage2.inventory
                
                # 초기화
                InvenInfo = []           # 아이템 ID 리스트 (예: [1, 1, 5])
                InvenCnt = [0, 0, 0, 0, 0] # 개수 카운트 (예: [2, 0, 0, 0, 1])
                
                cnt = 0
                for item_name in s2_inventory:
                    # Stage 1에서 사용하는 아이템인지 확인
                    if item_name in ITEM_NAME_TO_ID:
                        item_id = ITEM_NAME_TO_ID[item_name]
                        if item_id == 4:
                            continue
                        InvenCnt[item_id - 1] += 1
                for i in range(5): # 아이템 ID 1~5번 확인
                    item_id = i + 1
                    count = InvenCnt[i] # 해당 아이템의 총 개수
                    while count > 0:
                        InvenInfo.append(item_id) # 슬롯 추가
                        count -= 5

            elif result == "timeOUT":
                sfx_bombSound.play()
                if f_isFail(screen, overs):
                    current_state = STATE_STAGE2
                    MapInfo, ItemMapInfo, InvenInfo, InvenCnt = 0, 0, 0, [0,0,0,0,0] 
                    Try = 0
                    stage2.reset_game_data()
                    timer.reset()

            elif result=="reset":
                MapInfo, ItemMapInfo, InvenInfo, InvenCnt = 0, 0, 0, [0,0,0,0,0] 
                Try = 0
                timer.reset()
                
                stage2.reset_game_data()
                
                current_state = STATE_STAGE2
                    
            elif result == "quit" or result == "game_over":
                MapInfo, ItemMapInfo, InvenInfo, InvenCnt = 0, 0, 0, [0,0,0,0,0] 
                timer.reset()
                current_state = STATE_EXIT

        # ---------------------------------------
        # Stage 3 & 4 
        # ---------------------------------------
        elif current_state == STATE_STAGE3:
            # --- Stage 3  ---
            pygame.mixer.stop()
            stage3 = Stage3(screen, mode=game_difficulty,game_state=game_state)
            next_stage_3 = stage3.run()
            
            if next_stage_3 == "quit":
                current_state = STATE_EXIT
            
            elif next_stage_3 == "dead":
                back = Stage2Back(screen)
                back.run()
                continue
            
            # --- Stage 4 ---
            elif next_stage_3 == "stage4":
                stage4 = Stage4(screen, mode=game_difficulty)
                result_4 = stage4.run()
                while True:
                    if result_4 == "stage4to3":
                        stage4to3 = Stage4To3(screen,num_fuels=count)
                        back = stage4to3.run()
                        if back == "stage4":
                            result_4 = stage4.resume()
                        else:
                            current_state = STATE_EXIT
                            break                  
                    elif result_4 == "dead" or result_4 == "success" or result_4 == "quit"or result_4=="fule_empty":
                        break
                    else:
                        break 

                if result_4 == "dead":
                    fuel_manager.set_fuel(count*10+70)
                    back = Stage2Back(screen)
                    back.run()
                    continue
                elif result_4=="fule_empty":
                    stage2 = Stage2(screen)
                    current_state = STATE_STAGE2 
                    #-----------1스테이지랑 2에서 쓰는 변수들 초기화 하긴 했는데 초기화 더 할 거 있으면 수정 좀-----#
                    Try = 0
                    count=0
                    MapInfo, ItemMapInfo, InvenInfo, InvenCnt = 0, 0, 0, [0,0,0,0,0]
                    timer.reset()
                    

                elif result_4 == "success":
                    current_state = STATE_EXIT 
                
                elif result_4 == "quit":
                    current_state = STATE_EXIT

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

'''
            elif result == "stage1":
                current_state = STATE_STAGE1
                # 인벤토리 복구 
                s2_inventory = stage2.inventory
                InvenCnt =[0, 0, 0, 0, 0]
                for item_name in s2_inventory:
                    if item_name in ITEM_NAME_TO_ID:
                        InvenCnt[ITEM_NAME_TO_ID[item_name] - 1] += 1
'''