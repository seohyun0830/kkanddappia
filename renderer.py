import pygame
import assets
import constants
import random

def draw_maze(SCREEN, maze_data, grid_size, tile_size, offset_x, offset_y, iron_gates=None, broken_tiles=None):
    for i in range(grid_size):
        for j in range(grid_size):
            x, y = j * tile_size + offset_x, i * tile_size + offset_y
            tile = maze_data[i][j]

            # 벽
            if tile == constants.WALL:
                SCREEN.blit(pygame.transform.scale(assets.bg_img, (tile_size, tile_size)), (x, y))
                continue

            if tile == constants.BROKEN:
                SCREEN.blit(pygame.transform.scale(assets.bg_img, (tile_size, tile_size)), (x, y))
                #스파크이미지 깜빡이도록
                spark = assets.pipe_images[constants.BROKEN].copy()
                spark_alpha = random.randint(150, 255)
                spark.set_alpha(spark_alpha)

                SCREEN.blit(
                    pygame.transform.scale(spark, (tile_size, tile_size)),
                    (x, y)
                )

                continue

            if tile == constants.IRON_GATE:
                is_closed = any(g[0] == i and g[1] == j and g[2] for g in iron_gates)
                if is_closed:
                    SCREEN.blit(pygame.transform.scale(assets.pipe_images[constants.IRON_GATE], (tile_size, tile_size)), (x, y))
                    continue
    

            img = get_tile_image(i, j, maze_data, grid_size, iron_gates, broken_tiles)
            SCREEN.blit(pygame.transform.scale(img, (tile_size, tile_size)), (x, y))

def get_tile_image(i, j, maze_data, grid_size, iron_gates, broken_tiles):
    from assets import pipe_images
    tile = maze_data[i][j]
    
    up = (i>0 and maze_data[i-1][j] in [constants.PATH, constants.IRON_GATE, constants.BROKEN])
    down = (i<grid_size-1 and maze_data[i+1][j] in [constants.PATH, constants.IRON_GATE, constants.BROKEN])
    left = (j>0 and maze_data[i][j-1] in [constants.PATH, constants.IRON_GATE, constants.BROKEN])
    right = (j<grid_size-1 and maze_data[i][j+1] in [constants.PATH, constants.IRON_GATE, constants.BROKEN])
    
    img_key = choose_pipe(up, down, left, right)
    return pipe_images[img_key]

# 파이프 이미지 
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
