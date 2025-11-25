import pygame
from engine import constants, assets
from stage3 import Stage3   # __init__.py 덕분에 이렇게 import 가능

def main():
    pygame.init()

    screen = pygame.display.set_mode(
        (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    )
    pygame.display.set_caption("main_Stage3")

    assets.load_all()
    
    stage = Stage3(screen)
    next_stage = stage.run()

    pygame.quit()


if __name__ == "__main__":
    main()
