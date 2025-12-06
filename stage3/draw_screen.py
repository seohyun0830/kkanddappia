#배경->미로->단선글로우->수리바->플레이어->ui->효과...# stage3/draw_screen.py
import pygame
import math
from engine import assets, constants
from stage3.effects import (
    draw_low_pressure_darkness,
    draw_high_pressure_red_overlay,
    draw_broken_glow
)
from stage3.draw_ui import (
    draw_pressure_regulator,
    draw_pressure_needle,
    draw_pressure_text,
    draw_hp,
    draw_timer
)
from engine import renderer


def draw_screen(stage3):
    screen = stage3.screen

    # 1. 배경 출력
    screen.blit(assets.bk_img, (0, 0))

    # 2. 타이머 출력
    draw_timer(screen, stage3)

    # 3. 미로 출력
    renderer.draw_maze(
        screen,
        stage3.maze_data,
        constants.GRID_SIZE,
        constants.TILE_SIZE,
        constants.GRID_OFFSET_X,
        constants.GRID_OFFSET_Y,
        stage3.iron_gates,
        stage3.broken_tiles
    )

    # 아이템 표시
    teleport_img = assets.teleport_item_img  # 너가 로드한 teleport.png
    for (r, c) in stage3.item_positions:
        x = constants.GRID_OFFSET_X + c * constants.TILE_SIZE
        y = constants.GRID_OFFSET_Y + r * constants.TILE_SIZE
        screen.blit(teleport_img, (x, y))

    # 아이템 반짝 효과
    time_now = pygame.time.get_ticks()
    glow_radius = 12 + int(4 * abs(math.sin(time_now * 0.005)))
    glow_alpha  = 120 + int(60 * abs(math.sin(time_now * 0.004)))

    for (r, c) in stage3.item_positions:
        x = constants.GRID_OFFSET_X + c * constants.TILE_SIZE + constants.TILE_SIZE // 2
        y = constants.GRID_OFFSET_Y + r * constants.TILE_SIZE + constants.TILE_SIZE // 2

        # 반투명 surface 생성
        glow_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (255, 255, 100, glow_alpha), (50, 50), glow_radius)

        # 중심에 맞춰 블릿
        screen.blit(glow_surf, (x - 50, y - 50))

    # 4. 단선 타일 글로우 효과
    draw_broken_glow(
        screen,
        stage3.broken_tiles,
        constants.GRID_OFFSET_X,
        constants.GRID_OFFSET_Y
    )

    # 5. 수리 진행 바
    stage3.repair.draw_progress(
        screen,
        stage3.player_row,
        stage3.player_col
    )

    finish_active = all(not b[2] for b in stage3.broken_tiles)

    fx = constants.GRID_OFFSET_X + (constants.GRID_SIZE - 1) * constants.TILE_SIZE + constants.TILE_SIZE // 2
    fy = constants.GRID_OFFSET_Y + (constants.GRID_SIZE - 1) * constants.TILE_SIZE + constants.TILE_SIZE // 2

    pygame.draw.circle(
        screen,
        (0, 255, 0) if finish_active else (255, 0, 0),
        (fx, fy),
        8
    )

    # 6. 플레이어 이미지 출력
    draw_player(screen, stage3.player_row, stage3.player_col)
    if stage3.drone_active:
        screen.blit(
            assets.drone_img,
            (stage3.drone_x - 20, stage3.drone_y - 20)
        )


    # 7. UI 요소 (압력계, 바늘, psi 텍스트, HP바)
    draw_pressure_regulator(screen)
    draw_pressure_needle(screen, stage3.pressure)
    draw_pressure_text(screen, stage3.pressure)
    draw_hp(screen, stage3.hp)
    draw_item_ui(screen, stage3.teleport_item_count)

    # 8. 압력 상태에 따른 화면 효과
    if stage3.pressure <= 40:
        draw_low_pressure_darkness(screen, stage3)
    elif stage3.pressure >= 70:
        draw_high_pressure_red_overlay(screen, stage3)

    if stage3.drone_active:
        screen.blit(
            assets.drone_img,
            (stage3.drone_x - 20, stage3.drone_y - 20)
        )

    if stage3.selecting_teleport:
        draw_teleport_overlay(screen, stage3)


#플레이어 출력
def draw_player(screen, row, col):
    player = assets.player_img
    px = constants.GRID_OFFSET_X + col * constants.TILE_SIZE + constants.TILE_SIZE // 2
    py = constants.GRID_OFFSET_Y + row * constants.TILE_SIZE + constants.TILE_SIZE // 2

    x = px - player.get_width() // 2
    y = py - player.get_height() // 2

    screen.blit(player, (x, y))

def draw_item_ui(screen, count):
    # 화면 우측 위에 고정 표시
    x = 50
    y = 500

    # 아이템 아이콘 (크게 보이게)
    icon = assets.teleport_item_img
    icon = pygame.transform.scale(icon, (40, 40))
    screen.blit(icon, (x, y))

    # 개수 텍스트
    font = pygame.font.Font('DungGeunMO.ttf', 32)
    text = font.render(f"x {count}", True, (255, 255, 255))
    screen.blit(text, (x + 50, y + 5))

def draw_teleport_overlay(screen, stage3):
    # 전체 어둡게
    dark = pygame.Surface(
        (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT),
        pygame.SRCALPHA
    )
    dark.fill((0, 0, 0, 180))
    screen.blit(dark, (0, 0))

    # 단선 타일만 밝게 하이라이트
    for (r, c, broken) in stage3.broken_tiles:
        if not broken:
            continue

        x = constants.GRID_OFFSET_X + c * constants.TILE_SIZE
        y = constants.GRID_OFFSET_Y + r * constants.TILE_SIZE

        glow = pygame.Surface((constants.TILE_SIZE, constants.TILE_SIZE), pygame.SRCALPHA)
        glow.fill((255, 200, 0, 160))  # 노란 하이라이트
        screen.blit(glow, (x, y))

    # 안내 텍스트
    font = pygame.font.Font('DungGeunMO.ttf', 36)
    text = font.render("이동할 단선을 클릭하세요 (ESC 취소)", True, (255, 255, 255))
    tr = text.get_rect(center=(constants.SCREEN_WIDTH//2, constants.SCREEN_HEIGHT//2 - 200))
    screen.blit(text, tr)
