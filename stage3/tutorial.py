import pygame
from engine import constants
from stage3.draw_screen import draw_screen


class Stage3Tutorial:

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(constants.FONT_NAME, 48)  # 기본 폰트(크기 48)
        self.minifont = pygame.font.SysFont(constants.FONT_NAME, 20)

        # -------------------------
        # 튜토리얼 페이지 구성
        # 좌표(px, py)는 화살표가 가리킬 위치
        # -------------------------
        self.pages = [
            ("제한시간 5분 안에 운전실로 이동해야 합니다", pygame.Rect(0, 0, 147, 65), []),
            ("압력을 확인할 수 있습니다\n 압력은 미세하게 변동합니다\n 가끔 압력이 크게 변할 수 있으니 조심하세요", pygame.Rect(26, 575, 161, 204), []),
            ("압력이 40이하로 떨어지면 \n 파이프 내부에 음압 차이로\n 격벽이 자동으로 닫히고 \n이동효율도 크게 떨어집니다 ", pygame.Rect(26, 575, 161, 204),
             ["images/stage3/irongate.jpg"]),
            ("저압상태로 오래 있게 되면 HP가 감소합니다", pygame.Rect(970, 733, 230, 67), []),
            ("압력이 70이상이면 단선 발생확률이 증가합니다", pygame.Rect(26, 575, 161, 204),
             ["images/stage3/broken.png"]),
            ("단선이 발생하면 도착지점은 활성화 되지 않아요", pygame.Rect(931, 729, 19, 19),
             ["images/stage3/broken.png"]),
            ("비상상황이라고 너무 놀라지 마세요\n 미니드론이 도와줄거에요", pygame.Rect(0, 0, 0, 0),
             ["images/stage3/drone.png"]),
            ("드론이 텔레포트 아이템을 떨어뜨립니다\n R키를 누르면 이동하고 싶은 단선을 선택해\n 순간이동 할 수 있어요", pygame.Rect(0, 0, 0, 0),
             ["images/stage3/teleport.png", "images/stage3/rkey.png"]),
            ("방향키로 움직일 수 있습니다", pygame.Rect(252, 48, 19, 19),
             ["images/stage3/arrowkey.png"]),
            ("압력은 Q키와 W로 직접 조절할 수 있습니다", pygame.Rect(0, 0, 0, 0),
             ["images/stage3/qwekey.png"]),
            ("단선은 E키를 2초간 꾹 눌러 수리하세요", pygame.Rect(0, 0, 0, 0),
             ["images/stage3/qwekey.png", "images/stage3/broken.png"]),
            ("여기까지 도착하면 성공!",
             pygame.Rect(920, 719, 29, 29), []),
        ]


    def run(self, stage3):
        page = 0
        total = len(self.pages)

        while 0 <= page < total:
            text, rect, img_paths = self.pages[page]
            result = self.show_page(stage3, text, rect, img_paths)

            if result == "quit":
                return "quit"

            elif result == "next":
                page += 1

            elif result == "prev":
                page -= 1

            elif result == "skip":
                return


    def show_page(self, stage3, text, rect, img_paths):
        """
        각 튜토리얼 페이지 출력
        space 누르면 다음 페이지로 넘어감
        """
        showing = True
        imgs = []
        for path in img_paths:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (250, 250))   # 크기 조절
            imgs.append(img)

        while showing:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return "quit"

                if e.type == pygame.KEYDOWN:
                    # → 다음
                    if e.key == pygame.K_RIGHT:
                        return "next"

                    # ← 이전
                    if e.key == pygame.K_LEFT:
                        return "prev"

                    # SPACE = 전체 스킵
                    if e.key == pygame.K_SPACE:
                        return "skip"

            # Stage3 기본 화면 출력
            draw_screen(stage3)

            # 반투명 덮개
            overlay = pygame.Surface(
                (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 200))

            overlay.fill((0, 0, 0, 0), rect)

            self.screen.blit(overlay, (0, 0))

            # ---- 줄바꿈 지원 ----
            lines = text.split("\n")
            y = 120
            for line in lines:
                text_surf = self.font.render(line, True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=(constants.SCREEN_WIDTH // 2, y))
                self.screen.blit(text_surf, text_rect)
                y += self.font.get_height() + 5  # 줄 간격(5px)
            # ---------------------

            # ★ 이미지 출력 (텍스트 아래)
            if imgs:
                total_width = len(imgs) * 260   # 이미지 사이 여백 포함 총 길이
                start_x = (constants.SCREEN_WIDTH - total_width) // 2 + 130
                img_y = y + 100

                for img in imgs:
                    rect_img = img.get_rect(center=(start_x, img_y))
                    self.screen.blit(img, rect_img)
                    start_x += 260   # 다음 이미지 오른쪽으로 이동

            # SPACE 안내문
            arrow_text = "<-  ->"
            skip_text = "skip: space"

            arrow_surf = self.font.render(arrow_text, True, (200, 200, 200))
            skip_surf = self.minifont.render(skip_text, True, (200, 200, 200))

            # 첫 줄: 방향키 표시
            arrow_rect = arrow_surf.get_rect(
                center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT - 110)
            )

            # 둘째 줄: space 안내
            skip_rect = skip_surf.get_rect(
                center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT - 70)
            )

            self.screen.blit(arrow_surf, arrow_rect)
            self.screen.blit(skip_surf, skip_rect)

            pygame.display.update()
