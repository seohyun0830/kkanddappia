import pygame,sys
import random

from engine import constants, sound, maze, assets
from engine.difficultyLevel import DIFFICULTY

# Stage3 모듈들
from stage3.movement import try_move_player
from stage3.pressure import update_pressure_small, update_pressure_spike, user_pressure_control
from stage3.repair import RepairSystem
from stage3.broken import generate_broken_tile
from stage3.draw_screen import draw_screen
from stage3.tutorial import Stage3Tutorial
from stage3.fail_animation import play_oxygen_fail
from stage3.success_animation import play_success_animation


class Stage3:

    # 일단 easy로설정
    def apply_difficulty(self, mode="HARD"):
        cfg = DIFFICULTY.get(mode, DIFFICULTY["HARD"])

        # 압력 랜덤
        self.MIN_RANDOM_CHANGE = cfg["MIN_RANDOM_CHANGE"]
        self.MAX_RANDOM_CHANGE = cfg["MAX_RANDOM_CHANGE"]
        self.PRESSURE_UPDATE_INTERVAL = cfg["PRESSURE_UPDATE_INTERVAL"]
        # 스파이크
        self.MIN_SPIKE_INTERVAL = cfg["MIN_SPIKE_INTERVAL"]
        self.MAX_SPIKE_INTERVAL = cfg["MAX_SPIKE_INTERVAL"]
        self.MIN_SPIKE_CHANGE = cfg["MIN_SPIKE_CHANGE"]
        self.MAX_SPIKE_CHANGE = cfg["MAX_SPIKE_CHANGE"]
        # 단선 확률
        self.BROKEN_LOW_CHANCE = cfg["BROKEN_LOW_CHANCE"]
        self.BROKEN_MID_CHANCE = cfg["BROKEN_MID_CHANCE"]
        self.BROKEN_HIGH_CHANCE = cfg["BROKEN_HIGH_CHANCE"]
        # HP
        self.HP_DAMAGE = cfg["HP_DAMAGE"]
        self.HP_DAMAGE_INTERVAL = cfg["HP_DAMAGE_INTERVAL"]
        # 초기 단선
        self.BEGIN_BROKEN_CNT = cfg["BEGIN_BROKEN_CNT"]
        # 드론확률
        self.DRONE_CHANCE = cfg["DRONE_CHANCE"]
        # 압력 조절
        self.PRESSURE_CONTROL_AMOUNT = cfg["PRESSURE_CONTROL_AMOUNT"]

    def __init__(self, screen, mode="hard", game_state=None):
        self.screen = screen
        self.game_state = game_state or {}

        if self.game_state is None:
            self.game_state = {}

        pygame.font.init()

        self.apply_difficulty(mode.upper()) #문자 다 대문자로바꺼주기

        # 드론 애니메이션
        self.drone_active = False
        self.drone_x = 0
        self.drone_y = 0
        self.drone_target_y = 120
        self.last_drone_time = 0
        self.drone_state = "idle"  
        self.drone_speed = 6

        # 미로 데이터
        self.maze_data = maze.initialize_grid(constants.GRID_SIZE)
        self.iron_gates = []
        self.broken_tiles = []

        # 플레이어 위치
        self.player_row = 0
        self.player_col = 0

        # 이동 변속 관련
        self.move_timer = 0
        self.key_states = {
            k: False for k in [
                pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT
            ]
        }

        # 압력 시스템
        self.pressure = 50
        self.n = self.PRESSURE_CONTROL_AMOUNT
        self.key_pressed = False
        self.low_pressure_start_time = None
        self.last_broken_time = 0

        # 아이템
        self.item_positions = []      # 미로에 있는 아이템 좌표 리스트
        self.max_items = 2            # 플레이어 최대 보유 아이템 개수
        self.teleport_item_count = 0  # 현재 플레이어가 가진 아이템 개수
        self.selecting_teleport = False

        # HP
        self.hp = constants.MAX_HP

        # 수리 시스템
        self.repair = RepairSystem()

        # BGM
        self.current_bgm_state = "normal"
        self.high_playing = False
        sound.play_bgm(sound.normal_bgm)

        # 이벤트 타이머 설정
        self.PRESSURE_UPDATE_EVENT = pygame.USEREVENT + 2  # 미세변동
        self.SPIKE_UPDATE_EVENT = pygame.USEREVENT + 3     # 스파이크

        pygame.time.set_timer(self.PRESSURE_UPDATE_EVENT, self.PRESSURE_UPDATE_INTERVAL)
        pygame.time.set_timer(
            self.SPIKE_UPDATE_EVENT,
            random.randint(self.MIN_SPIKE_INTERVAL, self.MAX_SPIKE_INTERVAL),
            1
        )

        self.fps = pygame.time.Clock()

    def show_timeover(self):
        sound.high_bgm.stop()
        sound.stop_bgm()
        sound.fail_bgm.play()

        img = pygame.image.load("images/stage3/timeover.png")
        scale = min(
            constants.SCREEN_WIDTH / img.get_width(),
            constants.SCREEN_HEIGHT / img.get_height()
        )
        img = pygame.transform.scale(
            img,
            (int(img.get_width() * scale), int(img.get_height() * scale))
        )
        rect = img.get_rect(
            center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2)
        )

        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return

            self.screen.fill((0, 0, 0))
            self.screen.blit(img, rect)
            pygame.display.update()

    def show_success(self):
        play_success_animation(self.screen)

    # ---------------------------------------------------
    # 메인 루프
    # ---------------------------------------------------
    def run(self):
        running = True

        draw_screen(self)
        pygame.display.update()
        pygame.time.delay(200)

        if not self.game_state.get("stage3_tutorial_done", False):
            tutorial = Stage3Tutorial(self.screen)
            result = tutorial.run(self)

            if result == "quit":
                return

            self.game_state["stage3_tutorial_done"] = True

        self.spawn_initial_item()
        self.spawn_initial_broken()

        self.start_time = pygame.time.get_ticks()

        while running:
            self.fps.tick(constants.FPS)

            # 이벤트 처리
            running = self.handle_events()
            if not running:
                return "quit"

            self.update_logic()
            draw_screen(self)
            pygame.display.update()

            if self.pressure <= 0 or self.hp <= 0:
                self.fadeout_with_breath()
                play_oxygen_fail(self.screen)
                self.stop_all_sounds()
                return "dead"

            elif self.pressure >= 100:
                from stage3.fail_animation import play_overpressure_fail
                play_overpressure_fail(self.screen)
                self.stop_all_sounds()
                return "dead"

            now = pygame.time.get_ticks()
            elapsed = now - self.start_time
            if elapsed >= constants.TOTAL_GAME_TIME_SECONDS * 1000:
                self.show_timeover()
                return "dead"

            if self.check_clear():
                self.stop_all_sounds()
                self.show_success()
                return "stage4"

    # ---------------------------------------------------
    # 이벤트 처리
    # ---------------------------------------------------
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

            # 압력 변화 이벤트
            if e.type == self.PRESSURE_UPDATE_EVENT:
                self.pressure = update_pressure_small(self.pressure, self)

            if e.type == self.SPIKE_UPDATE_EVENT:
                self.pressure = update_pressure_spike(self.pressure, self)

                pygame.time.set_timer(
                    self.SPIKE_UPDATE_EVENT,
                    random.randint(self.MIN_SPIKE_INTERVAL, self.MAX_SPIKE_INTERVAL),
                    1
                )

            # 텔레포트
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                if self.teleport_item_count > 0 and self.broken_tiles:
                    self.selecting_teleport = True

            if self.selecting_teleport:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mx, my = e.pos
                    self.handle_teleport_click(mx, my)
                    return True

                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.selecting_teleport = False

        return True

    # ---------------------------------------------------
    # 게임 로직
    # ---------------------------------------------------
    def update_logic(self):
        now = pygame.time.get_ticks()

        # 1) 아이템 획득
        if (self.player_row, self.player_col) in self.item_positions:
            if self.teleport_item_count < self.max_items:
                self.teleport_item_count += 1
                self.item_positions.remove((self.player_row, self.player_col))
                sound.item_pickup.play()

        # 2) 이동
        self.move_timer += 1
        effective_cd = self.get_move_cooldown()
        if self.move_timer >= effective_cd:
            self.handle_movement()
            self.move_timer = 0

        # 3) 단선 수리 처리
        repaired = self.repair.update(self.maze_data)

        if repaired:
            self.pressure = min(100, self.pressure + 10)

            if now - self.last_drone_time >= 7000:
                if random.random() < self.DRONE_CHANCE:
                    self.spawn_drone_reward()
                    self.last_drone_time = now

        # 4) 압력 조절
        self.pressure, self.key_pressed = user_pressure_control(
            self.pressure, self.key_pressed, self
        )

        # 5) 고압 → 단선 생성
        self.update_broken_tiles()

        # 6) HP 감소
        self.update_hp()

        # 7) BGM
        self.update_bgm()

        # 8) 철문
        self.update_iron_gates()

        # 9) 드론
        if self.drone_active:
            self.update_drone_animation()

        # 10) 드론 보상 (압력 극단 상황)
        if now - self.last_drone_time >= 7000:

            if self.pressure >= 85 and random.random() < self.DRONE_CHANCE:
                self.spawn_drone_reward()
                self.last_drone_time = now

            if self.pressure <= 15 and random.random() < self.DRONE_CHANCE:
                self.spawn_drone_reward()
                self.last_drone_time = now

    
    def update_iron_gates(self):
        if self.pressure <= 40:
            if any(g[2] for g in self.iron_gates):
                return

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
                self.iron_gates.append([r, c, True, -constants.TILE_SIZE])
                self.maze_data[r][c] = constants.IRON_GATE

        else:
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
                broken_chance = self.BROKEN_LOW_CHANCE
            elif self.pressure < 90:
                broken_chance = self.BROKEN_MID_CHANCE
            else:
                broken_chance = self.BROKEN_HIGH_CHANCE

            if random.random() < broken_chance:
                generate_broken_tile(self.maze_data, self.broken_tiles)
                self.pressure = max(0, self.pressure - 10)
                self.last_broken_time = now

    def update_hp(self):
        if self.pressure <= 40 or self.pressure >= 70:
            if self.low_pressure_start_time is None:
                self.low_pressure_start_time = pygame.time.get_ticks()
            else:
                if pygame.time.get_ticks() - self.low_pressure_start_time >= self.HP_DAMAGE_INTERVAL:
                    self.hp = max(0, self.hp - self.HP_DAMAGE)
                    self.low_pressure_start_time = pygame.time.get_ticks()
        else:
            self.low_pressure_start_time = None

    def update_bgm(self):

        if self.pressure <= 40:
            if self.current_bgm_state != "low":
                sound.stop_bgm()
                sound.play_bgm(sound.low_bgm)
                self.current_bgm_state = "low"

        elif self.pressure >= 70:
            if not self.high_playing:
                sound.high_bgm.play(-1)
                self.high_playing = True

        else:
            if self.high_playing:
                sound.high_bgm.stop()
                self.high_playing = False

            if self.current_bgm_state != "normal":
                sound.stop_bgm()
                sound.play_bgm(sound.normal_bgm)
                self.current_bgm_state = "normal"

    def check_clear(self):
        all_fixed = all(not b[2] for b in self.broken_tiles)

        reached = (
            self.player_row == constants.GRID_SIZE - 1
            and self.player_col == constants.GRID_SIZE - 1
        )
        """
        reached = (
                    self.player_row == 0
                    and self.player_col == 0
                )"""

        return all_fixed and reached

    def spawn_initial_item(self):
        candidates = [
            (r, c)
            for r in range(constants.GRID_SIZE)
            for c in range(constants.GRID_SIZE)
            if self.maze_data[r][c] == constants.PATH
        ]

        if not candidates:
            return

        r, c = random.choice(candidates)
        self.item_positions.append((r, c))

    def handle_teleport_click(self, mx, my):
        col = (mx - constants.GRID_OFFSET_X) // constants.TILE_SIZE
        row = (my - constants.GRID_OFFSET_Y) // constants.TILE_SIZE

        if not (0 <= row < constants.GRID_SIZE and 0 <= col < constants.GRID_SIZE):
            return

        for b in self.broken_tiles:
            if b[0] == row and b[1] == col and b[2]:
                self.player_row = row
                self.player_col = col

                self.teleport_item_count -= 1
                self.selecting_teleport = False

                sound.teleport.play()
                return

    def spawn_drone_reward(self):
        if len(self.item_positions) >= 3:
            return

        sound.drone_drop.play()

        side = random.choice(["left", "right"])
        if side == "left":
            self.drone_x = -60
            self.drone_speed = abs(self.drone_speed)
        else:
            self.drone_x = constants.SCREEN_WIDTH + 60
            self.drone_speed = -abs(self.drone_speed)

        self.drone_y = random.randint(80, 140)
        self.drone_target_x = random.randint(200, constants.SCREEN_WIDTH - 200)

        self.drone_state = "entering"
        self.drone_active = True

        self.last_drone_time = pygame.time.get_ticks()

    def update_drone_animation(self):
        if not self.drone_active:
            return

        if self.drone_state == "entering":
            if (
                (self.drone_speed > 0 and self.drone_x < self.drone_target_x)
                or (self.drone_speed < 0 and self.drone_x > self.drone_target_x)
            ):
                self.drone_x += self.drone_speed
            else:
                self.drone_state = "dropping"
                self.drop_start_time = pygame.time.get_ticks()
                self.drop_teleport_item()

        elif self.drone_state == "dropping":
            if pygame.time.get_ticks() - self.drop_start_time > 500:
                self.drone_state = "leaving"

        elif self.drone_state == "leaving":
            self.drone_y -= 10
            if self.drone_y < -50:
                self.drone_active = False
                self.drone_state = "idle"

    def drop_teleport_item(self):
        candidates = [
            (r, c)
            for r in range(constants.GRID_SIZE)
            for c in range(constants.GRID_SIZE)
            if self.maze_data[r][c] == constants.PATH
        ]

        if not candidates:
            return

        drop_pos = random.choice(candidates)
        self.item_positions.append(drop_pos)

    def fadeout_with_breath(self):
        clock = pygame.time.Clock()

        sound.stop_bgm()
        sound.high_bgm.stop()
        sound.breath.play()

        fade = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        fade.fill((0, 0, 0))

        for i in range(60):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            alpha = min(255, i * 5)
            fade.set_alpha(alpha)

            from stage3.draw_screen import draw_screen
            draw_screen(self)

            if self.drone_active:
                self.screen.blit(assets.drone_img, (self.drone_x - 20, self.drone_y - 20))

            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            clock.tick(40)

    def spawn_initial_broken(self):
        count = self.BEGIN_BROKEN_CNT
        candidates = [
            (r, c)
            for r in range(constants.GRID_SIZE)
            for c in range(constants.GRID_SIZE)
            if self.maze_data[r][c] == constants.PATH
        ]

        random.shuffle(candidates)

        for i in range(min(count, len(candidates))):
            r, c = candidates[i]
            self.broken_tiles.append([r, c, True])
            self.maze_data[r][c] = constants.BROKEN

    def get_move_cooldown(self):
        p = self.pressure

        if p <= 40:
            return 9
        elif p <= 70:
            return int(3 + (70 - p) * 0.08)
        return int(3 - (p - 70) * 0.02)


    def stop_all_sounds(self):
        try: sound.stop_bgm()
        except: pass

        try: sound.high_bgm.stop()
        except: pass

        try: sound.fire_loop.stop()
        except: pass

        try: sound.beep_error.stop()
        except: pass

        try: sound.oxfail_bgm.stop()
        except: pass

        try: sound.explosion.stop()
        except: pass

        try: sound.breath.stop()
        except: pass

        try: sound.fail_bgm.stop()
        except: pass
