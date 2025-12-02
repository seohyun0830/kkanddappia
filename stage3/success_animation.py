import pygame
import random
import time
from engine import constants, sound


# ----------------------------------------
#   성공 애니메이션 이미지 로드
#   win1 ~ win7
# ----------------------------------------
def load_success_frames():
    frames = []
    for i in range(1, 8):
        img = pygame.image.load(f"images/stage3/win{i}.png").convert()
        img = pygame.transform.scale(
            img, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        )
        frames.append(img)
    return frames


# ----------------------------------------
#   성공 애니메이션 실행
# ----------------------------------------
def play_success_animation(screen):
    frames = load_success_frames()
    clock = pygame.time.Clock()

    # 기존 브금 정지
    sound.stop_bgm()
    try:
        sound.high_bgm.stop()
    except:
        pass

    # 성공 브금 재생
    try:
        sound.success_bgm.play(-1)
    except:
        pass

    # 걷는 소리는 win1~win5 전용
    walking_sound_played = False

    # 페이드용 surface
    fade_surf = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    fade_surf.fill((0, 0, 0))

    # ----------------------------------------
    #   1) win1~win5 : 걷는 장면
    # ----------------------------------------
    for idx in range(5):  # 0~4 → win1~win5
        frame = frames[idx]

        if not walking_sound_played:
            try:
                sound.walking.play(-1)   # 걷는 소리 loop
            except:
                pass
            walking_sound_played = True

        # 프레임 재생
        for _ in range(25):
            shake_x = random.randint(-3, 3)
            shake_y = random.randint(-3, 3)

            screen.blit(frame, (shake_x, shake_y))

            # 살짝씩 어두워지는 효과(낮음)
            fade_alpha = random.randint(0, 60)
            fade_surf.set_alpha(fade_alpha)
            screen.blit(fade_surf, (0, 0))

            pygame.display.update()
            clock.tick(12)

    # 걷는 소리 중지
    try:
        sound.walking.stop()
    except:
        pass

    # ----------------------------------------
    #   2) win6 → win7 : 버튼 누르기
    # ----------------------------------------

    # win6 먼저 표시
    for _ in range(20):
        shake_x = random.randint(-2, 2)
        shake_y = random.randint(-2, 2)
        screen.blit(frames[5], (shake_x, shake_y))
        pygame.display.update()
        clock.tick(12)

    # 버튼 눌리는 순간 "딸깍!"
    try:
        sound.click.play()
    except:
        pass

    # win7 표시 (눌린 상태)
    for _ in range(25):
        shake_x = random.randint(-2, 2)
        shake_y = random.randint(-2, 2)

        screen.blit(frames[6], (shake_x, shake_y))

        fade_alpha = random.randint(20, 80)
        fade_surf.set_alpha(fade_alpha)
        screen.blit(fade_surf, (0, 0))

        pygame.display.update()
        clock.tick(12)

    # ----------------------------------------
    #   3) 마지막 완전 페이드아웃
    # ----------------------------------------
    for alpha in range(0, 255, 10):
        fade_surf.set_alpha(alpha)
        screen.blit(fade_surf, (0, 0))
        pygame.display.update()
        clock.tick(20)

    time.sleep(2)  # 여운

        # --- 애니메이션 종료 후 모든 소리 정지 ---
    try:
        sound.stop_bgm()        # mixer.music로 재생되는 브금 정지
    except:
        pass

    try:
        sound.success_bgm.stop()  # 성공 브금(효과음 기반) 정지
    except:
        pass

    try:
        sound.walking.stop()
    except:
        pass

    try:
        sound.click.stop()
    except:
        pass

