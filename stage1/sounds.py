import pygame

pygame.mixer.init() # 믹서 초기화

# 사운드 로드
#bgm_stage1 = "assets/stage1_bgm.mp3" # 음악은 파일 경로만 저장하거나
# bgm은 load를 플레이 직전에 하는 게 보통입니다.

# 효과음은 객체로 미리 로드
sfx_jump = pygame.mixer.Sound("stage1/assets/jump.wav")
sfx_step = pygame.mixer.Sound("stage1/assets/step.wav")
sfx_breaking = pygame.mixer.Sound("stage1/assets/breaking.mp3")