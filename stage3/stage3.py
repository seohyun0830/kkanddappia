import pygame
import random

from engine import  constants, sound, maze, assets

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

    def __init__(self, screen, game_state=None):
        self.screen = screen
        self.game_state = game_state

        if self.game_state is None:
            self.game_state={}

        pygame.font.init()

        #드론 애니메이션
        self.drone_active = False
        self.drone_x = 0
        self.drone_y = 0
        self.drone_target_y = 120
        self.last_drone_time = 0
        self.drone_state = "idle"  # idle, entering, dropping, leaving
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
        self.key_states = {k: False for k in [
            pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT
        ]}

        # 압력 시스템
        self.pressure = 50
        self.n = 3
        self.key_pressed = False
        self.low_pressure_start_time = None
        self.last_broken_time = 0

        #아이템 
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
        self.PRESSURE_UPDATE_EVENT = pygame.USEREVENT + 2
        self.SPIKE_UPDATE_EVENT = pygame.USEREVENT + 3

        pygame.time.set_timer(self.PRESSURE_UPDATE_EVENT, constants.PRESSURE_UPDATE_INTERVAL)
        pygame.time.set_timer(
            self.SPIKE_UPDATE_EVENT,
            random.randint(constants.MIN_SPIKE_INTERVAL, constants.MAX_SPIKE_INTERVAL),
            1
        )

        self.fps = pygame.time.Clock()


    def show_timeover(self):
        sound.high_bgm.stop()
        sound.stop_bgm()
        sound.fail_bgm.play()

        img = pygame.image.load("images/stage3/timeover.png")
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

    def show_success(self):
        play_success_animation(self.screen)


    # ---------------------------------------------------
    #                  메인 루프
    # ---------------------------------------------------
    #menu는 게임오버하면 돌아갈 stage (아마 stage2)
    def run(self):
        running = True
    
        draw_screen(self)
        pygame.display.update()
        pygame.time.delay(100)

        if not self.game_state.get("stage3_tutorial_done", False):
            tutorial = Stage3Tutorial(self.screen)
            tutorial.run(self)
            self.game_state["stage3_tutorial_done"] = True

        self.spawn_initial_item()
        #게임 시작 시 기본 단선 3개 생성
        self.spawn_initial_broken(3)
        #튜토리얼 종료-> 타이머 시작
        self.start_time=pygame.time.get_ticks()

        while running:
            self.fps.tick(constants.FPS)

            # 이벤트 처리
            running = self.handle_events()
            if not running:
                pygame.quit()
                quit()

            self.update_logic()
            draw_screen(self)
            pygame.display.update()

            if self.pressure <= 0 or self.hp<=0:
                self.fadeout_with_breath()
                play_oxygen_fail(self.screen)
                return "dead"

            elif self.pressure >= 100:
                from stage3.fail_animation import play_overpressure_fail
                play_overpressure_fail(self.screen)
                return "dead"



            # 시간 초과 체크 -> 이것도 2stage..? 플레이시간....
            now = pygame.time.get_ticks()
            elapsed = now - self.start_time
            if elapsed >= constants.TOTAL_GAME_TIME_SECONDS * 1000:
                self.show_timeover()
                return "dead"

            # 클리어
            if self.check_clear():
                self.show_success()
                return "stage4"

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
            
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                if self.teleport_item_count > 0 and self.broken_tiles:
                    self.selecting_teleport = True

            # 텔레포트 선택 모드 중
            if self.selecting_teleport:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mx, my = e.pos
                    self.handle_teleport_click(mx, my)
                    return True

                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.selecting_teleport = False


        return True

    #게임 로직
    def update_logic(self):
        now = pygame.time.get_ticks()

        # ----------------------------------------
        # 1) 아이템 획득 처리
        # ----------------------------------------
        if (self.player_row, self.player_col) in self.item_positions:
            if self.teleport_item_count < self.max_items:
                self.teleport_item_count += 1
                self.item_positions.remove((self.player_row, self.player_col))
                sound.item_pickup.play()

        # ----------------------------------------
        # 2) 이동 딜레이 처리
        # ----------------------------------------
        self.move_timer += 1
        effective_cd = constants.MOVE_COOLDOWN * (3 if self.pressure <= 40 else 1)

        if self.move_timer >= effective_cd:
            self.handle_movement()
            self.move_timer = 0

        # ----------------------------------------
        # 3) 단선 수리 처리
        # ----------------------------------------
        repaired = self.repair.update(self.maze_data)

        if repaired:
            # 압력 회복 +5
            self.pressure = min(100, self.pressure + 10)

            # 드론 보상 확률 (쿨타임 포함)
            if now - self.last_drone_time >= 7000:   # 7초 쿨타임
                if random.random() < 0.3:            # 수리 보상 확률
                    self.spawn_drone_reward()
                    self.last_drone_time = now

        # ----------------------------------------
        # 4) Q/W 압력 조절
        # ----------------------------------------
        self.pressure, self.key_pressed = user_pressure_control(
            self.pressure, self.key_pressed, self.n
        )

        # ----------------------------------------
        # 5) 고압 → 단선 생성
        # ----------------------------------------
        self.update_broken_tiles()

        # ----------------------------------------
        # 6) HP 감소 체크
        # ----------------------------------------
        self.update_hp()

        # ----------------------------------------
        # 7) BGM 변경
        # ----------------------------------------
        self.update_bgm()

        # ----------------------------------------
        # 8) 철문 생성/해제
        # ----------------------------------------
        self.update_iron_gates()

        # ----------------------------------------
        # 9) 드론 애니메이션 업데이트
        # ----------------------------------------
        if self.drone_active:
            self.update_drone_animation()

        # ----------------------------------------
        # 10) 압력이 매우 높거나 매우 낮을 때 드론 보상
        # ----------------------------------------
        if now - self.last_drone_time >= 7000:  # 쿨타임 7초
            # 고압 보상
            if self.pressure >= 85 and random.random() < 0.15:
                self.spawn_drone_reward()
                self.last_drone_time = now

            # 저압 보상
            if self.pressure <= 25 and random.random() < 0.15:
                self.spawn_drone_reward()
                self.last_drone_time = now




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
                   
        
        """reached = (self.player_row == 0 and
                   self.player_col == 0)#테스트용"""

        return all_fixed and reached
    
    def spawn_initial_item(self):
        # PATH인 장소 중 랜덤 1곳 선택
        candidates = [
            (r, c)
            for r in range(constants.GRID_SIZE)
            for c in range(constants.GRID_SIZE)
            if self.maze_data[r][c] == constants.PATH
        ]

        if not candidates:
            return  # PATH가 없으면 스폰 불가

        r, c = random.choice(candidates)

        self.item_positions.append((r, c))


    def handle_teleport_click(self, mx, my):
        # 마우스 → 타일 좌표 변환
        col = (mx - constants.GRID_OFFSET_X) // constants.TILE_SIZE
        row = (my - constants.GRID_OFFSET_Y) // constants.TILE_SIZE

        # 화면 밖 클릭 방지
        if not (0 <= row < constants.GRID_SIZE and 0 <= col < constants.GRID_SIZE):
            return

        # 해당 위치가 단선인지 확인
        for b in self.broken_tiles:
            if b[0] == row and b[1] == col and b[2]:  # b = [r,c,is_broken]
                # 텔레포트 실행
                self.player_row = row
                self.player_col = col

                self.teleport_item_count -= 1
                self.selecting_teleport = False

                sound.teleport.play()  # 원하면 다른 소리로 변경
                return

    def spawn_drone_reward(self):
        if len(self.item_positions) >= 3:
            return

        sound.drone_drop.play()

        # 드론 시작 위치 (왼쪽 밖 or 오른쪽 밖)
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

        # 1) 등장 단계
        if self.drone_state == "entering":
            if (self.drone_speed > 0 and self.drone_x < self.drone_target_x) or \
            (self.drone_speed < 0 and self.drone_x > self.drone_target_x):
                self.drone_x += self.drone_speed
            else:
                self.drone_state = "dropping"
                self.drop_start_time = pygame.time.get_ticks()
                self.drop_teleport_item()

        # 2) 투하(호버링)
        elif self.drone_state == "dropping":
            if pygame.time.get_ticks() - self.drop_start_time > 500:  # 0.5초 정지
                self.drone_state = "leaving"

        # 3) 떠나기 (위로 빠르게 상승)
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

        # 기존 브금 정지 후 숨소리 재생
        sound.stop_bgm()
        sound.high_bgm.stop()
        sound.breath.play()

        fade = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        fade.fill((0,0,0))

        # 1초 동안 서서히 까매짐
        for i in range(200):
            alpha = min(255, i * 4)   # 0 → 240까지 증가
            fade.set_alpha(alpha)

            # 기존 게임화면 먼저 그림
            from stage3.draw_screen import draw_screen
            draw_screen(self)

            # 드론은 예외처리: 항상 맨 위에 다시 그림
            if self.drone_active:
                self.screen.blit(assets.drone_img, (self.drone_x - 20, self.drone_y - 20))

            self.screen.blit(fade, (0,0))
            pygame.display.update()
            clock.tick(60)
    
    def spawn_initial_broken(self, count=3):
        #게임 시작 직후 미리 단선 타일 여러 개를 생성한다.
        candidates = [
            (r, c)
            for r in range(constants.GRID_SIZE)
            for c in range(constants.GRID_SIZE)
            if self.maze_data[r][c] == constants.PATH
        ]

        random.shuffle(candidates)

        for i in range(min(count, len(candidates))):
            r, c = candidates[i]

            # 단선 타일 등록
            self.broken_tiles.append([r, c, True])
            self.maze_data[r][c] = constants.BROKEN
    