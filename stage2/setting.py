import pygame
import os

# --- 화면 설정 ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# --- 색상 ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (50, 50, 50)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255) 

# --- 경로 설정 ---
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(CURRENT_PATH, 'kkanddabbia')
if not os.path.isdir(ASSETS_PATH):
    ASSETS_PATH = CURRENT_PATH 

# --- 플레이어 설정 ---
PLAYER_SIZE = (100, 100)
PLAYER_SPEED = 5
ANIMATION_SPEED = 6 
TREE_ANIMATION_SPEED = 12
PLAYER_START_X = 100
PLAYER_START_Y = 630
SPACESHIP_WALK_Y = 590

# --- 페이드 아웃 설정 ---
FADE_SPEED = 5

# --- 상호작용 거리 ---
INTERACTION_RANGE = 200

# --- 이미지 크기 ---
IMG_SIZE_MAKE = (600, 600)
IMG_SIZE_MAKE2 = (546, 380)
IMG_SIZE_INVEN = (600, 600)
IMG_SIZE_DIC = (600, 600)
IMG_SIZE_SPACESHIP_MAKE = (600, 600)
IMG_SIZE_ICON = (80, 80)
ITEM_SIZE = 70
SPACESHIP_ITEM_SIZE = 90
SLOT_SIZE_PX = 92

#화살표
ARROW_SIZE=70

# --- [추가] 쪽지(Paper) 설정 ---
PAPER_SIZE = 40
NOTE_APPEAR_INTERVAL = 5000  # 5초(5000ms)마다 하나씩 나타남

# 쪽지 8개의 위치 (맵 이름, x좌표, y좌표) - 순서대로 나타납니다.
NOTE_DATA = [
    {"map": "outside1", "pos": (200, 650)},  # 1번
    {"map": "outside1", "pos": (600, 650)},  # 2번
    {"map": "inside",   "pos": (300, 500)},  # 3번
    {"map": "inside",   "pos": (900, 500)},  # 4번
    {"map": "outside2", "pos": (100, 650)},  # 5번
    {"map": "outside2", "pos": (800, 650)},  # 6번
    {"map": "outside1", "pos": (1000, 650)}, # 7번
    {"map": "inside",   "pos": (600, 500)}   # 8번
]

# --- UI 위치 ---
MAKE_IMAGE_X = (SCREEN_WIDTH - IMG_SIZE_MAKE[0]) // 2
MAKE_IMAGE_Y = (SCREEN_HEIGHT - IMG_SIZE_MAKE[1]) // 2
MAKE2_IMAGE_X = (SCREEN_WIDTH - IMG_SIZE_MAKE2[0]) // 2 - 310
MAKE2_IMAGE_Y = (SCREEN_HEIGHT - IMG_SIZE_MAKE2[1]) // 2
INVEN_IMAGE_X = (SCREEN_WIDTH - IMG_SIZE_INVEN[0]) // 2 + 280
INVEN_IMAGE_Y = (SCREEN_HEIGHT - IMG_SIZE_INVEN[1]) // 2
CENTERED_INV_X = (SCREEN_WIDTH - IMG_SIZE_INVEN[0]) // 2 
INV_CENTER_SHIFT_X = CENTERED_INV_X - INVEN_IMAGE_X
INV_DRAW_Y = INVEN_IMAGE_Y
SPACESHIP_MAKE_IMAGE_X = (SCREEN_WIDTH - IMG_SIZE_SPACESHIP_MAKE[0]) // 2
SPACESHIP_MAKE_IMAGE_Y = (SCREEN_HEIGHT - IMG_SIZE_SPACESHIP_MAKE[1]) // 2
DIC_IMAGE_X = (SCREEN_WIDTH - IMG_SIZE_DIC[0]) // 2
DIC_IMAGE_Y = (SCREEN_HEIGHT - IMG_SIZE_DIC[1]) // 2

ICON_MARGIN = 10
DIC_ICON_X = SCREEN_WIDTH - ICON_MARGIN - IMG_SIZE_ICON[0]
DIC_ICON_Y = ICON_MARGIN
BAG_ICON_X = DIC_ICON_X - IMG_SIZE_ICON[0]
BAG_ICON_Y = ICON_MARGIN

