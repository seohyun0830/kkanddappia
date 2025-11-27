"""
이미지,폰트 로드, ui리소스 로딩
"""
import pygame
from . import constants

pygame.font.init()

pipe_images = {}             # 미로 파이프 이미지
pressure_regulator_img = None
needle_img = None

fuel_gage_img = None
fuel_needle_img = None

bg_img = None                # 배경 이미지(벽)
player_img = None            # 플레이어 이미지
back_button_img = None       # Stage4로 돌아가기 버튼

# 가이드북 이미지
guide_book_button = None
guide_images = []            # [g1, g2, g3, g4, g5]

# 폰트
pressure_font_base = pygame.font.SysFont(constants.FONT_NAME, constants.BASE_FONT_SIZE, bold=True)
timer_font = pygame.font.SysFont(constants.FONT_NAME, constants.TIMER_FONT_SIZE, bold=True)

fuel_img=None

#파이프,단선,철문이미지 전부 
def load_pipe_images():
    global pipe_images, bg_img

    # 1~11번 파이프
    for i in range(1, 12):
        pipe_images[i] = pygame.image.load(f'images/stage3/pipe{i}.jpg')

    # 철문 / 단선
    pipe_images[constants.IRON_GATE] = pygame.image.load('images/stage3/irongate.jpg').convert_alpha()
    pipe_images[constants.BROKEN] = pygame.image.load('images/stage3/broken.png').convert_alpha()

    # 미로 배경(벽)
    bg_img_raw = pygame.image.load("images/stage3/bg_img.jpg")
    bg_img = pygame.transform.scale(bg_img_raw, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    
#배경 로드
def load_background():
    global bk_img
    raw = pygame.image.load("images/stage3/bk.jpg")
    bk_img = pygame.transform.scale(raw, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

#플레이어 이미지
def load_player():
    global player_img
    raw = pygame.image.load("images/stage3/c1.png")
    player_img = pygame.transform.scale(raw, (constants.TILE_SIZE, constants.TILE_SIZE))
  
#압력계 이미지
def load_pressure_images():
    global pressure_regulator_img, needle_img
    pressure_regulator_img = pygame.image.load('images/stage3/pressure.png')
    needle_img = pygame.image.load('images/stage3/needle.png')

#연료게이지 이미지
def load_fuel_gage_images():
    global fuel_gage_img, fuel_needle_img
    fuel_gage_img = pygame.image.load('images/stage3/fuel_gage.png')
    fuel_needle_img = pygame.image.load('images/stage3/fuel_needle.png')

# HP 바 그리기 함수 (Stage3 UI에서 사용)
def draw_hp_bar(screen, hp):
    hp_ratio = max(0.0, min(1.0, hp / constants.MAX_HP))

    # 색상 계산
    if hp_ratio > 0.7:
        color = (0, 255, 0)
    elif hp_ratio > 0.4:
        color = (255, 255, 0)
    elif hp_ratio > 0.1:
        color = (255, 0, 0)
    else:
        color = (150, 150, 150)

    # 회색 배경 bar
    pygame.draw.rect(
        screen,
        (30, 30, 30),
        (constants.HP_BAR_X, constants.HP_BAR_Y, constants.HP_BAR_W, constants.HP_BAR_H)
    )

    # 실제 HP bar
    filled_width = int(constants.HP_BAR_W * hp_ratio)
    pygame.draw.rect(
        screen,
        color,
        (constants.HP_BAR_X, constants.HP_BAR_Y, filled_width, constants.HP_BAR_H)
    )

    # 테두리
    pygame.draw.rect(
        screen,
        (200, 200, 200),
        (constants.HP_BAR_X, constants.HP_BAR_Y, constants.HP_BAR_W, constants.HP_BAR_H),
        2
    )

    # 텍스트 (HP: 85%)
    font = pygame.font.SysFont(constants.FONT_NAME, 18, bold=True)
    text = font.render(f"HP: {int(hp)}%", True, (230, 230, 230))
    text_rect = text.get_rect(
        center=(constants.HP_BAR_X + constants.HP_BAR_W // 2,
                constants.HP_BAR_Y + constants.HP_BAR_H // 2)
    )
    screen.blit(text, text_rect)


#가이드북
def load_guide_images():
    global guide_book_button, guide_images

    # 가이드북 버튼
    guide_raw = pygame.image.load('images/stage3/guidebook.png')
    guide_book_button = pygame.transform.scale(guide_raw, (100, 100))

    # 페이지 1~5
    guide_images = []
    for i in range(1, 6):
        img = pygame.image.load(f'images/stage3/guide{i}.jpg')
        guide_images.append(img)

def load_fuel_image():
    global fuel_img
    fuel_img = pygame.image.load("images/stage3/fuel.png").convert_alpha()

   
#3->4stage버튼
def load_back_button():
    global back_button_img
    raw = pygame.image.load('images/stage3/backto4.png')
    back_button_img = pygame.transform.scale(raw, (150, 150))


#게임 시작 시 한번만 호출하면 모든 이미지 로딩됨
def load_all():
    load_pipe_images()
    load_background()
    load_player()
    load_pressure_images()
    load_fuel_gage_images()
    load_back_button()
    load_guide_images()
    load_fuel_image()