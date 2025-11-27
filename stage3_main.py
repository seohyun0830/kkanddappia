import pygame
from engine import constants, assets
from stage3 import Stage3 


def main():
    pygame.init()

    screen = pygame.display.set_mode(
        (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    )
    pygame.display.set_caption("main_Stage3")

    assets.load_all() #모든 에셋들 로드
    
    stage3 = Stage3(screen)
    next_stage = stage3.run()

    pygame.quit()


if __name__ == "__main__":
    main()
