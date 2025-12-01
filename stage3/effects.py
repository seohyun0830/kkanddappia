#단선 글로우 효과,저압 어두워지고 주변만 보이는,고압 붉은 화면 
import pygame
import math
from engine import constants

def draw_broken_glow(screen, broken_tiles, offset_x, offset_y):

    for b in broken_tiles:
        r, c, is_broken = b
        if not is_broken:
            continue

        # 타일 중심 위치 계산
        center_x = offset_x + c * constants.TILE_SIZE + constants.TILE_SIZE // 2
        center_y = offset_y + r * constants.TILE_SIZE + constants.TILE_SIZE // 2

        tile_size = constants.TILE_SIZE
        glow_radius = int(tile_size * 1.2)
        glow_diameter = glow_radius * 2

        # 글로우 Surface
        glow = pygame.Surface((glow_diameter, glow_diameter), pygame.SRCALPHA)

        # 알파값을 시간에 따라 깜빡임
        alpha = 70 + int(50 * math.sin(pygame.time.get_ticks() * 0.005))

        pygame.draw.circle(
            glow,
            (255, 120, 0, alpha),  # 오렌지색 + 알파
            (glow_radius, glow_radius),
            glow_radius
        )

        screen.blit(glow, (center_x - glow_radius, center_y - glow_radius))

def draw_low_pressure_darkness(screen, stage3):
    pressure = stage3.pressure

    maze_w = constants.GRID_SIZE * constants.TILE_SIZE
    maze_h = constants.GRID_SIZE * constants.TILE_SIZE

    maze_x = constants.GRID_OFFSET_X
    maze_y = constants.GRID_OFFSET_Y

    # 어두운 정도 (압력이 낮을수록 더 어둡게)
    max_black = 200
    min_black = 250
    sight_black = int(min_black + (max_black - min_black) * (pressure / 40))

    darkness_mask = pygame.Surface((maze_w, maze_h), pygame.SRCALPHA)
    darkness_mask.fill((0, 0, 0, sight_black))

    # 플레이어 위치 (local 좌표)
    px = maze_x + stage3.player_col * constants.TILE_SIZE + constants.TILE_SIZE // 2
    py = maze_y + stage3.player_row * constants.TILE_SIZE + constants.TILE_SIZE // 2

    local_px = px - maze_x
    local_py = py - maze_y

    # 플레이어 주변만 둥글게 밝게
    pygame.draw.circle(
        darkness_mask,
        (0, 0, 0, 0),
        (local_px, local_py),
        60
    )

    screen.blit(darkness_mask, (maze_x, maze_y))

def draw_high_pressure_red_overlay(screen, stage3):
    pressure = stage3.pressure

    redness = int(180 * ((pressure - 70) / 30.0))  # 50~180
    redness = min(180, max(50, redness))

    overlay_red = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    overlay_red.set_alpha(redness)
    overlay_red.fill((255, 0, 0))

    screen.blit(overlay_red, (0, 0))
