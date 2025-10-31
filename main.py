import pygame,sys,random,math
import constants,assets
from maze import initialize_grid, place_iron_gates, place_broken_tiles
from renderer import draw_maze
from game_state import try_move_player

pygame.init()
pygame.font.init()

#폰트설정 
pressure_font_base = pygame.font.SysFont(constants.FONT_NAME, constants.BASE_FONT_SIZE, bold=True)
timer_font = pygame.font.SysFont(constants.FONT_NAME, constants.TIMER_FONT_SIZE, bold=True)

#압력 미세 변동
PRESSURE_UPDATE_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(PRESSURE_UPDATE_EVENT, constants.PRESSURE_UPDATE_INTERVAL)

#압력 급변
SPIKE_UPDATE_EVENT = pygame.USEREVENT + 3

#급변 타이머 설정
pygame.time.set_timer(SPIKE_UPDATE_EVENT, random.randint(constants.MIN_SPIKE_INTERVAL, constants.MAX_SPIKE_INTERVAL), 1)

SCREEN = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Stage3")

assets.load_pipe_images() #파이프 이미지
assets.load_pressure_images() #압력조절기 이미지

# 배경 이미지
bk_img = pygame.image.load("images/bk.jpg").convert()
bk_img = pygame.transform.scale(bk_img, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

# 플레이어 이미지
player_img = pygame.image.load("images/c1.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (constants.TILE_SIZE, constants.TILE_SIZE))

# 미로 데이터
maze_data = initialize_grid(constants.GRID_SIZE)
iron_gates = place_iron_gates(maze_data, num_gates=8)
broken_tiles = place_broken_tiles(maze_data, num_tiles=6)

# 기본 설정
player_row, player_col = 0, 0
TARGET_ROW, TARGET_COL = constants.GRID_SIZE - 1, constants.GRID_SIZE - 1
move_timer = 0
key_states = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}

fps = pygame.time.Clock()
gate_timer = broken_timer = 0

# 압력 변수 초기화
pressure = 50 # 처음 압력 50
n = 1
key_pressed = False 

start_time = pygame.time.get_ticks() 

#성공
def show_end_screen():
    img1 = pygame.image.load("images/ending_image1.png")
    img2 = pygame.image.load("images/ending_image2.jpg")
    scale = min(constants.SCREEN_WIDTH / img1.get_width(), constants.SCREEN_HEIGHT / img1.get_height())
    s1 = pygame.transform.scale(img1, (int(img1.get_width() * scale), int(img1.get_height() * scale)))
    s2 = pygame.transform.scale(img2, (int(img2.get_width() * scale), int(img2.get_height() * scale)))
    pos = ((constants.SCREEN_WIDTH - s1.get_width()) // 2, (constants.SCREEN_HEIGHT - s1.get_height()) // 2)
    clickable = s1.get_rect(topleft=pos)
    current = s1
    swapped = False
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN and clickable.collidepoint(e.pos) and not swapped:
                current = s2
                swapped = True
            SCREEN.fill((0, 0, 0))
            SCREEN.blit(current, pos)
            pygame.display.update()

#타임오버
def show_end_timeover():
    img=pygame.image.load("images/timeover.png")
    scale = min(constants.SCREEN_WIDTH / img.get_width(), constants.SCREEN_HEIGHT / img.get_height())
    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    pos=img.get_rect(center=(constants.SCREEN_WIDTH//2,constants.SCREEN_HEIGHT//2))

    running=True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False

        SCREEN.fill((0,0,0))
        SCREEN.blit(img,pos)
        pygame.display.update()


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
            print(f"Mouse clicked at: ({x}, {y})")
        
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
            
    #미로
    if move_timer >= constants.MOVE_COOLDOWN:
        if key_states[pygame.K_UP]:
            player_row, player_col = try_move_player(maze_data, (player_row, player_col), -1, 0, iron_gates, broken_tiles)
        elif key_states[pygame.K_DOWN]:
            player_row, player_col = try_move_player(maze_data, (player_row, player_col), 1, 0, iron_gates, broken_tiles)
        elif key_states[pygame.K_LEFT]:
            player_row, player_col = try_move_player(maze_data, (player_row, player_col), 0, -1, iron_gates, broken_tiles)
        elif key_states[pygame.K_RIGHT]:
            player_row, player_col = try_move_player(maze_data, (player_row, player_col), 0, 1, iron_gates, broken_tiles)
        move_timer = 0


    # 배경 출력
    SCREEN.blit(bk_img, (0, 0))

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
    timer_surface = timer_font.render(timer_text_str, True, TIMER_COLOR)
    
    SCREEN.blit(timer_surface, (10, 10)) 

    # 시간이 다 되면 게임 종료
    if remaining_time<=0:
        show_end_timeover()
        play = False


    #미로 출력
    draw_maze(
        SCREEN,
        maze_data,
        constants.GRID_SIZE,
        constants.TILE_SIZE,
        (constants.SCREEN_WIDTH - constants.GRID_SIZE * constants.TILE_SIZE) // 2,
        (constants.SCREEN_HEIGHT - constants.GRID_SIZE * constants.TILE_SIZE) // 2,
        iron_gates,
        broken_tiles,
    )

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

    if pressure <= 40:
        for g in iron_gates:
            if not g[2]: 
                g[2] = True
                maze_data[g[0]][g[1]] = constants.IRON_GATE
    else:
        for g in iron_gates:
            if g[2]:
                g[2] = False
                maze_data[g[0]][g[1]] = constants.PATH
   
    if pressure >= 70:
        for b in broken_tiles:
            if not b[2]: 
                b[2] = True
                maze_data[b[0]][b[1]] = constants.BROKEN
    
    else:
        for b in broken_tiles:
            if b[2]: 
                b[2] = False
                maze_data[b[0]][b[1]] = constants.PATH
    
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

    current_font = pressure_font_base # 기본 폰트 크기로 시작
    TEXT_COLOR = (240, 240, 240) # 기본 색상 (밝은 회색)

    #위급상황: 색상 바뀌면서 글씨크기 커졌다 작아졌다
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
    SCREEN.blit(player_img, (px - constants.TILE_SIZE // 2, py - constants.TILE_SIZE // 2))

    pygame.display.update()

    if player_row == TARGET_ROW and player_col == TARGET_COL and finish_active:
        show_end_screen() #도착지점 도착하고, 활성화되면
        play = False

pygame.quit()
sys.exit()
