import pygame
from engine import constants, assets
from stage3 import Stage3
from stage4.stage4 import Stage4
from stage4to3.stage4to3 import Stage4To3
import builtins 

def main():
    pygame.init()
    screen = pygame.display.set_mode(
        (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    )
    builtins.shared_screen=screen

    pygame.display.set_caption("stage3,4 merge")

    assets.load_all()
    '''
    # -------- Stage 3 --------
    stage3 = Stage3(screen)
    next_stage = stage3.run()
    
    # -------- Stage 4 --------
    if next_stage == "stage4":
        stage4=Stage4(screen)
        result=stage4.run()

        while True:
            if result=="stage4to3":
                stage4to3=Stage4To3(screen)
                back=stage4to3.run()

                if back=="stage4":
                    result=stage4.resume()

                else:
                    break
            else:
                break
                    

    '''
    stage4 = Stage4(screen)
    result = stage4.run()

    # [수정] 들여쓰기 레벨 주의 (if문 밖으로 꺼냈으니 왼쪽으로 당겨야 함)
    while True:
        if result == "stage4to3":
            stage4to3 = Stage4To3(screen)
            back = stage4to3.run()

            if back == "stage4":
                # resume() 대신 다시 run()을 하거나 초기화된 상태를 원하면
                # 상황에 따라 stage4.reset() 같은 게 필요할 수도 있음
                result = stage4.resume() # 또는 stage4.run()
            else:
                break
        else:
            # stage4to3이 아니면(클리어하거나 종료했으면) 루프 탈출
            break
    pygame.quit()

if __name__ == "__main__":
    main()
