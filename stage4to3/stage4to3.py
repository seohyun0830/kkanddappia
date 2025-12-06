import pygame
import random, sys
from engine import constants, maze, renderer, assets, sound
from stage4to3.ui import FuelGauge, FuelIndicator
from stage4to3.movement import try_move_player
from engine.fuel_manager import fuel_manager   # ★ fuel_manager 사용!


class Stage4To3:
    def __init__(self, screen,num_fuels):
        self.screen = screen
        pygame.font.init()

        # 타이머
        self.start_time = pygame.time.get_ticks()
        self.TIME_LIMIT = 30

        # 미로
        self.maze = maze.initialize_grid(constants.GRID_SIZE)

        # 플레이어
        self.player_row = 0
        self.player_col = 0
        self.key_states = {k: False for k in [
            pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT
        ]}
        self.move_timer = 0

        # 연료 스폰 설정
        self.NUM_FUELS = num_fuels #연료 2에서 가져온만큼 뿌리기
        self.FUEL_PER_ITEM = 10

        candidates = [
            (r, c)
            for r in range(constants.GRID_SIZE)
            for c in range(constants.GRID_SIZE)
            if self.maze[r][c] == constants.PATH and not (r == 0 and c == 0)
        ]
        random.shuffle(candidates)
        self.candidates = candidates

        self.fuel_positions = []
        self.collected_fuels = []

        self.fuel_spawn_index = 0
        self.FUEL_DELAY = 1000
        self.last_spawn = pygame.time.get_ticks()

        # 연료 UI (★ fuel_manager 사용)
        self.fuel_gauge = FuelGauge(0, 660, assets.fuel_gage_img)
        self.fuel_indicator = FuelIndicator(
            78, 760, assets.fuel_needle_img, fuel_manager.fuel, 100
        )

        self.font = assets.pressure_font_base

        # Back 버튼
        self.button_w = 160
        self.button_h = 160
        self.button_img = pygame.transform.scale(assets.back_button_img,
                                                 (self.button_w, self.button_h))

        self.button_x = constants.SCREEN_WIDTH - self.button_w - 20
        self.button_y = 20
        self.button_rect = pygame.Rect(self.button_x, self.button_y,
                                       self.button_w, self.button_h)

        self.fps = pygame.time.Clock()

        sound.play_bgm(sound.normal_bgm)

    # ---------------------------------------------------
    # 메인 실행
    # ---------------------------------------------------
    def run(self):
        running = True

        while running:
            self.fps.tick(40)
            self.move_timer += 1

            # 타이머
            now = pygame.time.get_ticks()
            elapsed = (now - self.start_time) // 1000
            remaining = max(0, self.TIME_LIMIT - elapsed)

            if remaining <= 0:
                return "stage4"  # ★ 시간 끝 → Stage4 복귀

            self.handle_events()
            self.spawn_fuel()
            self.move_player()

            self.draw(remaining)

            if self.check_back_button():
                return "stage4"

            pygame.display.update()

        return "stage4"

    # ---------------------------------------------------
    # 이벤트
    # ---------------------------------------------------
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN and e.key in self.key_states:
                self.key_states[e.key] = True

            if e.type == pygame.KEYUP and e.key in self.key_states:
                self.key_states[e.key] = False

    # ---------------------------------------------------
    # 연료 생성
    # ---------------------------------------------------
    def spawn_fuel(self):
        now = pygame.time.get_ticks()
        if self.fuel_spawn_index < self.NUM_FUELS and now - self.last_spawn >= self.FUEL_DELAY:
            sound.fuel_appear.play()
            self.fuel_positions.append(self.candidates[self.fuel_spawn_index])
            self.fuel_spawn_index += 1
            self.last_spawn = now

    # ---------------------------------------------------
    # 플레이어 이동
    # ---------------------------------------------------
    def move_player(self):
        if self.move_timer < constants.back_MOVE_COOLDOWN:
            return

        r, c = self.player_row, self.player_col

        if self.key_states[pygame.K_UP]:
            r, c = try_move_player(self.maze, (r, c), -1, 0, [], [])
        elif self.key_states[pygame.K_DOWN]:
            r, c = try_move_player(self.maze, (r, c), 1, 0, [], [])
        elif self.key_states[pygame.K_LEFT]:
            r, c = try_move_player(self.maze, (r, c), 0, -1, [], [])
        elif self.key_states[pygame.K_RIGHT]:
            r, c = try_move_player(self.maze, (r, c), 0, 1, [], [])

        self.player_row, self.player_col = r, c
        self.move_timer = 0

    # ---------------------------------------------------
    # Back 버튼 클릭
    # ---------------------------------------------------
    def check_back_button(self):
        mouse = pygame.mouse.get_pos()
        down = pygame.mouse.get_pressed()[0]

        if self.button_rect.collidepoint(mouse) and down:
            return True
        return False

    # ---------------------------------------------------
    # 화면 그리기
    # ---------------------------------------------------
    def draw(self, remaining):
        screen = self.screen

        # 배경
        screen.blit(assets.bk_img, (0, 0))

        # 타이머
        m = remaining // 60
        s = remaining % 60
        timer_text = f"{m:02}:{s:02}"
        timer_surface = assets.timer_font.render(timer_text, True, (255, 255, 255))
        screen.blit(timer_surface, (10, 10))

        # 미로
        renderer.draw_maze(
            screen, self.maze,
            constants.GRID_SIZE, constants.TILE_SIZE,
            constants.GRID_OFFSET_X, constants.GRID_OFFSET_Y,
            [], []
        )

        # 연료 UI
        self.fuel_gauge.draw(screen)
        self.fuel_indicator.update(fuel_manager.fuel)  # ★ 싱글톤
        self.fuel_indicator.draw(screen)

        # Fuel % 텍스트
        text = f"{int(fuel_manager.fuel)}%"
        txt_surface = self.font.render(text, True, (255, 255, 255))
        screen.blit(txt_surface, (63, 640))

        # Fuel 아이템
        self.draw_fuel_items()

        # Player
        px = constants.GRID_OFFSET_X + self.player_col * constants.TILE_SIZE + constants.TILE_SIZE//2
        py = constants.GRID_OFFSET_Y + self.player_row * constants.TILE_SIZE + constants.TILE_SIZE//2
        screen.blit(assets.player_img, (px - constants.TILE_SIZE//2, py - constants.TILE_SIZE//2))

        # Back 버튼
        screen.blit(self.button_img, (self.button_x, self.button_y))

        mouse_pos = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]
        is_hover = self.button_rect.collidepoint(mouse_pos)

        if is_hover:
            overlay = pygame.Surface((self.button_w, self.button_h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 60))
            screen.blit(overlay, (self.button_x, self.button_y))

            if mouse_down:
                overlay2 = pygame.Surface((self.button_w, self.button_h), pygame.SRCALPHA)
                overlay2.fill((0, 0, 0, 120))
                screen.blit(overlay2, (self.button_x, self.button_y))

    # ---------------------------------------------------
    # 연료 표시 + 먹기
    # ---------------------------------------------------
    def draw_fuel_items(self):
        screen = self.screen
        offset_x = constants.GRID_OFFSET_X
        offset_y = constants.GRID_OFFSET_Y

        fuel_size = int(constants.TILE_SIZE * 0.92)
        fuel_img = pygame.transform.scale(assets.fuel_img, (fuel_size, fuel_size))

        for (fr, fc) in self.fuel_positions:
            if (fr, fc) in self.collected_fuels:
                continue

            fx = offset_x + fc * constants.TILE_SIZE + constants.TILE_SIZE // 2
            fy = offset_y + fr * constants.TILE_SIZE + constants.TILE_SIZE // 2

            rect = fuel_img.get_rect(center=(fx, fy))
            screen.blit(fuel_img, rect)

            if self.player_row == fr and self.player_col == fc:
                sound.fuel_bgm.play()
                self.collected_fuels.append((fr, fc))

                fuel_manager.add_fuel(self.FUEL_PER_ITEM)