# --- 클릭 영역 ---
CLICK_AREA = pygame.Rect(850, 100, 300, 380) 
OUTSIDE_DOOR_AREA = pygame.Rect(400, 400, 400, 300) 
OUTSIDE_MAKE_AREA = pygame.Rect(10, 340, 490, 350) 
TREE_AREA = pygame.Rect(840, 430, 120, 290) 
DIC_AREA = pygame.Rect(250, 480, 250, 100)
SPACESHIP_AREA = pygame.Rect(900, 600, 280, 100)
STAGE1_AREA = pygame.Rect(100, 500, 300, 200)
MAKE_BUTTON_AREA = pygame.Rect(420, 260, 115, 115)
ERASE_BUTTON_AREA = pygame.Rect(420, 400, 115, 115)
DIC_ICON_AREA = pygame.Rect(DIC_ICON_X, DIC_ICON_Y, IMG_SIZE_ICON[0], IMG_SIZE_ICON[1])
BAG_ICON_AREA = pygame.Rect(BAG_ICON_X, BAG_ICON_Y, IMG_SIZE_ICON[0], IMG_SIZE_ICON[1])
SPACESHIP_DROP_AREA = pygame.Rect(SPACESHIP_MAKE_IMAGE_X + 50, SPACESHIP_MAKE_IMAGE_Y + 50, 500, 500)

