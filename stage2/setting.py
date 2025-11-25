import pygame
import os

# 화면
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# 색
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (50, 50, 50)
GREEN = (0, 200, 0)

# 경로
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(CURRENT_PATH, 'kkanddabbia')
if not os.path.isdir(ASSETS_PATH):
    ASSETS_PATH = CURRENT_PATH 

# 사람
PLAYER_SIZE = (100, 100)
PLAYER_SPEED = 5
ANIMATION_SPEED = 6
PLAYER_START_X = 100
PLAYER_START_Y = 630
SPACESHIP_WALK_Y = 590

EASY_MODE=True

FADE_SPEED = 5

# 이미지
IMG_SIZE_MAKE = (600, 600)
IMG_SIZE_MAKE2 = (546, 380)
IMG_SIZE_INVEN = (600, 600)
IMG_SIZE_DIC = (600, 600)
IMG_SIZE_SPACESHIP_MAKE = (600, 600)
IMG_SIZE_ICON = (80, 80)
ITEM_SIZE = 70
SPACESHIP_ITEM_SIZE = 90
SLOT_SIZE_PX = 92

MAKE_IMAGE_X = (SCREEN_WIDTH - IMG_SIZE_MAKE[0]) // 2
MAKE_IMAGE_Y = (SCREEN_HEIGHT - IMG_SIZE_MAKE[1]) // 2

# 작은 제작
MAKE2_IMAGE_X = (SCREEN_WIDTH - IMG_SIZE_MAKE2[0]) // 2 - 310
MAKE2_IMAGE_Y = (SCREEN_HEIGHT - IMG_SIZE_MAKE2[1]) // 2

# 제작창 인벤
INVEN_IMAGE_X = (SCREEN_WIDTH - IMG_SIZE_INVEN[0]) // 2 + 280
INVEN_IMAGE_Y = (SCREEN_HEIGHT - IMG_SIZE_INVEN[1]) // 2

# 아이콘 인벤
CENTERED_INV_X = (SCREEN_WIDTH - IMG_SIZE_INVEN[0]) // 2 
INV_CENTER_SHIFT_X = CENTERED_INV_X - INVEN_IMAGE_X
INV_DRAW_Y = INVEN_IMAGE_Y

# 우주선 제작창
SPACESHIP_MAKE_IMAGE_X = (SCREEN_WIDTH - IMG_SIZE_SPACESHIP_MAKE[0]) // 2
SPACESHIP_MAKE_IMAGE_Y = (SCREEN_HEIGHT - IMG_SIZE_SPACESHIP_MAKE[1]) // 2

# 사전
DIC_IMAGE_X = (SCREEN_WIDTH - IMG_SIZE_DIC[0]) // 2
DIC_IMAGE_Y = (SCREEN_HEIGHT - IMG_SIZE_DIC[1]) // 2

# 아이콘
ICON_MARGIN = 10
DIC_ICON_X = SCREEN_WIDTH - ICON_MARGIN - IMG_SIZE_ICON[0]
DIC_ICON_Y = ICON_MARGIN
BAG_ICON_X = DIC_ICON_X - IMG_SIZE_ICON[0]
BAG_ICON_Y = ICON_MARGIN

CLICK_AREA = pygame.Rect(850, 100, 300, 380) 
OUTSIDE_DOOR_AREA = pygame.Rect(400, 400, 400, 300) 
OUTSIDE_MAKE_AREA = pygame.Rect(10, 340, 490, 350) 
TREE_AREA = pygame.Rect(840, 430, 120, 290) 
DIC_AREA = pygame.Rect(250, 480, 250, 100)
SPACESHIP_AREA = pygame.Rect(900, 600, 280, 100)
STAGE1_AREA = pygame.Rect(100, 500, 300, 200)
MAKE_BUTTON_AREA = pygame.Rect(420, 260, 115, 115)

DIC_ICON_AREA = pygame.Rect(DIC_ICON_X, DIC_ICON_Y, IMG_SIZE_ICON[0], IMG_SIZE_ICON[1])
BAG_ICON_AREA = pygame.Rect(BAG_ICON_X, BAG_ICON_Y, IMG_SIZE_ICON[0], IMG_SIZE_ICON[1])

SPACESHIP_DROP_AREA = pygame.Rect(
    SPACESHIP_MAKE_IMAGE_X + 50, 
    SPACESHIP_MAKE_IMAGE_Y + 50, 
    500, 
    500
)

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

SPACESHIP_SLOT_POSITIONS = []
SPACESHIP_SLOT_RECTS = []
SPACESHIP_X_REL_COORDS = [55, 188, 321, 454]
SPACESHIP_Y_REL_COORDS = [55, 188, 321, 454]

SPACESHIP_REQUIREMENTS = {
    'spaceship-roof': 4,
    'spaceship-side': 4,
    'fuel tank': 7,
}
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
MAX_DIC_PAGES = 11
GATHER_DURATION = 3000

PULSATE_SPEED = 0.003
PULSATE_MIN_SCALE = 0.9
PULSATE_MAX_SCALE = 1.1

# 레시피
RECIPES = [
    {
        'recipe':[None, 'wood', None,
                  None, 'wood', None,
                  None, 'wood', None],
        'result':'stick'
    },
    {
        'recipe':[None, None, None,
                  None, 'fossil', 'fossil',
                  None, None, None],
        'result':'fuel'
    },
    {
        'recipe':[None, None, None,
                  'stone','stone','fire',
                  None, None, None],
        'result':'steel'
    },
    {
        'recipe':['steel', 'steel', 'steel',
                  None, 'stick', None,
                  None, 'stick', None],
        'result':'hammer'
    },
    {
        'recipe':['steel', 'steel', 'steel',
                  None, 'stick', None,
                  None, 'stick', None],
        'result':'axe'
    },
    {
        'recipe':[None, None, None,
                  None, 'steel', None,
                  None, 'steel', None],
        'result':'screw'
    },
    {
        'recipe':[None, None, None,
                  'steel', 'fuel', 'steel',
                  None, 'steel', None],
        'result':'fuel tank'
    },
    {
        'recipe':[None, 'soil', None,
                  'soil', 'fire', 'soil',
                  None, 'soil', None],
        'result':'glass'
    },
    {
        'recipe':[None, None, None,
                  None, 'glass', 'glass',
                  None, 'glass', 'glass'],
        'result':'window-piece'
    },
    {
        'recipe':['stick', None, 'stick',
                  'stick', 'stick', 'stick',
                  'stick', None, 'stick'],
        'result':'ladder'
    },
    {
        'recipe':[None, None, None,
                  None, None, None,
                  None, None, None],
        'result':None
    }
]