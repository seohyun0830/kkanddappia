import pygame,sys,random,math
pygame.init()
pygame.font.init()
import constants,assets,maze,renderer,game_state

SCREEN = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("stage3")

#압력 미세 변동
PRESSURE_UPDATE_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(PRESSURE_UPDATE_EVENT, constants.PRESSURE_UPDATE_INTERVAL)

#압력 급변
SPIKE_UPDATE_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(SPIKE_UPDATE_EVENT, random.randint(constants.MIN_SPIKE_INTERVAL, constants.MAX_SPIKE_INTERVAL), 1)

assets.load_pipe_images() #파이프 이미지
assets.load_pressure_images() #압력조절기 이미지

# 미로 데이터
maze_data = maze.initialize_grid(constants.GRID_SIZE)
iron_gates = []
broken_tiles = []

# 기본 설정
player_row, player_col = 0, 0
hp=constants.MAX_HP
HP_DECAY_RATE=0.03
TARGET_ROW, TARGET_COL = constants.GRID_SIZE - 1, constants.GRID_SIZE - 1
move_timer = 0
key_states = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}

fps = pygame.time.Clock()
gate_timer = broken_timer = 0

# 압력 변수 초기화
pressure = 50 # 처음 압력 50
n = 3 #q,w키로 몇씩 높아지고 낮아지는지
key_pressed = False 

start_time = pygame.time.get_ticks() 

repairing = False
repair_start_time = 0
repair_target = None

last_broken_time=0


