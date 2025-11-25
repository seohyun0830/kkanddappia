import pygame
import random

from engine import  constants, sound, maze

# Stage3 모듈들
from stage3.movement import try_move_player
from stage3.pressure import update_pressure_small, update_pressure_spike, user_pressure_control
from stage3.repair import RepairSystem
from stage3.broken import generate_broken_tile
from stage3.draw_screen import draw_screen
from stage3.guide import GuideBook


class Stage3:

    def __init__(self, screen, game_state=None):
        self.screen = screen
        self.game_state = game_state

        pygame.font.init()

        # 타이머
        self.start_time = pygame.time.get_ticks()

        # 미로 데이터
        self.maze_data = maze.initialize_grid(constants.GRID_SIZE)
        self.iron_gates = []
        self.broken_tiles = []

        # 플레이어 위치
        self.player_row = 0
        self.player_col = 0

        # 이동 변속 관련
        self.move_timer = 0
        self.key_states = {k: False for k in [
            pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT
        ]}

        # 압력 시스템
        self.pressure = 50
        self.n = 3
        self.key_pressed = False
        self.low_pressure_start_time = None
        self.last_broken_time = 0

        # HP
        self.hp = constants.MAX_HP

        # 수리 시스템
        self.repair = RepairSystem()

        # 가이드북 시스템
        self.guide = GuideBook()

        # BGM
        self.current_bgm_state = "normal"
        self.high_playing = False
        sound.play_bgm(sound.normal_bgm)

        # 이벤트 타이머 설정
        self.PRESSURE_UPDATE_EVENT = pygame.USEREVENT + 2
        self.SPIKE_UPDATE_EVENT = pygame.USEREVENT + 3

        pygame.time.set_timer(self.PRESSURE_UPDATE_EVENT, constants.PRESSURE_UPDATE_INTERVAL)
        pygame.time.set_timer(
            self.SPIKE_UPDATE_EVENT,
            random.randint(constants.MIN_SPIKE_INTERVAL, constants.MAX_SPIKE_INTERVAL),
            1
        )

        self.fps = pygame.time.Clock()

    #엔딩화면들
    def show_gameover(self):
        #압력 0,100,HP=0
        sound.stop_bgm()
        sound.fail_bgm.play()

        img = pygame.image.load("images/gameover.png")
        scale = min(constants.SCREEN_WIDTH / img.get_width(), constants.SCREEN_HEIGHT / img.get_height())
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        rect = img.get_rect(center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2))

        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return

            self.screen.fill((0,0,0))
            self.screen.blit(img, rect)
            pygame.display.update()

    def show_timeover(self):
        sound.stop_bgm()
        sound.fail_bgm.play()

        img = pygame.image.load("images/timeover.png")
        scale = min(constants.SCREEN_WIDTH / img.get_width(), constants.SCREEN_HEIGHT / img.get_height())
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        rect = img.get_rect(center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2))

        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return

            self.screen.fill((0,0,0))
            self.screen.blit(img, rect)
            pygame.display.update()

    #성공시퀀스
    def show_success(self):
        sound.stop_bgm()
        sound.success_bgm.play()

        bg = pygame.image.load("images/ending_img3.png")
        spaceship_img = pygame.image.load("images/spaceship.png")

        scale = min(constants.SCREEN_WIDTH / bg.get_width(), constants.SCREEN_HEIGHT / bg.get_height())
        bg = pygame.transform.scale(bg, (int(bg.get_width() * scale), int(bg.get_height() * scale)))
        bg_rect = bg.get_rect(center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2))

        spaceship_scale = 2.0
        spaceship_y = constants.SCREEN_HEIGHT - 300
        spaceship_x = constants.SCREEN_WIDTH // 2

        running = True
        while running:

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return

            self.screen.blit(bg, bg_rect)

            spaceship_y -= 60 * (1/60)
            spaceship_scale -= 0.003

            if spaceship_scale < 0:
                spaceship_scale = 0

            new_w = int(spaceship_img.get_width() * spaceship_scale)
            new_h = int(spaceship_img.get_height() * spaceship_scale)

            if new_w > 0 and new_h > 0:
                scaled_ship = pygame.transform.scale(spaceship_img, (new_w, new_h))
                rect = scaled_ship.get_rect(center=(spaceship_x, int(spaceship_y)))
                self.screen.blit(scaled_ship, rect)

            pygame.display.update()

            if spaceship_y < -150:
                return

    # ---------------------------------------------------
    #                  메인 루프
    # ---------------------------------------------------
    #menu는 게임오버하면 돌아갈 문자열
    def run(self):
        running = True

        while running:
            self.fps.tick(constants.FPS)

            # 가이드북 활성화 시 게임 정지
            if self.guide.open:
                if not self.guide.handle_open_events():
                    return "menu"
                self.guide.draw(self.screen)
                pygame.display.update()
                continue

            # 이벤트 처리
            running = self.handle_events()
            if not running:
                return "menu"

            self.update_logic()
            draw_screen(self)
            pygame.display.update()

            # HP 0 , 압력0/100 -> 실패
            if self.hp <= 0 or self.pressure <= 0 or self.pressure>=100:
                self.show_gameover()
                return "menu"

            # 시간 초과 체크
            now = pygame.time.get_ticks()
            elapsed = now - self.start_time - self.guide.game_paused_time
            if elapsed >= constants.TOTAL_GAME_TIME_SECONDS * 1000:
                self.show_timeover()
                return "menu"

            # 클리어
            if self.check_clear():
                self.show_success()
                return "stage4"

        return "menu"

    #이벤트 로직
    def handle_events(self):
        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                return False

            if e.type == pygame.KEYDOWN and e.key in self.key_states:
                self.key_states[e.key] = True

            if e.type == pygame.KEYUP and e.key in self.key_states:
                self.key_states[e.key] = False

            # 수리
            if e.type == pygame.KEYDOWN and e.key == pygame.K_e:
                self.repair.start(self.player_row, self.player_col, self.broken_tiles)

            if e.type == pygame.KEYUP and e.key == pygame.K_e:
                self.repair.cancel()

            # 가이드북
            if e.type == pygame.MOUSEBUTTONDOWN:
                x, y = e.pos
                if self.guide.handle_button_click(x, y):
                    continue

            # 압력 변화 이벤트
            if e.type == self.PRESSURE_UPDATE_EVENT:
                self.pressure = update_pressure_small(self.pressure)

            if e.type == self.SPIKE_UPDATE_EVENT:
                self.pressure = update_pressure_spike(self.pressure)

                pygame.time.set_timer(
                    self.SPIKE_UPDATE_EVENT,
                    random.randint(constants.MIN_SPIKE_INTERVAL, constants.MAX_SPIKE_INTERVAL),
                    1
                )

        return True

    #게임 로직
    def update_logic(self):

        # 이동 딜레이 적용
        self.move_timer += 1
        effective_cd = constants.MOVE_COOLDOWN * (3 if self.pressure <= 40 else 1)

        if self.move_timer >= effective_cd:
            self.handle_movement()
            self.move_timer = 0

        # 수리 진행
        self.repair.update(self.maze_data)

        # 압력 직접 제어 (Q/W)
        self.pressure, self.key_pressed = user_pressure_control(
            self.pressure, self.key_pressed, self.n
        )

        # 고압 → 단선 발생
        self.update_broken_tiles()

        # HP 체크
        self.update_hp()

        # BGM 교체
        self.update_bgm()

        self.update_iron_gates()



    def update_iron_gates(self):
    # 압력이 40 이하일 때 철문 생성
        if self.pressure <= 40:

        # 이미 철문이 존재하면 또 생성하지 않음
            if any(g[2] for g in self.iron_gates):
                return

        # 랜덤 철문 생성
            num_new_gates = random.randint(5, 15)
            candidates = []

            for r in range(constants.GRID_SIZE):
                for c in range(constants.GRID_SIZE):
                    if self.maze_data[r][c] == constants.PATH:
                        candidates.append((r, c))

            random.shuffle(candidates)
            selected = candidates[:num_new_gates]

            self.iron_gates.clear()

            for (r, c) in selected:
                self.iron_gates.append([r, c, True, -constants.TILE_SIZE])  # [r,c,closed,slide_y]
                self.maze_data[r][c] = constants.IRON_GATE

        else:
            # 압력 회복 → 철문 제거
            for g in self.iron_gates:
                r, c, closed, slide_y = g
                self.maze_data[r][c] = constants.PATH

            self.iron_gates.clear()


    def handle_movement(self):
        r, c = self.player_row, self.player_col

        if self.key_states[pygame.K_UP]:
            r, c = try_move_player(self.maze_data, (r, c), -1, 0, self.iron_gates, self.broken_tiles)
        elif self.key_states[pygame.K_DOWN]:
            r, c = try_move_player(self.maze_data, (r, c), 1, 0, self.iron_gates, self.broken_tiles)
        elif self.key_states[pygame.K_LEFT]:
            r, c = try_move_player(self.maze_data, (r, c), 0, -1, self.iron_gates, self.broken_tiles)
        elif self.key_states[pygame.K_RIGHT]:
            r, c = try_move_player(self.maze_data, (r, c), 0, 1, self.iron_gates, self.broken_tiles)

        self.player_row, self.player_col = r, c

    def update_broken_tiles(self):
        now = pygame.time.get_ticks()

        if self.pressure >= 70 and now - self.last_broken_time >= 3000:

            if self.pressure < 80:
                broken_chance = 0.01
            elif self.pressure < 90:
                broken_chance = 0.02
            else:
                broken_chance = 0.03

            if random.random() < broken_chance:
                generate_broken_tile(self.maze_data, self.broken_tiles)
                self.pressure = max(0, self.pressure - 5)
                self.last_broken_time = now

    def update_hp(self):
        if self.pressure <= 40:
            if self.low_pressure_start_time is None:
                self.low_pressure_start_time = pygame.time.get_ticks()
            else:
                if pygame.time.get_ticks() - self.low_pressure_start_time >= 3000:
                    self.hp = max(0, self.hp - 5)
                    self.low_pressure_start_time = pygame.time.get_ticks()
        else:
            self.low_pressure_start_time = None

    def update_bgm(self):

        # 저압 브금
        if self.pressure <= 40:
            if self.current_bgm_state != "low":
                sound.stop_bgm()
                sound.play_bgm(sound.low_bgm)
                self.current_bgm_state = "low"

        # 고압 브금(효과음)
        elif self.pressure >= 70:
            if not self.high_playing:
                sound.high_bgm.play(-1)
                self.high_playing = True

        # 정상
        else:
            if self.high_playing:
                sound.high_bgm.stop()
                self.high_playing = False

            if self.current_bgm_state != "normal":
                sound.stop_bgm()
                sound.play_bgm(sound.normal_bgm)
                self.current_bgm_state = "normal"

    def check_clear(self):
        # 모든 단선 수리
        all_fixed = all(not b[2] for b in self.broken_tiles)

        # 도착 지점
        reached = (self.player_row == constants.GRID_SIZE - 1 and
                   self.player_col == constants.GRID_SIZE - 1)

        return all_fixed and reached
