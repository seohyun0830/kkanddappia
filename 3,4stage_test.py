import pygame
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
    builtins.shared_screen=screen

    pygame.display.set_caption("stage3,4 merge")

    assets.load_all()
    
   
    # --------Story-----------
    #3스토리는 처음 플레이 할 때 한번만 나오게
    story = Stage3Story(screen)
    story.run() 
    pygame.event.clear()

    while True:
            # -------- Stage 3 --------
            stage3 = Stage3(screen)
            next_stage = stage3.run()

            if next_stage=="dead":
                back_cutscene = Stage2Back(screen)
                back_cutscene.run()
                continue
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
                    elif result=="dead":
                        break
                    elif result=="success":
                        break
                                    
                if result=="dead":
                    fuel_manager.fuel=80    #연료 초기화
                    back_cutscene = Stage2Back(screen)
                    back_cutscene.run()
                    continue 
                                
            pygame.quit()

if __name__ == "__main__":
    main()
