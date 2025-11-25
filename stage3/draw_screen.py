#배경->미로->단선글로우->수리바->플레이어->ui->효과...# stage3/draw_screen.py
import pygame
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
    draw_hp
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

    # 7. UI 요소 (압력계, 바늘, psi 텍스트, HP바)
    draw_pressure_regulator(screen)
    draw_pressure_needle(screen, stage3.pressure)
    draw_pressure_text(screen, stage3.pressure)
    draw_hp(screen, stage3.hp)

    # 8. 압력 상태에 따른 화면 효과
    if stage3.pressure <= 40:
        draw_low_pressure_darkness(screen, stage3)
    elif stage3.pressure >= 70:
        draw_high_pressure_red_overlay(screen, stage3)

    # 9. 가이드북 버튼 (항상 표시)
    screen.blit(assets.guide_book_button, (constants.SCREEN_WIDTH - 120, 20))


#타이머 그리기
def draw_timer(screen, stage3):
    current_ticks = pygame.time.get_ticks()
    elapsed_time = current_ticks - stage3.start_time - stage3.guide.game_paused_time
    remaining_time = max(0, constants.TOTAL_GAME_TIME_SECONDS * 1000 - elapsed_time)

    minutes = remaining_time // 1000 // 60
    seconds = (remaining_time // 1000) % 60

    text = f"{minutes:02}:{seconds:02}"
    surface = assets.timer_font.render(text, True, (220, 220, 220))

    screen.blit(surface, (10, 10))


#플레이어 출력
def draw_player(screen, row, col):
    px = constants.GRID_OFFSET_X + col * constants.TILE_SIZE + constants.TILE_SIZE // 2
    py = constants.GRID_OFFSET_Y + row * constants.TILE_SIZE + constants.TILE_SIZE // 2

    screen.blit(assets.player_img, (px - constants.TILE_SIZE // 2,
                                    py - constants.TILE_SIZE // 2))
