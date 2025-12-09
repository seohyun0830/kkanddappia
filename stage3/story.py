import pygame
import random
from engine import constants

class Stage3Story:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        # 배경 로드
        self.bg = pygame.image.load("images/stage3/piperoom.png")
        self.bg = pygame.transform.scale(
            self.bg,
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        )
        self.bg_open = pygame.image.load("images/stage3/piperoom2.png")
        self.bg_open = pygame.transform.scale(
            self.bg_open,
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        )

        self.font = pygame.font.Font('DungGeunMO.ttf', 90)

        # 러닝 애니메이션 이미지
        self.ani1 = pygame.image.load("images/stage3/ani1.png").convert_alpha()
        self.ani2 = pygame.image.load("images/stage3/ani2.png").convert_alpha()
        self.ani3 = pygame.image.load("images/stage3/ani3.png").convert_alpha()
        self.ani1 = pygame.transform.scale(self.ani1, (150, 200))
        self.ani2 = pygame.transform.scale(self.ani2, (150, 200))
        self.ani3 = pygame.transform.scale(self.ani3, (150, 200))
    

        self.animation_timer = 0
        self.animation_speed = 300

        # 플레이어 위치
        self.player_x = -150
        self.player_y = 440
        self.run_speed = 6

        # 사운드
        self.siren = pygame.mixer.Sound("sounds/stage3/사이렌.mp3")
        self.alert = pygame.mixer.Sound("sounds/stage3/시스템경고음.mp3")
        self.siren.set_volume(0.3)
        self.alert.set_volume(0.9)

        # 플래시 & 흔들림
        self.shake_amount = 5
        self.reached = False

    def run(self):
        self.siren.play(-1)
        self.alert.play()

        start = pygame.time.get_ticks()
        running = True

        while running:
            dt = self.clock.tick(40)
            self.animation_timer += dt
            now = pygame.time.get_ticks()
            elapsed = now - start

            # 이벤트 처리
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    running = False

            # 플레이어 이동
            if self.player_x < 710:
                self.player_x += self.run_speed
            else:
                self.reached = True
                self.bg = self.bg_open

            # 애니메이션 프레임 선택
            if not self.reached:
                mod = (self.animation_timer // self.animation_speed) % 3
                if mod == 0:
                    current_img = self.ani1
                elif mod == 1:
                    current_img = self.ani2
                else:
                    current_img = self.ani3
            else:
                current_img = self.ani3  # 도착 후 고정

            # 그리기
            self.draw(current_img, elapsed)

        self.cleanup_sounds()
        pygame.mixer.stop()
        pygame.mixer.music.stop()

    def draw(self, current_img, elapsed):
        shake_x = random.randint(-self.shake_amount, self.shake_amount)
        shake_y = random.randint(-self.shake_amount, self.shake_amount)

        # 배경
        self.screen.blit(self.bg, (shake_x, shake_y))

        # 플레이어
        self.screen.blit(current_img, (self.player_x + shake_x, self.player_y + shake_y))

        # 빨간 플래시
        if (elapsed // 300) % 2 == 0:
            overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            overlay.fill((255, 0, 0))
            overlay.set_alpha(80)
            self.screen.blit(overlay, (0, 0))

        # ================================
        #   PRESS SPACE TO CONTINUE 표시
        # ================================
        if self.reached:  # 문 근처 도달하면 표시
            # 글자 깜빡임 효과
            blink = (pygame.time.get_ticks() // 500) % 2

            if blink == 0:
                text = "PRESS SPACE TO 3STAGE"
                surface = self.font.render(text, True, (255, 255, 255))
                rect = surface.get_rect(center=(constants.SCREEN_WIDTH // 2, 200))
                self.screen.blit(surface, rect)

        pygame.display.flip()

    
    def cleanup_sounds(self):
        try:
            self.siren.stop()
            self.alert.stop()
        except:
            pass
