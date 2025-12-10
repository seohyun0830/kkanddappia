import pygame, sys
from engine import constants, assets
from stage3 import Stage3
from stage4.stage4 import Stage4
from stage3.story import Stage3Story
from stage4to3.stage4to3 import Stage4To3
from stage2_back.stage2_back_main import Stage2Back
from engine.fuel_manager import fuel_manager
import builtins


def main():
    pygame.init()
    screen = pygame.display.set_mode(
        (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    )
    builtins.shared_screen = screen
    pygame.display.set_caption("stage3,4 merge")

    assets.load_all()

    # ------------------------------------
    # 1) 스토리 & 튜토리얼 (딱 한번만)
    # ------------------------------------
    story = Stage3Story(screen)
    story.run()
    pygame.event.clear()

    game_state = {"stage3_tutorial_done": False}

    # ------------------------------------
    # 2) 메인 루프
    # ------------------------------------
    
    while True:
        pygame.mixer.stop()

        # ===== Stage 3 =====
        stage3 = Stage3(screen, game_state=game_state)
        next_stage = stage3.run()
        
        if next_stage == "quit":
            pygame.quit()
            sys.exit()

        if next_stage == "dead":
            back = Stage2Back(screen)
            back.run()
            continue

        # ===== Stage 4 =====
        if next_stage == "stage4":
            fuel_manager.fuel = 70
            difficulty = "hard"
            stage4 = Stage4(screen, mode=difficulty)
            result = stage4.run()

            # stage4 내부 반복 처리
            while result == "stage4to3":
                stage4to3 = Stage4To3(screen)
                back = stage4to3.run()

                if back == "stage4":
                    result = stage4.resume()
                else:
                    break

            # stage4 결과
            if result == "dead":
                back = Stage2Back(screen)
                back.run()
                continue

            if result == "success":
                # 여기서 엔딩 가능
                break

    pygame.quit()
    '''
    while True:
        stage4 = Stage4(screen)
        result = stage4.run()

                # stage4 내부 반복 처리
        while result == "stage4to3":
            stage4to3 = Stage4To3(screen)
            back = stage4to3.run()

            if back == "stage4":
                result = stage4.resume()
            else:
                break

                # stage4 결과
        if result == "dead":
            fuel_manager.fuel = 80
            back = Stage2Back(screen)
            back.run()
            continue

        if result == "success":
                    # 여기서 엔딩 가능
            break
    pygame.quit()
'''

if __name__ == "__main__":
    main()
