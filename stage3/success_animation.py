SUCCESS_FRAMES = []

def preload_success_frames():
    global SUCCESS_FRAMES
    if SUCCESS_FRAMES:
        return

    for i in range(1, 8):
        img = pygame.image.load(f"images/stage3/win{i}.png").convert()
        img = pygame.transform.scale(img, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        SUCCESS_FRAMES.append(img)


import pygame, sys, random
from engine import constants, sound

def play_success_animation(screen):
    preload_success_frames()
    frames = SUCCESS_FRAMES
    clock = pygame.time.Clock()

    # 모든 BGM 초기 정리
    try: sound.stop_bgm()
    except: pass
    try: sound.high_bgm.stop()
    except: pass

    # 성공 브금 재생
    try: sound.success_bgm.play(-1)
    except: pass

    fade_surf = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)).convert()
    fade_surf.fill((0, 0, 0))

    # ================================
    #   1) win1 ~ win5 (걷기 연출)
    # ================================
    try: sound.walking.play(-1)
    except: pass

    for idx in range(5):   # 0~4
        frame = frames[idx]

        for _ in range(10):   # 15 → 10 (부드럽지만 가벼움)

            # QUIT 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            shake_x = random.randint(-2, 2)
            shake_y = random.randint(-2, 2)
            screen.blit(frame, (shake_x, shake_y))

            # 약한 페이드(매 프레임 적용하면 무거우니 랜덤 확률 적용)
            if random.random() < 0.5:
                fade_surf.set_alpha(random.randint(0, 40))
                screen.blit(fade_surf, (0, 0))

            pygame.display.update()
            clock.tick(18)

    try: sound.walking.stop()
    except: pass

    # ================================
    #   2) win6 (버튼 직전)
    # ================================
    for _ in range(12):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        shake_x = random.randint(-1, 1)
        shake_y = random.randint(-1, 1)
        screen.blit(frames[5], (shake_x, shake_y))
        pygame.display.update()
        clock.tick(16)

    # 클릭 사운드
    try: sound.click.play()
    except: pass

    # ================================
    #   3) win7 (버튼 눌림)
    # ================================
    for _ in range(12):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        shake_x = random.randint(-1, 1)
        shake_y = random.randint(-1, 1)
        screen.blit(frames[6], (shake_x, shake_y))

        fade_surf.set_alpha(random.randint(30, 90))
        screen.blit(fade_surf, (0, 0))

        pygame.display.update()
        clock.tick(15)

    # ================================
    #   4) 마지막 페이드아웃
    # ================================
    for alpha in range(0, 255, 12):   # 10 → 12 (부드럽고 가벼움)
        fade_surf.set_alpha(alpha)
        screen.blit(fade_surf, (0, 0))
        pygame.display.update()
        clock.tick(20)

    # ================================
    #   모든 사운드 정리
    # ================================
    try: sound.success_bgm.stop()
    except: pass
    try: sound.walking.stop()
    except: pass
    try: sound.click.stop()
    except: pass

