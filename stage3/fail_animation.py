import pygame, sys, random
from engine import constants, sound

# ----------------------------
# 이미지 미리 로드 (프로그램 실행 시 1번만)
# ----------------------------
FAIL1_FRAMES = []
FAIL2_FRAMES = []

def preload_fail_images():
    global FAIL1_FRAMES, FAIL2_FRAMES

    if not FAIL1_FRAMES:
        for i in range(1, 5):
            img = pygame.image.load(f"images/stage3/fail1_{i}.png").convert()
            img = pygame.transform.scale(img, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            FAIL1_FRAMES.append(img)

    if not FAIL2_FRAMES:
        for i in range(1, 5):
            img = pygame.image.load(f"images/stage3/fail2_{i}.png").convert()
            img = pygame.transform.scale(img, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            FAIL2_FRAMES.append(img)


# -----------------------------
# 산소 부족 실패 애니메이션
# -----------------------------
def play_oxygen_fail(screen):
    preload_fail_images()
    frames = FAIL1_FRAMES
    clock = pygame.time.Clock()

    sound.stop_bgm()
    try: sound.high_bgm.stop()
    except: pass
    try: sound.oxfail_bgm.play()
    except: pass

    fade = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)).convert()
    fade.fill((0, 0, 0))

    # 4장 × 8프레임 = 32프레임 (아주 빠르고 끊김 없음)
    for frame in frames:
        for _ in range(16):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            shake_x = random.randint(-2, 2)
            shake_y = random.randint(-2, 2)

            screen.blit(frame, (shake_x, shake_y))

            fade.set_alpha(random.randint(80, 150))
            screen.blit(fade, (0, 0))

            pygame.display.update()
            clock.tick(16)

    # 마지막 암전
    for alpha in range(0, 255, 20):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        clock.tick(20)


# -----------------------------
# 과압력 실패 애니메이션
# -----------------------------
def play_overpressure_fail(screen):
    preload_fail_images()
    frames = FAIL2_FRAMES
    clock = pygame.time.Clock()

    sound.stop_bgm()
    try: sound.high_bgm.stop()
    except: pass

    fade = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)).convert()
    fade.fill((0, 0, 0))

    fire_sound_played = False

    for idx, frame in enumerate(frames):

        if idx == 0:
            try: sound.beep_error.play()
            except: pass
        elif idx == 1:
            try: sound.explosion.play()
            except: pass
        elif idx >= 2 and not fire_sound_played:
            try: sound.fire_loop.play(-1)
            except: pass
            fire_sound_played = True

        for _ in range(8):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            shake_x = random.randint(-4, 4)
            shake_y = random.randint(-4, 4)

            screen.blit(frame, (shake_x, shake_y))

            fade.set_alpha(random.randint(50, 120))
            screen.blit(fade, (0, 0))

            pygame.display.update()
            clock.tick(20)

    for alpha in range(0, 255, 30):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        clock.tick(30)

    try: sound.fire_loop.stop()
    except: pass
