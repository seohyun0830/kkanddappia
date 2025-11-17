import pygame,sys,random
pygame.font.init()
import constants,maze,renderer,game_state,assets

pygame.init()

SCREEN = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("stage4to3")
fps=pygame.time.Clock()
assets.load_pipe_images()
assets.load_fuel_gage_images()

back_maze_data = maze.initialize_grid(constants.GRID_SIZE)

player_row,player_col=0,0

#---연료---
fuel_level=0 #현재연료량 일단은 0으로 설정
NUM_FUELS=random.randint(20,30)
FUEL_PER_ITEM=10

candidates=[
    (r,c)
    for r in range(constants.GRID_SIZE)
    for c in range(constants.GRID_SIZE)
    if back_maze_data[r][c] == constants.PATH and not (r == 0 and c == 0)
]
random.shuffle(candidates)
fuel_positions = candidates[:NUM_FUELS]
collected_fuels = []
#-------------------------------------

#---이동---
key_states = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
move_timer = 0

#---back to 4stage button---
button_width, button_height = 160,160
back_button_img = pygame.transform.scale(assets.back_button_img, (button_width, button_height))
button_x = constants.SCREEN_WIDTH - button_width - 20
button_y = 20
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

fuel_obtainde=False
play=True

while play:
    fps.tick(40)
    move_timer+=1

    mouse_pos = pygame.mouse.get_pos()
    mouse_down = pygame.mouse.get_pressed()[0]  
    is_hover = button_rect.collidepoint(mouse_pos) 

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

    if move_timer >= constants.back_MOVE_COOLDOWN:
        if key_states[pygame.K_UP]:
            player_row, player_col = game_state.try_move_player(back_maze_data, (player_row, player_col), -1, 0,[],[])
        elif key_states[pygame.K_DOWN]:
            player_row, player_col = game_state.try_move_player(back_maze_data, (player_row, player_col), 1, 0,[],[])
        elif key_states[pygame.K_LEFT]:
            player_row, player_col = game_state.try_move_player(back_maze_data, (player_row, player_col), 0, -1,[],[])
        elif key_states[pygame.K_RIGHT]:
            player_row, player_col = game_state.try_move_player(back_maze_data, (player_row, player_col), 0, 1,[],[])
        move_timer = 0

        #-----------------이부분 3번쓰이니깐 걍함수로만들기

    SCREEN.blit(assets.bk_img, (0, 0))

    #미로 출력
    renderer.draw_maze(
        SCREEN,
        back_maze_data,
        constants.GRID_SIZE,
        constants.TILE_SIZE,
        (constants.SCREEN_WIDTH - constants.GRID_SIZE * constants.TILE_SIZE) // 2,
        (constants.SCREEN_HEIGHT - constants.GRID_SIZE * constants.TILE_SIZE) // 2,
        [],[]
    )
    #----------------------------------
    fuel_x = 10
    fuel_y = constants.SCREEN_HEIGHT - 200
    scaled_fuel = pygame.transform.scale(assets.fuel_gage_img, (200, 200))
    SCREEN.blit(scaled_fuel, (fuel_x, fuel_y))

    needle_scaled = pygame.transform.scale(assets.fuel_needle_img, (50,50)) #바늘 크기 조절
    #-------------------------------------

    #---------------------------------------
    # 중심 좌표
    center_x, center_y = 111,710
    angle_to_rotate = (fuel_level/100.0)*-155+37 # 파이게임에서 회전은 반시계 방향이 양수

    original_rect = needle_scaled.get_rect(center=(center_x, center_y))
    rotated_needle = pygame.transform.rotate(needle_scaled, angle_to_rotate)
    rotated_rect = rotated_needle.get_rect(center=original_rect.center)
    SCREEN.blit(rotated_needle, rotated_rect)

    fuel_text_str = f"{int(fuel_level)}%"

    current_font = assets.pressure_font_base # 기본 폰트 크기로 시작
    TEXT_COLOR = (240, 240, 240) # 기본 색상 (밝은 회색)
    
    pressure_surface = current_font.render(fuel_text_str, True, TEXT_COLOR)

    text_x = center_x 
    text_y = center_y - 110 

    pressure_rect = pressure_surface.get_rect(center=(text_x, text_y))

    SCREEN.blit(pressure_surface, pressure_rect)

    #-----------------------------------------

    # 플레이어 위치 계산
    offset_x = (constants.SCREEN_WIDTH - constants.GRID_SIZE * constants.TILE_SIZE) // 2
    offset_y = (constants.SCREEN_HEIGHT - constants.GRID_SIZE * constants.TILE_SIZE) // 2
    px = offset_x + player_col * constants.TILE_SIZE + constants.TILE_SIZE // 2
    py = offset_y + player_row * constants.TILE_SIZE + constants.TILE_SIZE // 2

    fuel_size = int(constants.TILE_SIZE * 0.92)  # 105% 크기로 약간 크게
    scaled_fuel = pygame.transform.scale(assets.fuel_img, (fuel_size, fuel_size))

    for (fr, fc) in fuel_positions:
        if (fr, fc) not in collected_fuels:
            fx = offset_x + fc * constants.TILE_SIZE + constants.TILE_SIZE // 2
            fy = offset_y + fr * constants.TILE_SIZE + constants.TILE_SIZE // 2
            rect = scaled_fuel.get_rect(center=(fx, fy))  # 중심 맞춤
            SCREEN.blit(scaled_fuel, rect)

            if player_row == fr and player_col == fc:
                collected_fuels.append((fr, fc))  # 목록에 추가 (중복 방지)
                fuel_level = min(100, fuel_level + FUEL_PER_ITEM)


    SCREEN.blit(
        assets.player_img,
        (px - constants.TILE_SIZE // 2, py - constants.TILE_SIZE // 2),
    )

    SCREEN.blit(assets.back_button_img, (button_x, button_y))
    if is_hover:
        overlay = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 60 if mouse_down else 40))  
        SCREEN.blit(overlay, (button_x, button_y))

    pygame.display.update()

pygame.quit()
sys.exit()