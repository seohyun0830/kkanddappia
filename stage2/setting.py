import pygame
import os

# --- 화면 및 게임 설정 ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

CLICK_AREA = pygame.Rect(850, 100, 300, 380)    # 제작 책상
OUTSIDE_DOOR_AREA = pygame.Rect(400, 400, 400, 300) # 밖으로 나가는 문
TREE_AREA = pygame.Rect(840, 430, 120, 290)     # 나무
DIC_AREA = pygame.Rect(250, 480, 250, 100)      # [추가!] 방 안의 사전 오브젝트
SPACESHIP_AREA = pygame.Rect(900, 600, 280, 100) # 우주선

# --- 색상 ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# --- 경로 설정 ---
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'kkanddabbia')
if not os.path.isdir(assets_path):
    assets_path = current_path

# --- 플레이어 설정 ---
PLAYER_SIZE = (100, 100)
ANIMATION_SPEED = 6

# --- 아이콘 및 UI 설정 ---
ICON_SIZE = 80
ICON_MARGIN = 10
ITEM_SIZE = 70
SPACESHIP_ITEM_SIZE = 90
MAX_STACK_SIZE = 10
MAX_DIC_PAGES = 11

DIC_ICON_X = SCREEN_WIDTH - ICON_MARGIN - ICON_SIZE
DIC_ICON_Y = ICON_MARGIN

BAG_ICON_X = DIC_ICON_X - ICON_SIZE
BAG_ICON_Y = ICON_MARGIN

# --- 우주선 제작 조건 ---
SPACESHIP_REQUIREMENTS = {
    'spaceship-roof': 4,
    'spaceship-side': 4,
    'fuel tank': 7,
}
MAX_SPACESHIP_PARTS = sum(SPACESHIP_REQUIREMENTS.values()) # 15

# --- 제작 레시피 (데이터) ---
RECIPES = [
    {
        'recipe': [None, 'wood', None,
                   None, 'wood', None,
                   None, 'wood', None],
        'result': 'stick'
    },
    {
        'recipe': [None, None, None,
                   None, 'fossil', 'fossil',
                   None, None, None],
        'result': 'fuel'
    },
    {
        'recipe': [None, None, None,
                   'stone', 'stone', 'fire',
                   None, None, None],
        'result': 'steel'
    },
    {
        'recipe': ['steel', 'steel', 'steel',
                   None, 'stick', None,
                   None, 'stick', None],
        'result': 'hammer'
    },
    {
        'recipe': ['steel', 'steel', 'steel',
                   None, 'stick', None,
                   None, 'stick', None],
        'result': 'axe'
    },
    {
        'recipe': [None, None, None,
                   None, 'steel', None,
                   None, 'steel', None],
        'result': 'screw'
    },
    {
        'recipe': [None, None, None,
                   'steel', 'fuel', 'steel',
                   None, 'steel', None],
        'result': 'fuel tank'
    },
    {
        'recipe': [None, 'soil', None,
                   'soil', 'fire', 'soil',
                   None, 'soil', None],
        'result': 'glass'
    },
    {
        'recipe': [None, None, None,
                   None, 'glass', 'glass',
                   None, 'glass', 'glass'],
        'result': 'window-piece'
    },
    {
        'recipe': ['stick', None, 'stick',
                   'stick', 'stick', 'stick',
                   'stick', None, 'stick'],
        'result': 'ladder'
    },
    {
        'recipe': [None, None, None,
                   None, None, None,
                   None, None, None],
        'result': None
    }
]