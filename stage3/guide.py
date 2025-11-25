import pygame
from engine import constants, assets

"""
3stage가이드북 
열기,닫기 상태 관리
페이지 이동, 반투명 오버레이
"""

class GuideBook:
    def __init__(self):
        self.open = False
        self.current_page = 1
        self.total_pages = 5
        self.pause_start_time = 0   # 열린 시간 기록
        self.game_paused_time = 0   # 전체 일시정지 누적시간

    #가이드북 버튼 클릭여부
    def handle_button_click(self, x, y):
        btn_rect = assets.guide_book_button.get_rect(
            topleft=(constants.SCREEN_WIDTH - 120, 20)
        )

        # 버튼을 누르지 않았다면 False 그대로 반환
        if not btn_rect.collidepoint(x, y):
            return False

        # 가이드북 토글
        if not self.open:
            # 처음 열었을 때
            self.open = True
            self.current_page = 1
            self.pause_start_time = pygame.time.get_ticks()

        else:
            # 닫을 때
            self.open = False
            paused_duration = pygame.time.get_ticks() - self.pause_start_time
            self.game_paused_time += paused_duration

        return True

    #가이드북 활성화 상태 키보드 이벤트
    def handle_open_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False

            if e.type == pygame.KEYDOWN:
                # ESC → 닫기
                if e.key == pygame.K_ESCAPE:
                    self.close()
                    continue

                # 좌우 페이지 이동
                if e.key == pygame.K_LEFT:
                    self.current_page = max(1, self.current_page - 1)
                elif e.key == pygame.K_RIGHT:
                    self.current_page = min(self.total_pages, self.current_page + 1)

            # 마우스로 클릭해도 페이지 이동
            if e.type == pygame.MOUSEBUTTONDOWN:
                x, y = e.pos

                # 버튼 다시 눌러도 닫기 가능
                if self.handle_button_click(x, y):
                    continue

                # 화면 왼쪽 영역 → 이전 페이지
                if x < 200:
                    self.current_page = max(1, self.current_page - 1)

                # 화면 오른쪽 영역 → 다음 페이지
                elif x > constants.SCREEN_WIDTH - 200:
                    self.current_page = min(self.total_pages, self.current_page + 1)

        return True

    def close(self):
        self.open = False
        paused_duration = pygame.time.get_ticks() - self.pause_start_time
        self.game_paused_time += paused_duration

    def draw(self, screen):
        # 1) 반투명 검은 배경
        overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        overlay.set_alpha(210)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # 2) 페이지 이미지 선택
        guide_imgs = assets.guide_images
        img = guide_imgs[self.current_page - 1]

        # 3) 화면 중앙 700x700로 스케일링
        scaled = pygame.transform.scale(img, (700, 700))
        rect = scaled.get_rect(center=(constants.SCREEN_WIDTH // 2,
                                       constants.SCREEN_HEIGHT // 2))
        screen.blit(scaled, rect)

        # 4) 좌우 페이지 버튼 텍스트
        font = pygame.font.SysFont(constants.FONT_NAME, 40, bold=True)
        left = font.render("<", True, (255, 255, 255))
        right = font.render(">", True, (255, 255, 255))

        screen.blit(left, (120, constants.SCREEN_HEIGHT // 2 - 20))
        screen.blit(right, (constants.SCREEN_WIDTH - 120, constants.SCREEN_HEIGHT // 2 - 20))

        # 5) ESC 안내
        exit_text = font.render("ESC : 닫기", True, (180, 180, 180))
        screen.blit(exit_text, (constants.SCREEN_WIDTH // 2 - 100,
                                constants.SCREEN_HEIGHT - 80))