# --- 1페이지 슬롯 ---
INVENTORY_SLOT_POSITIONS = []
INVENTORY_SLOT_RECTS = []
INV_X_REL_COORDS = [50, 142, 234, 326, 418, 512]
INV_Y_REL_COORDS = [50, 142, 234, 326, 418, 512]
for rel_y in INV_Y_REL_COORDS:
    for rel_x in INV_X_REL_COORDS:
        absolute_x = INVEN_IMAGE_X + rel_x - (ITEM_SIZE // 2) + 20
        absolute_y = INVEN_IMAGE_Y + rel_y - (ITEM_SIZE // 2) + 20
        INVENTORY_SLOT_POSITIONS.append((absolute_x, absolute_y))
        INVENTORY_SLOT_RECTS.append(pygame.Rect(absolute_x, absolute_y, ITEM_SIZE, ITEM_SIZE))

# --- 2페이지 슬롯 ---
INVENTORY_PAGE2_SLOT_POSITIONS = []
INVENTORY_PAGE2_SLOT_RECTS = []
INV_P2_X_REL = [120, 380] 
INV_P2_Y_REL = [120, 380]
for rel_y in INV_P2_Y_REL:
    for rel_x in INV_P2_X_REL:
        absolute_x = INVEN_IMAGE_X + rel_x - (SPACESHIP_ITEM_SIZE // 2)
        absolute_y = INVEN_IMAGE_Y + rel_y - (SPACESHIP_ITEM_SIZE // 2)
        INVENTORY_PAGE2_SLOT_POSITIONS.append((absolute_x, absolute_y))
        INVENTORY_PAGE2_SLOT_RECTS.append(pygame.Rect(absolute_x, absolute_y, SPACESHIP_ITEM_SIZE, SPACESHIP_ITEM_SIZE))

SPACESHIP_PART_NAMES = ['spaceship-side-piece', 'spaceship-roof-piece','spaceship-side', 'spaceship-roof']

# --- 제작 슬롯 ---
CRAFT_SLOT_POSITIONS = []
CRAFT_SLOT_RECTS = []
CRAFT_X_POSITIONS = [51, 151, 251]
CRAFT_Y_POSITIONS = [56, 154, 255]
for rel_y in CRAFT_Y_POSITIONS:
    for rel_x in CRAFT_X_POSITIONS:
        absolute_x = MAKE2_IMAGE_X + rel_x
        absolute_y = MAKE2_IMAGE_Y + rel_y
        CRAFT_SLOT_POSITIONS.append((absolute_x, absolute_y))
        CRAFT_SLOT_RECTS.append(pygame.Rect(absolute_x, absolute_y, ITEM_SIZE, ITEM_SIZE))

# --- 우주선 슬롯 ---
SPACESHIP_SLOT_POSITIONS = []
SPACESHIP_SLOT_RECTS = []
SPACESHIP_X_REL_COORDS = [55, 188, 321, 454]
SPACESHIP_Y_REL_COORDS = [55, 188, 321, 454]
SPACESHIP_REQUIREMENTS = {'spaceship-roof': 4, 'spaceship-side': 4, 'fuel tank': 7}
MAX_SPACESHIP_PARTS = sum(SPACESHIP_REQUIREMENTS.values()) 
_slot_relative_coords = []
for rel_y in SPACESHIP_Y_REL_COORDS:
    for rel_x in SPACESHIP_X_REL_COORDS:
        _slot_relative_coords.append((rel_x, rel_y))
if len(_slot_relative_coords) > MAX_SPACESHIP_PARTS:
    _slot_relative_coords = _slot_relative_coords[:MAX_SPACESHIP_PARTS] 
for rel_x, rel_y in _slot_relative_coords:
    absolute_x = SPACESHIP_MAKE_IMAGE_X + rel_x
    absolute_y = SPACESHIP_MAKE_IMAGE_Y + rel_y
    SPACESHIP_SLOT_POSITIONS.append((absolute_x, absolute_y))
    SPACESHIP_SLOT_RECTS.append(pygame.Rect(absolute_x, absolute_y, SLOT_SIZE_PX, SLOT_SIZE_PX))

MAX_STACK_SIZE = 10
MAX_DIC_PAGES = 14
GATHER_DURATION = 3000
PULSATE_SPEED = 0.003
PULSATE_MIN_SCALE = 0.9
PULSATE_MAX_SCALE = 1.1

RECIPES = [
    {'recipe':[None, None, None,
               None, 'wood', None,
               None, None, 'axe'],
    'result':'stick'
    },
    {'recipe':[None, None, None,
               None, 'fossil', 'fossil',
               None, None, None],
    'result':'fuel'
    },
    {'recipe':[None, None, None,
               'stone','stone','fire',
               None, None, None],
    'result':'steel'
    },
    {'recipe':['steel', 'steel', 'steel',
               None, 'stick', None,
               None, 'stick', None],
    'result':'hammer'
    },
    {'recipe':[None, None, None,
               None, 'steel', None,
               None, 'steel', None],
    'result':'screw'},
    {'recipe':[None, None, None,
               'steel', 'fuel', 'steel',
               None, 'steel', None],
    'result':'fuel tank'},
    {'recipe':[None, None, None,
               None, 'soil', None,
               None, 'soil', 'fire'],
    'result':'glass'},
    {'recipe':[None, None, None,
               None, 'glass', None,
               None, 'glass', 'hammer'],
    'result':'window-piece'},
    {'recipe':[None, None, None,
               None, 'stick', None,
               'stick', None, 'stick'],
    'result':'ladder'},
    {'recipe':['steel', None, 'steel',
               'screw', 'window-piece', 'screw',
               'steel', 'hammer', 'steel'],
     'result':'spaceship-side-piece'},
    {'recipe':['spaceship-side-piece', 'spaceship-side-piece', 'spaceship-side-piece',
               'spaceship-side-piece','spaceship-side-piece','spaceship-side-piece',
               'spaceship-side-piece','spaceship-side-piece','spaceship-side-piece'],

    'result':'spaceship-side'
    },
    {'recipe':['steel', 'steel', None,
               'screw', 'screw', 'hammer',
               'steel', 'steel', None],
    'result':'spaceship-roof-piece'
    },
    {'recipe':['spaceship-roof-piece', 'spaceship-roof-piece', None,
               'spaceship-roof-piece', 'spaceship-roof-piece', None,
               None, None, None],
    'result':'spaceship-roof'
    },
    {'recipe':[None, None, None, None, None, None, None, None, None], 'result':None}
]