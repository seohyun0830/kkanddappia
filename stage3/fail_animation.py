import pygame
import random
import time
from engine import constants, sound


def load_fail_frames():
    frames = []
    for i in range(1, 5):  # fail1_1 ~ fail1_4
        img = pygame.image.load(f"images/stage3/fail1_{i}.png").convert()
        img = pygame.transform.scale(img, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        frames.append(img)
    return frames


def play_oxygen_fail(screen):
    frames = load_fail_frames()
    clock = pygame.time.Clock()

    sound.stop_bgm()
    try:
        sound.high_bgm.stop()
    except:
        pass

    try:
        sound.oxfail_bgm.play()
    except:
        pass

    fade_surf = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    fade_surf.fill((0, 0, 0))

    # ===== 애니메이션 =====
    for frame in frames:
        for _ in range(25):  # 천천히
            shake_x = random.randint(-5, 5)
            shake_y = random.randint(-5, 5)

            # 흔들림 적용된 프레임
            screen.blit(frame, (shake_x, shake_y))

            # 점점 까매지는 효과
            fade_alpha = random.randint(50, 140)
            fade_surf.set_alpha(fade_alpha)
            screen.blit(fade_surf, (0, 0))

            pygame.display.update()
            clock.tick(12)

    # 마지막 완전 암전
    for alpha in range(0, 255, 12):
        fade_surf.set_alpha(alpha)
        screen.blit(fade_surf, (0, 0))
        pygame.display.update()
        clock.tick(20)

    screen.blit(fade_surf, (0, 0))
    pygame.display.update()
    time.sleep(5)


def load_fail2_frames():
    frames = []
    for i in range(1, 5):  # fail2_1 ~ fail2_4
        img = pygame.image.load(f"images/stage3/fail2_{i}.png").convert()
        img = pygame.transform.scale(img, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        frames.append(img)
    return frames


def play_overpressure_fail(screen):
    frames = load_fail2_frames()
    clock = pygame.time.Clock()

    # 기존 브금 정지
    sound.stop_bgm()
    try:
        sound.high_bgm.stop()
    except:
        pass

    fade_surf = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    fade_surf.fill((0, 0, 0))

    fire_sound_played = False

    # ===== 애니메이션 순차 재생 =====
    for idx, frame in enumerate(frames):
        # 사운드 처리
        if idx == 0:
            try:
                sound.beep_error.play()
            except:
                pass

        elif idx == 1:
            try:
                sound.explosion.play()
            except:
                pass

        elif idx >= 2 and not fire_sound_played:
            try:
                sound.fire_loop.play(-1)  # 불소리 loop
            except:
                pass
            fire_sound_played = True

        # 프레임 애니메이션
        for _ in range(25):
            shake_x = random.randint(-5, 5)
            shake_y = random.randint(-5, 5)

            screen.blit(frame, (shake_x, shake_y))

            fade_alpha = random.randint(40, 160)
            fade_surf.set_alpha(fade_alpha)
            screen.blit(fade_surf, (0, 0))

            pygame.display.update()
            clock.tick(12)

    # ===== 마지막 암전 =====
    for alpha in range(0, 255, 10):
        fade_surf.set_alpha(alpha)
        screen.blit(fade_surf, (0, 0))
        pygame.display.update()
        clock.tick(20)

    # 불소리 정지
    try:
        sound.fire_loop.stop()
    except:
        pass

    # 암전 유지 3초
    time.sleep(3)
