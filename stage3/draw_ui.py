#HP,압력계,압력텍스트,연료
# stage3/draw_ui.py
import pygame
import math
from engine import constants, assets

def draw_pressure_regulator(screen):
    regulator_x = 10
    regulator_y = constants.SCREEN_HEIGHT - 200
    scaled = pygame.transform.scale(assets.pressure_regulator_img, (200, 200))
    screen.blit(scaled, (regulator_x, regulator_y))

def draw_pressure_needle(screen, pressure):
    # 바늘 중심 위치
    center_x, center_y = 111, 700

    # 압력 → 회전각 변환 (0~100 → -90° ~ +180°)
    rotation_angle = (pressure / 100.0) * 270 - 90
    angle_to_rotate = -rotation_angle  # pygame은 반시계방향 +임

    needle_img = pygame.transform.scale(assets.needle_img, (30, 30))
    original_rect = needle_img.get_rect(center=(center_x, center_y))

    rotated = pygame.transform.rotate(needle_img, angle_to_rotate)
    rotated_rect = rotated.get_rect(center=original_rect.center)

    screen.blit(rotated, rotated_rect)


def draw_pressure_text(screen, pressure):
    pressure_text = f"{int(pressure)}psi"

    # 기본 폰트
    font = assets.pressure_font_base
    color = (240, 240, 240)

    current_time = pygame.time.get_ticks()

    # 고압 (70 이상 → 빨간색 + 깜빡임)
    if pressure > 70:
        color = (255, 50, 50)

        pulsation = (math.sin(current_time * constants.PULSATE_SPEED) + 1.0)
        pulsation *= (constants.PULSATE_MAX_OFFSET / 2)
        size = constants.BASE_FONT_SIZE + pulsation
        font = pygame.font.SysFont(constants.FONT_NAME, int(size), bold=True)

    # 저압 (40 이하 → 보라색 + 깜빡임)
    elif pressure < 40:
        color = (200, 50, 255)

        pulsation = (math.sin(current_time * constants.PULSATE_SPEED) + 1.0)
        pulsation *= (constants.PULSATE_MAX_OFFSET / 2)
        size = constants.BASE_FONT_SIZE + pulsation
        font = pygame.font.SysFont(constants.FONT_NAME, int(size), bold=True)

    # 텍스트 위치
    text_x = 111
    text_y = 600
    surface = font.render(pressure_text, True, color)
    rect = surface.get_rect(center=(text_x, text_y))

    screen.blit(surface, rect)


def draw_hp(screen, hp):
    assets.draw_hp_bar(screen, hp)
