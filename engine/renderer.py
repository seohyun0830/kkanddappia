#미로화면 그리는 부분
import pygame
import random
from . import assets, constants

#벽,파이프,단선,철문 이미지를 타일 크기에 맞게 그린다
def draw_maze(SCREEN, maze_data, grid_size, tile_size, offset_x, offset_y,
              iron_gates=None, broken_tiles=None):
    for i in range(grid_size):
        for j in range(grid_size):
            x = j * tile_size + offset_x
            y = i * tile_size + offset_y

            tile = maze_data[i][j]
            
            #벽
            if tile == constants.WALL:
                draw_wall_tile(SCREEN, x, y, tile_size)
                continue

            #단선
            if tile == constants.BROKEN:
                draw_wall_tile(SCREEN, x, y, tile_size)  # 기본 배경
                draw_broken_tile(SCREEN, x, y, tile_size)
                continue

            #철문
            if tile == constants.IRON_GATE:
                draw_iron_gate(SCREEN, i, j, x, y, tile_size, iron_gates)
                continue

            #파이프
            img = get_pipe_tile_image(i, j, maze_data, grid_size, iron_gates, broken_tiles)
            SCREEN.blit(pygame.transform.scale(img, (tile_size, tile_size)), (x, y))

#벽 타일 
def draw_wall_tile(SCREEN, x, y, tile_size):
    tile_img = pygame.transform.scale(assets.bg_img, (tile_size, tile_size))
    SCREEN.blit(tile_img, (x, y))

#단선 타일 + 스파크 효과
def draw_broken_tile(SCREEN, x, y, tile_size):
    spark = assets.pipe_images[constants.BROKEN].copy()
    spark.set_alpha(random.randint(160, 255))

    scaled = pygame.transform.scale(spark, (tile_size, tile_size))
    SCREEN.blit(scaled, (x, y))

#철문 + 슬라이드 효과
def draw_iron_gate(SCREEN, r, c, x, y, tile_size, iron_gates):
    if iron_gates is None:
        return

    for gate in iron_gates:
        gr, gc, closed, slide_y = gate

        if gr == r and gc == c:

            # 슬라이드 애니메이션: 아래로 5px씩 이동
            if closed:
                gate[3] = min(0, slide_y + 5)  # 0 = 제자리

            img = assets.pipe_images[constants.IRON_GATE]
            scaled = pygame.transform.scale(img, (tile_size, tile_size))

            SCREEN.blit(scaled, (x, y + gate[3]))
            return

#파이프 타일 11가지 상하좌우 연결
def get_pipe_tile_image(i, j, maze_data, grid_size, iron_gates, broken_tiles):
    tile = maze_data[i][j]

    def is_open(r, c):
        if not (0 <= r < grid_size and 0 <= c < grid_size):
            return False
        return maze_data[r][c] in [constants.PATH, constants.IRON_GATE, constants.BROKEN]

    up    = is_open(i - 1, j)
    down  = is_open(i + 1, j)
    left  = is_open(i, j - 1)
    right = is_open(i, j + 1)

    img_key = choose_pipe(up, down, left, right)
    return assets.pipe_images[img_key]

#파이프 이미지 고르는 부분
def choose_pipe(up, down, left, right):
    if up and down and left and right: return 11
    elif up and down and left and not right: return 8
    elif up and down and not left and right: return 7
    elif up and not down and left and right: return 10
    elif not up and down and left and right: return 9
    elif left and right and not up and not down: return 1
    elif up and down and not left and not right: return 2
    elif not up and right and down and not left: return 3
    elif not up and left and down and not right: return 4
    elif up and right and not down and not left: return 5
    elif up and left and not down and not right: return 6
    elif up or down: return 2
    elif left or right: return 1
    return 2
