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

    while True:
        if result == "stage4to3":
            stage4to3 = Stage4To3(screen)
            back = stage4to3.run()

            if back == "stage4":
                result = stage4.resume()
            else:
                break
        else:
            break
    '''
    pygame.quit()

if __name__ == "__main__":
    main()
