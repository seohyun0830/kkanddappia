import pygame
import constants

pipe_images = {}

#파이프 이미지 11개 배열로 저장
def load_pipe_images():
    global bg_img,fuel_img
    for i in range(1, 12):
        pipe_images[i] = pygame.image.load(f'images/pipe{i}.jpg')
    pipe_images[constants.IRON_GATE] = pygame.image.load('images/irongate.jpg').convert_alpha()
    pipe_images[constants.BROKEN] = pygame.image.load('images/broken.png').convert_alpha()
    bg_img = pygame.image.load('images/bg_img.jpg')
    fuel_img=pygame.image.load('images/fuel.png')

#압력조절기
def load_pressure_images():
    global pressure_regulator_img, needle_img
    pressure_regulator_img = pygame.image.load('images/pressure.png')
    needle_img = pygame.image.load('images/needle.png')

#연료게이지
def load_fuel_gage_images():
    global fuel_gage_img, fuel_needle_img
    fuel_gage_img = pygame.image.load('images/fuelgage.png')
    fuel_needle_img = pygame.image.load('images/needle.png')

# 배경 이미지
bk_img = pygame.image.load("images/bk.jpg")
bk_img = pygame.transform.scale(bk_img, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

# 플레이어 이미지
player_img = pygame.image.load("images/c1.png")
player_img = pygame.transform.scale(player_img, (constants.TILE_SIZE, constants.TILE_SIZE))

#폰트설정 
pressure_font_base = pygame.font.SysFont(constants.FONT_NAME, constants.BASE_FONT_SIZE, bold=True)
timer_font = pygame.font.SysFont(constants.FONT_NAME, constants.TIMER_FONT_SIZE, bold=True)

back_button_img=pygame.image.load('images/backto4.png')
back_button_img=pygame.transform.scale(back_button_img,(150,150))

#HP 색상 계산
def get_hp_color(hp_ratio):
    if hp_ratio > 0.7:
        base_color = (0, 255, 0)        # 초록 (안정)
    elif hp_ratio > 0.4:
        base_color = (255, 255, 0)      # 노랑 (주의)
    elif hp_ratio > 0.1:
        base_color = (255, 0, 0)        # 빨강 (위험)
    else:
        base_color = (150, 150, 150)    # 회색 (거의 사망)

    dark_factor = max(0.0, min(1.0, hp_ratio))
    r = int(base_color[0] * dark_factor)
    g = int(base_color[1] * dark_factor)
    b = int(base_color[2] * dark_factor)

    return (r,g,b)

#HP바 그리기 함수
def draw_hp_bar(screen,hp):
    hp_ratio = max(0.0, min(1.0, hp / constants.MAX_HP))
    color = get_hp_color(hp_ratio)

    # HP바 배경 (어두운 회색)
    pygame.draw.rect(screen, (30, 30, 30), (constants.HP_BAR_X, constants.HP_BAR_Y, constants.HP_BAR_W, constants.HP_BAR_H))

    # 현재 HP바 (채워진 영역)
    filled_width = int(constants.HP_BAR_W * hp_ratio)
    pygame.draw.rect(screen, color, (constants.HP_BAR_X, constants.HP_BAR_Y, filled_width, constants.HP_BAR_H))

    # 테두리
    pygame.draw.rect(screen, (200, 200, 200), (constants.HP_BAR_X, constants.HP_BAR_Y, constants.HP_BAR_W, constants.HP_BAR_H), 2)

    # 숫자 표시 (선택 사항)
    font = pygame.font.SysFont(constants.FONT_NAME, 18, bold=True)
    hp_text = font.render(f"HP: {int(hp)}%", True, (220, 220, 220))
    text_rect = hp_text.get_rect(center=(constants.HP_BAR_X + constants.HP_BAR_W // 2, constants.HP_BAR_Y + constants.HP_BAR_H // 2))
    screen.blit(hp_text, text_rect)