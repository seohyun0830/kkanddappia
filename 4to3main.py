import pygame
from engine import constants, assets
from stage4to3.stage4to3 import Stage4To3

pygame.init()

# 화면 생성
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

# 에셋 로드
assets.load_all()

# 스테이지 실행
stage = Stage4To3(screen)
stage.run()

pygame.quit()