play = True
while play:
    fps.tick(40)
    move_timer += 1

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            play = False
        elif e.type == pygame.KEYDOWN and e.key in key_states:
            key_states[e.key] = True
        elif e.type == pygame.KEYUP and e.key in key_states:
            key_states[e.key] = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            x, y = e.pos
            print(f"Mouse clicked at: ({x}, {y})") ############이거는 필요할까봐 해주는거임 게임에는 필요없음##############
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_e:
            for b in broken_tiles:
                if b[0] == player_row and b[1] == player_col and b[2]:
                    repairing = True
                    repair_start_time = pygame.time.get_ticks()
                    repair_target = b
                    break
        elif e.type == pygame.KEYUP and e.key == pygame.K_e:
            repairing = False
            repair_target = None
        
        # 미세 변동 0.2초마다
        elif e.type == PRESSURE_UPDATE_EVENT:
            random_change = random.uniform(constants.MIN_RANDOM_CHANGE, constants.MAX_RANDOM_CHANGE)
            
            if random.choice([True, False]):
                pressure += random_change
            else: # False면 감소
                pressure -= random_change
            
            pressure = max(0.0, min(100.0, pressure))
        
        # 압력 급변 (8~12초마다)
        elif e.type == SPIKE_UPDATE_EVENT:
            spike_change = random.uniform(constants.MIN_SPIKE_CHANGE, constants.MAX_SPIKE_CHANGE)
            
            if random.choice([True, False]):
                pressure += spike_change
            else:
                pressure -= spike_change

            pressure = max(0.0, min(100.0, pressure))
            
            # 다음 급변 타이머 재설정 (무작위 간격)
            next_spike_time = random.randint(constants.MIN_SPIKE_INTERVAL, constants.MAX_SPIKE_INTERVAL)
            pygame.time.set_timer(SPIKE_UPDATE_EVENT, next_spike_time, 1) 
            
    effective_move_cooldown = constants.MOVE_COOLDOWN * (2 if pressure <= 40 else 1)

    #미로
    if move_timer >= effective_move_cooldown:
        if key_states[pygame.K_UP]:
            player_row, player_col = game_state.try_move_player(maze_data, (player_row, player_col), -1, 0, iron_gates, broken_tiles)
        elif key_states[pygame.K_DOWN]:
            player_row, player_col = game_state.try_move_player(maze_data, (player_row, player_col), 1, 0, iron_gates, broken_tiles)
        elif key_states[pygame.K_LEFT]:
            player_row, player_col = game_state.try_move_player(maze_data, (player_row, player_col), 0, -1, iron_gates, broken_tiles)
        elif key_states[pygame.K_RIGHT]:
            player_row, player_col = game_state.try_move_player(maze_data, (player_row, player_col), 0, 1, iron_gates, broken_tiles)
        move_timer = 0

    if pressure <= 40:
        # 철문 생성 (이미 닫힌 문 없을 때만 새로 배치)
        if not any(g[2] for g in iron_gates):
            num_new_gates = random.randint(5, 15)
            candidates = []
            for r in range(constants.GRID_SIZE):
                for c in range(constants.GRID_SIZE):
                    if maze_data[r][c] == constants.PATH:
                        candidates.append((r, c))
            random.shuffle(candidates)
            selected = candidates[:num_new_gates]

            iron_gates.clear()
            for (r, c) in selected:
                iron_gates.append([r, c, True])
                maze_data[r][c] = constants.IRON_GATE

        # 저압 유지 타이머
        #특정시간 유지시 HP감소
        if low_pressure_start_time is None:
            low_pressure_start_time = pygame.time.get_ticks()
        else:
            elapsed_low = pygame.time.get_ticks() - low_pressure_start_time
            if elapsed_low >= 3000:  # 3초 유지 시
                hp = max(0, hp - 5)
                low_pressure_start_time = pygame.time.get_ticks()  # 다시 카운트
    else:
        # 회복: 철문 해제 + 타이머 리셋
        low_pressure_start_time = None
        for g in iron_gates:
            if g[2]:
                maze_data[g[0]][g[1]] = constants.PATH
        iron_gates.clear()


    # 배경 출력
    SCREEN.blit(assets.bk_img, (0, 0))

    #타이머 계산,출력
    elapsed_time = pygame.time.get_ticks() - start_time
    #남은시간 계산
    remaining_time = max(0, constants.TOTAL_GAME_TIME_SECONDS * 1000 - elapsed_time)
    
    total_seconds = remaining_time // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    
    # 시간 형식 (MM:SS)
    timer_text_str = f"{minutes:02}:{seconds:02}" 
    
    TIMER_COLOR = (200,200,200) 
    timer_surface = assets.timer_font.render(timer_text_str, True, TIMER_COLOR)
    
    SCREEN.blit(timer_surface, (10, 10)) 

    # 시간이 다 되면 게임 종료
    if remaining_time<=0:
        game_state.show_end_timeover(SCREEN)
        play = False


    #미로 출력
    renderer.draw_maze(
        SCREEN,
        maze_data,
        constants.GRID_SIZE,
        constants.TILE_SIZE,
        (constants.SCREEN_WIDTH - constants.GRID_SIZE * constants.TILE_SIZE) // 2,
        (constants.SCREEN_HEIGHT - constants.GRID_SIZE * constants.TILE_SIZE) // 2,
        iron_gates,
        broken_tiles,
    )

    for b in broken_tiles:
        if b[2]:  # 아직 고장 상태
            r, c = b[0], b[1]

            maze_offset_x = (constants.SCREEN_WIDTH - constants.GRID_SIZE * constants.TILE_SIZE) // 2
            maze_offset_y = (constants.SCREEN_HEIGHT - constants.GRID_SIZE * constants.TILE_SIZE) // 2
            center_x = maze_offset_x + c * constants.TILE_SIZE + constants.TILE_SIZE // 2
            center_y = maze_offset_y + r * constants.TILE_SIZE + constants.TILE_SIZE // 2

            tile_size = constants.TILE_SIZE

            glow_radius = int(tile_size * 1.2)
            glow_diameter = glow_radius * 2

            glow = pygame.Surface((glow_diameter, glow_diameter), pygame.SRCALPHA)

            # 깜빡이는 느낌 (조명 숨쉬기)
            alpha = 70 + int(50 * math.sin(pygame.time.get_ticks() * 0.005))

            pygame.draw.circle(glow, (255, 120, 0, alpha), (glow_radius, glow_radius), glow_radius)
            SCREEN.blit(glow, (center_x - glow_radius, center_y - glow_radius))

    if repairing and repair_target:
        now = pygame.time.get_ticks()
        elapsed = now - repair_start_time

        if elapsed >= 2000:  #2초 이상 유지하면 수리 완료
            repair_target[2] = False
            maze_data[repair_target[0]][repair_target[1]] = constants.PATH
            repairing = False
            repair_target = None

        else:
            progress = elapsed / 2000
            bar_width = 40
            bar_height = 6
            px = (constants.SCREEN_WIDTH - constants.GRID_SIZE * constants.TILE_SIZE) // 2 + player_col * constants.TILE_SIZE + constants.TILE_SIZE // 2
            py = (constants.SCREEN_HEIGHT - constants.GRID_SIZE * constants.TILE_SIZE) // 2 + player_row * constants.TILE_SIZE - 10
            pygame.draw.rect(SCREEN, (50, 50, 50), (px - bar_width//2, py, bar_width, bar_height))
            pygame.draw.rect(SCREEN, (0, 255, 0), (px - bar_width//2, py, int(bar_width * progress), bar_height))

    #압력 조절기
    regulator_x = 10
    regulator_y = constants.SCREEN_HEIGHT - 200
    scaled_regulator = pygame.transform.scale(assets.pressure_regulator_img, (200, 200))
    SCREEN.blit(scaled_regulator, (regulator_x, regulator_y))

    #압력계 바늘
    needle_scaled = pygame.transform.scale(assets.needle_img, (30, 30)) #바늘 크기 조절

    keys = pygame.key.get_pressed()

    # Q,W키로 압력 조절
    if not key_pressed:
        if keys[pygame.K_q]:
            pressure = min(100.0, pressure + n) #100안넘도록
            key_pressed = True
        elif keys[pygame.K_w]:
            pressure = max(0.0, pressure - n) #0미만 안되도록
            key_pressed = True
    else: 
        if not (keys[pygame.K_q] or keys[pygame.K_w]):
            key_pressed = False
   
    #---hp가 0이면 게임오버
    if hp<=0: #gameover
        play=False


        # ---------------- 단선 확률적 생성 ----------------
    current_time = pygame.time.get_ticks()
    if pressure >= 70 and current_time - last_broken_time >= 3000:
        # 압력 구간에 따라 확률 결정
        if pressure < 80:
            broken_chance = 0.01  
        elif pressure < 90:
            broken_chance = 0.02   
        else:
            broken_chance = 0.03   

        # 확률 기반으로 단선 발생 (매 프레임마다 검사)
        if random.random() < broken_chance:  # 0.0~1.0 사이 난수
            # 단선 후보 위치 선택
            candidates = []
            for r in range(constants.GRID_SIZE):
                for c in range(constants.GRID_SIZE):
                    if maze_data[r][c] == constants.PATH:
                        already_broken = any(b[0] == r and b[1] == c and b[2] for b in broken_tiles)
                        if not already_broken:
                            candidates.append((r, c))
            if candidates:
                r, c = random.choice(candidates)
                broken_tiles.append([r, c, True])
                maze_data[r][c] = constants.BROKEN
                pressure = max(0.0, pressure - 5)  # 단선 발생 시 압력 하락
                last_broken_time = current_time
            

    finish_active = all(not b[2] for b in broken_tiles)

    # 중심 좌표
    center_x, center_y = 111, 700

    # 회전 각도 계산
    rotation_angle = (pressure / 100.0) * 270 - 90
    angle_to_rotate = -rotation_angle # 파이게임에서 회전은 반시계 방향이 양수

    original_rect = needle_scaled.get_rect(center=(center_x, center_y))
    rotated_needle = pygame.transform.rotate(needle_scaled, angle_to_rotate)
    rotated_rect = rotated_needle.get_rect(center=original_rect.center)
    SCREEN.blit(rotated_needle, rotated_rect)

    pressure_text_str = f"{int(pressure)}psi"

    current_font = assets.pressure_font_base # 기본 폰트 크기로 시작
    TEXT_COLOR = (240, 240, 240) # 기본 색상 (밝은 회색)

    #---위급상황: 색상 바뀌면서 글씨크기 커졌다 작아졌다---
    if pressure > 70:# 70이상이면 빨간색으로 표시 
        TEXT_COLOR = (255, 50, 50) 
        current_time = pygame.time.get_ticks()
        pulsation_offset = (math.sin(current_time * constants.PULSATE_SPEED) + 1.0) * (constants.PULSATE_MAX_OFFSET / 2.0)
        current_font_size = constants.BASE_FONT_SIZE + pulsation_offset
        current_font = pygame.font.SysFont(constants.FONT_NAME, int(current_font_size), bold=True)

    if pressure<40: # 40미만이면 핑크색으로 표시
        TEXT_COLOR=(200,50,255)
        current_time = pygame.time.get_ticks()
        pulsation_offset = (math.sin(current_time * constants.PULSATE_SPEED) + 1.0) * (constants.PULSATE_MAX_OFFSET / 2.0)
        current_font_size = constants.BASE_FONT_SIZE + pulsation_offset
        current_font = pygame.font.SysFont(constants.FONT_NAME, int(current_font_size), bold=True)
        
    pressure_surface = current_font.render(pressure_text_str, True, TEXT_COLOR)

    text_x = center_x 
    text_y = center_y - 100 

    pressure_rect = pressure_surface.get_rect(center=(text_x, text_y))

    SCREEN.blit(pressure_surface, pressure_rect)

    # 플레이어 위치 계산
    fx = (constants.SCREEN_WIDTH - constants.GRID_SIZE * constants.TILE_SIZE) // 2 + TARGET_COL * constants.TILE_SIZE + constants.TILE_SIZE // 2
    fy = (constants.SCREEN_HEIGHT - constants.GRID_SIZE * constants.TILE_SIZE) // 2 + TARGET_ROW * constants.TILE_SIZE + constants.TILE_SIZE // 2
    px = (constants.SCREEN_WIDTH - constants.GRID_SIZE * constants.TILE_SIZE) // 2 + player_col * constants.TILE_SIZE + constants.TILE_SIZE // 2
    py = (constants.SCREEN_HEIGHT - constants.GRID_SIZE * constants.TILE_SIZE) // 2 + player_row * constants.TILE_SIZE + constants.TILE_SIZE // 2

    #도착지점(활성화->초록색,비활성화->빨간색)
    pygame.draw.circle(SCREEN, (0, 255, 0) if finish_active else (255, 0, 0), (fx, fy), 8)
    #플레이어 이미지 표시
    SCREEN.blit(assets.player_img, (px - constants.TILE_SIZE // 2, py - constants.TILE_SIZE // 2))

    assets.draw_hp_bar(SCREEN,hp)

    #---------압력 높고 낮음 경고 애니메이션-----------------------------------------------------
    if pressure <= 40:
    # 플레이어 화면상 좌표 계산
        maze_w = constants.GRID_SIZE * constants.TILE_SIZE
        maze_h = constants.GRID_SIZE * constants.TILE_SIZE
        maze_x = (constants.SCREEN_WIDTH - maze_w) // 2
        maze_y = (constants.SCREEN_HEIGHT - maze_h) // 2

        max_black=200
        min_black=250
        sight_black=int(min_black+(max_black-min_black)*(pressure/40))

    # 전체 검은 화면 만들기 (알파 가능)
        darkness_mask = pygame.Surface((maze_w, maze_h), pygame.SRCALPHA)
        darkness_mask.fill((0, 0, 0, sight_black))

        local_px=px-maze_x
        local_py=py-maze_y

    # 원형 구멍 뚫기 (중심 = 플레이어)
        pygame.draw.circle(
            darkness_mask,
            (0, 0, 0, 0),  # 완전 투명
            (local_px, local_py),
            60
        )

    # 화면에 마스크 적용w
        SCREEN.blit(darkness_mask, (maze_x,maze_y))

    # 압력 0이면 완전 암흑 + 게임오버 처리 그대로 유지
        if pressure <= 0:
            full_dark = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            full_dark.set_alpha(255)
            full_dark.fill((0, 0, 0))
            SCREEN.blit(full_dark, (0, 0))

            gameover_img = pygame.image.load('images/gameover.png')
            gameover_img = pygame.transform.scale(gameover_img, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            SCREEN.blit(gameover_img, (0, 0))

            pygame.display.update()
            play = False

            

    elif pressure >= 70:
        # 70~100 구간 → 0~180 사이의 알파값 (높을수록 더 빨개짐)
        redness = int(180 * ((pressure - 70) / 30.0))
        redness = min(180, max(50, redness))  # 최소 50~최대 180 제한q
        
        overlay_red = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        overlay_red.set_alpha(redness)
        overlay_red.fill((255, 0, 0))  # 붉은빛 오버레이
        SCREEN.blit(overlay_red, (0, 0))

        if pressure >=100:
            gameover_img=pygame.image.load('images/gameover.png')
            gameover_img = pygame.transform.scale(gameover_img, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            SCREEN.blit(gameover_img,(0,0))
            pygame.display.update()
            play=False
    #-----------------------------------------------------------------------------
    

    pygame.display.update()

    if player_row == TARGET_ROW and player_col == TARGET_COL and finish_active:
        game_state.show_end_screen(SCREEN) #도착지점 도착하고, 활성화되면
        play = False

pygame.quit()
sys.exit()


'''
<지금당장생각>
- 어떻게 해야 재미있을까??******************


미로에 단선이 압력 70을 넘을때마다 몇개씩 생김
단선을 복구해야함 한번생긴 단선은 저절로 없어지지 않음
근데 단선을 복구할 떄 마다 매번 미션이 있음 (리듬게임같은거?)
단선이 많을수록 압력이 빨리 낮아짐
압력이 40이하면 철문으로인해 길이 막힘
압력이 (70~80)(80~90)(90~99 )이렇게해서 단선이 생기는갸수가 점점많아짐
압력이 100이되면 폭발해서 실패
단선을 다 복구해야 도착지점 활성화
그리고 안정범위 벗어나면 플레이어 속도 느려지도록?

-->시간압박심하게

교수님이 ㅈㄴ노잼같다고하심



압력을 체력처럼?
압력이 너무 높거나 낮으면 산소부족?, 폭발위험 에니매이션 발생
그런 채로 일정시간 유지하면 HP깎임
HP 0이되면 실패화면으로 연결

압력이 너무 낮으면 0~30 이동속도 감소, 화면 어두워짐 ,산소부족 경고음,화면흔들림?
압력 안정 30~~70 정상속도,기계소음 약하게
압력 70~90 철문 닫힘, 단선 증가,경고음,화면붉은빛
압력 90~100 위험단계 화염발생,데미지 감소 사이렌,경고음



압력계가 ㅈㄴ굳이 필요한가라고 하셧음
--> 그냥 단순히 키보드로 수치가 오르내리면서 이게 단선 생성 ,문여닫기로 연결되면
겉보기엔 그냥 장애물 하나 설치한 미로게임처럼 보여서 단조로워보임

압력계는 단순 장식이 아닌, 플레이어가 전략적으로 조절해야 하는 위험관리 장치임

압력계를 이용한 플레이가 재밌으려면??

q,w를 리스크있는 능력으로 만들기??
정답이 없는 선택 어느쪽을 선택해도 문제생김 예를들어 압력 올리면 문은 열리는데 바로 단선생김 
낮추면 안정화,그러나 문닫힘





- 4->3 비상수리 연료없을때






<여유 있을 때>
- 3->4 넘어갈떄 애니메이션 실감나게
- 실패 화면 실감나게
- 게임 시퀀스 (경고음,대사/로그 기반 스토리)
- 게임퀄리티
    압력이 너무 낮으면??
    화면이 어두워지고, 움직임이 느려짐?
    너무높으면??
    미로에 불꽃 일어나고 데미지 받음 HP를 추가할까??
    중간-> 속도 빠르고 화면 안정



'''