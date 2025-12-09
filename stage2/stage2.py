import pygame
import os
import math 
from collections import Counter

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW=(255,255,0)

pygame.init()
pygame.display.set_caption("KKANDDABBIA!")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'kkanddabbia')
if not os.path.isdir(assets_path):
    assets_path = current_path 

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 30)
small_font_40 = pygame.font.Font(None, 40)
micro_font=pygame.font.Font(None, 24)

def safe_load_image(filename, size=None, convert_alpha=True):
    path = os.path.join(assets_path, filename)
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        if convert_alpha:
            img = pygame.image.load(path).convert_alpha()
        else:
            img = pygame.image.load(path).convert()
        
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except (pygame.error, FileNotFoundError) as e:
        placeholder = pygame.Surface(size or (100, 100))
        placeholder.fill(RED)
        if convert_alpha:
            placeholder.set_colorkey(RED)
        return placeholder


#########배경##########

start_background_image = safe_load_image('outside.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), False)
current_map = "outside1"
background_image = safe_load_image('inside.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), False)
second_background_image = safe_load_image('outside2.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), False)
new_background_image = safe_load_image('2to3.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), False)


##########사람 애니메이션###########


PLAYER_SIZE = (100, 100) 
ANIMATION_SPEED = 6
current_frame_index = 0
animation_counter = 0

BAG_FRAMES = ['person_bag1.png', 'person_bag2.png', 'person_bag3.png']
IN_FRAMES = ['person_in1.png', 'person_in2.png', 'person_in3.png']
TREE_FRAMES=['person_tree1.png', 'person_tree2.png']

all_animations = {}

def load_animation_set(frame_names, set_name):
    right_frames = []
    left_frames = []
    
    for name in frame_names:
        img = safe_load_image(name, PLAYER_SIZE, True) 
        
        if img.get_at((0, 0)) == RED and img.get_size() == PLAYER_SIZE:
             placeholder_img = img
             right_frames.append(placeholder_img)
             left_frames.append(placeholder_img)
        else:
            right_frames.append(img)
            left_frames.append(pygame.transform.flip(img, True, False))
            
    if not right_frames:
        placeholder = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
        placeholder.fill((255, 0, 0, 128))
        right_frames.append(placeholder)
        left_frames.append(placeholder)
        
    stand_index = min(1, len(right_frames) - 1)
    stand_right = right_frames[stand_index]
    stand_left = left_frames[stand_index]
        
    all_animations[set_name] = {
        'right': right_frames,
        'left': left_frames,
        'stand_right': stand_right,
        'stand_left': stand_left
    }

load_animation_set(BAG_FRAMES, 'bag')
load_animation_set(IN_FRAMES, 'in')
load_animation_set(TREE_FRAMES, 'tree')

if all_animations.get('bag'):
    person_image = all_animations['bag']['stand_right']
else:
    person_image = pygame.Surface(PLAYER_SIZE)


##############아이콘###############


ICON_SIZE=80
ICON_MARGIN=10

icon_bag_image=safe_load_image('icon_bag.png', (ICON_SIZE, ICON_SIZE))
icon_dic_image=safe_load_image('icon_dic.png', (ICON_SIZE, ICON_SIZE))

DIC_ICON_X=SCREEN_WIDTH-ICON_MARGIN-ICON_SIZE
DIC_ICON_Y=ICON_MARGIN
DIC_ICON_AREA=pygame.Rect(DIC_ICON_X, DIC_ICON_Y, ICON_SIZE, ICON_SIZE)

BAG_ICON_X=DIC_ICON_X-ICON_SIZE
BAG_ICON_Y=ICON_MARGIN
BAG_ICON_AREA=pygame.Rect(BAG_ICON_X, BAG_ICON_Y, ICON_SIZE, ICON_SIZE)


#################################


make_image = safe_load_image('make.png', (600, 600))
make_image_x = (SCREEN_WIDTH - make_image.get_width()) // 2
make_image_y = (SCREEN_HEIGHT - make_image.get_height()) // 2

make2_image = safe_load_image('make2.PNG', (546, 380))
make2_image_x = (SCREEN_WIDTH - make2_image.get_width()) // 2 - 310
make2_image_y = (SCREEN_HEIGHT - make2_image.get_height()) // 2

inven_image = safe_load_image('inventory.PNG', (600, 600))
inven_image_x = (SCREEN_WIDTH - inven_image.get_width()) // 2 + 280
inven_image_y = (SCREEN_HEIGHT - inven_image.get_height()) // 2

INV_DRAW_Y = inven_image_y
CENTERED_INV_X = (SCREEN_WIDTH - inven_image.get_width()) // 2 
INV_CENTER_SHIFT_X = CENTERED_INV_X - inven_image_x

make_outside_image = safe_load_image('make_outside.png', (600, 600))
make_outside_image_x = (SCREEN_WIDTH - make_outside_image.get_width()) // 2
make_outside_image_y = (SCREEN_HEIGHT - make_outside_image.get_height()) // 2

spaceship_make_image = safe_load_image('spaceship_make.png', (600, 600))
spaceship_make_image_x = (SCREEN_WIDTH - spaceship_make_image.get_width()) // 2
spaceship_make_image_y = (SCREEN_HEIGHT - spaceship_make_image.get_height()) // 2

dic_image = safe_load_image('dic.png', (600, 600))
dic_image_x = (SCREEN_WIDTH - dic_image.get_width()) // 2
dic_image_y = (SCREEN_HEIGHT - dic_image.get_height()) // 2

person_x = 100
person_y = 630
person_speed = 5
person_direction_right = True

open_door = False 
dic_open = False 
is_crafting_open = False 
is_spaceship_crafting_open = False 

done = False
game_over = False

is_player_walking_into_spaceship = False 
is_flying_animation_active = False       
fly_animation_start_time = 0             

fly_spaceship_image = safe_load_image('fly_spaceship.png', (250, 200), True)

#깜박임
pulsate_time_start = pygame.time.get_ticks()
PULSATE_SPEED = 0.003 
PULSATE_MIN_SCALE = 0.9
PULSATE_MAX_SCALE = 1.1

SPACESHIP_REQUIREMENTS = {
    'spaceship-roof': 4,
    'spaceship-side': 4,
    'fuel tank': 7,
}
MAX_SPACESHIP_PARTS = sum(SPACESHIP_REQUIREMENTS.values()) # 총 15개
spaceship_assembly_storage = [] 

is_tree_pressing = False
tree_press_start_time = 0
GATHER_DURATION = 3000

DROPPED_ITEMS = []

CLICK_AREA = pygame.Rect(850, 100, 300, 380) 
OUTSIDE_DOOR_AREA = pygame.Rect(400, 400, 400, 300) 
OUTSIDE_MAKE_AREA = pygame.Rect(10, 340, 490, 350) 
TREE_AREA = pygame.Rect(840, 430, 120, 290) 
DIC_AREA = pygame.Rect(250, 480, 250, 100)
SPACESHIP_AREA = pygame.Rect(900, 600, 280, 100)
STAGE1_AREA=pygame.Rect(100,500, 300, 200)

is_fading_out=False
player_alpha=255
FADE_SPEED=5

# 우주선 제작 창 드롭 영역
SPACESHIP_DROP_AREA = pygame.Rect(
    spaceship_make_image_x + 50, 
    spaceship_make_image_y + 50, 
    500, 
    500
)

MAKE_BUTTON_AREA = pygame.Rect(420, 260, 115, 115)

is_drag = False
drag_item = None
drag_item_original = None
current_dic_page = 1 
MAX_DIC_PAGES = 11 

drag_offset_x = 0
drag_offset_y = 0


##############인벤토리 정렬##############


MAX_STACK_SIZE = 10

def get_stacked_inventory(flat_inventory):
    counts = Counter(flat_inventory)
    stacked_inventory = []
    sorted_item_names = sorted(counts.keys())
    for item_name in sorted_item_names:
        total_count = counts[item_name]
        if item_name in item_images:
            while total_count > 0:
                stack_count = min(total_count, MAX_STACK_SIZE)
                stacked_inventory.append({'name': item_name, 'count': stack_count})
                total_count -= stack_count
    return stacked_inventory

def check_spaceship_condition(inventory):
    return 'spaceship' in inventory

#################아이템################


ITEM_SIZE = 70
SPACESHIP_ITEM_SIZE = 90

inventory = (['fire']*1 + ['stone']*15 + 
             ['spaceship'] * 1 + 
             ['spaceship-side'] * 4 + 
             ['spaceship-roof'] * 4 + 
             ['fuel tank'] * 7)

crafting_table = [None] * 9

item_images = {}

DIC_PAGES_NAMES = [f'dic_p{i}' for i in range(1, MAX_DIC_PAGES + 1)]

def load_item(name, filename):
    size = (ITEM_SIZE, ITEM_SIZE)
    convert_alpha = True
    
    if name.startswith('dic_p'):
        size = (dic_image.get_width() - 150, dic_image.get_height() - 40)
        convert_alpha = False
        
    item_images[name] = safe_load_image(filename, size, convert_alpha)

#아이템
load_item('fire', 'fire.png')
load_item('stone', 'stone.png')
load_item('soil', 'soil.png')
load_item('wood', 'wood.png')
load_item('stick', 'stick.png')
load_item('glass', 'glass.png')
load_item('window', 'window.png')
load_item('screw', 'screw.png')
load_item('steel', 'steel.png')
load_item('axe', 'axe.png')
load_item('fossil', 'fossil.png')
load_item('fuel tank', 'fuel tank.png')
load_item('fuel', 'fuel.png')
load_item('hammer', 'hammer.png')
load_item('ladder', 'ladder.png')
load_item('window-piece', 'window_piece.png')
load_item('steel', 'steel.png')

#우주선 조각
spaceship_display_image = safe_load_image('spaceship.png', (190, 100))
SPACESHIP_COMPLETED_IMAGE = safe_load_image('spaceship.png', (250, 200))
load_item('spaceship', 'spaceship.png')
load_item('spaceship-side', 'spaceship_side_piece.png')
load_item('spaceship-side-piece', 'spaceship_side_1_9.png')
load_item('spaceship-roof', 'spaceship_roof_piece.png') 
load_item('spaceship-roof-piece', 'spaceship_roof_1_4.png')

for i in range(1, MAX_DIC_PAGES + 1):
    load_item(f'dic_p{i}', f'dic_{i}.jpg')


##################일반 제작 조합#################


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


#################제작창 관련 위치################


INVENTORY_SLOT_POSITIONS = []
INVENTORY_SLOT_RECTS = []

INV_X_REL_COORDS = [50, 142, 234, 326, 418, 512]
INV_Y_REL_COORDS = [50, 142, 234, 326, 418, 512]

for rel_y in INV_Y_REL_COORDS:
    for rel_x in INV_X_REL_COORDS:
        absolute_x = inven_image_x + rel_x - (ITEM_SIZE // 2) + 20
        absolute_y = inven_image_y + rel_y - (ITEM_SIZE // 2) + 20
        INVENTORY_SLOT_POSITIONS.append((absolute_x, absolute_y))
        INVENTORY_SLOT_RECTS.append(pygame.Rect(absolute_x, absolute_y, ITEM_SIZE, ITEM_SIZE))


CRAFT_SLOT_POSITIONS = []
CRAFT_SLOT_RECTS = []

CRAFT_X_POSITIONS = [51, 151, 251]
CRAFT_Y_POSITIONS = [56, 154, 255]

for rel_y in CRAFT_Y_POSITIONS:
    for rel_x in CRAFT_X_POSITIONS:
        absolute_x = make2_image_x + rel_x
        absolute_y = make2_image_y + rel_y
        CRAFT_SLOT_POSITIONS.append((absolute_x, absolute_y))
        CRAFT_SLOT_RECTS.append(pygame.Rect(absolute_x, absolute_y, ITEM_SIZE, ITEM_SIZE))


SPACESHIP_X_REL_COORDS = [55, 188, 321, 454] 
SPACESHIP_Y_REL_COORDS = [55, 188, 321, 454] 
SLOT_SIZE_PX = 92 

SLOT_RELATIVE_COORDS = []
for rel_y in SPACESHIP_Y_REL_COORDS:
    for rel_x in SPACESHIP_X_REL_COORDS:
        SLOT_RELATIVE_COORDS.append((rel_x, rel_y))

if len(SLOT_RELATIVE_COORDS) > MAX_SPACESHIP_PARTS:
    SLOT_RELATIVE_COORDS.pop()


SPACESHIP_SLOT_POSITIONS = []
SPACESHIP_SLOT_RECTS = []

for rel_x, rel_y in SLOT_RELATIVE_COORDS:
    absolute_x = spaceship_make_image_x + rel_x
    absolute_y = spaceship_make_image_y + rel_y
    
    SPACESHIP_SLOT_POSITIONS.append((absolute_x, absolute_y))
    SPACESHIP_SLOT_RECTS.append(pygame.Rect(absolute_x, absolute_y, SLOT_SIZE_PX, SLOT_SIZE_PX))
    
ASSEMBLED_SLOT_MAP = {} 


#########메인루프#########


while not done:
    
    current_time = pygame.time.get_ticks()

    if is_fading_out:
        player_alpha-=FADE_SPEED
        if player_alpha<=0:
            player_alpha=0
            is_fading_out=False

    
    spaceship_part_count = len(spaceship_assembly_storage)
    is_completed = (spaceship_part_count == MAX_SPACESHIP_PARTS)
    
    
    if is_player_walking_into_spaceship:
        active_set = all_animations['in']
    elif current_map=="outside1" and is_tree_pressing:
        active_set=all_animations['tree']
    elif current_map == "inside":
        active_set = all_animations['in']
    elif current_map in ["outside1", "outside2"]:
        active_set = all_animations['bag']
    else:
        active_set = all_animations['bag']
    
    time_factor = (current_time - pulsate_time_start) * PULSATE_SPEED
    scale_offset = (math.sin(time_factor) + 1) / 2
    current_scale = PULSATE_MIN_SCALE + scale_offset * (PULSATE_MAX_SCALE - PULSATE_MIN_SCALE)


    if current_map == "outside1" and is_tree_pressing:
        if current_time - tree_press_start_time >= GATHER_DURATION:
            wood_drop_x = TREE_AREA.x + TREE_AREA.width // 2 - ITEM_SIZE // 2
            wood_drop_y = person_y + person_image.get_height()
            DROPPED_ITEMS.append({
                'item_name': 'wood',
                'rect': pygame.Rect(wood_drop_x, wood_drop_y, ITEM_SIZE, ITEM_SIZE)
            })
            is_tree_pressing = False
            tree_press_start_time = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.MOUSEBUTTONUP and not game_over and not is_flying_animation_active and not is_player_walking_into_spaceship:
            
            if current_map == "outside1" and is_tree_pressing:
                is_tree_pressing = False
                tree_press_start_time = 0
            
            mouse_pos = pygame.mouse.get_pos()
            
            if is_drag:
                dropped_in_crafting = False
                dropped_in_spaceship = False 
                dropped_on_spaceship_area = False 
                
                #일반 제작창
                if is_crafting_open:
                    for i in range(len(CRAFT_SLOT_RECTS)):
                        if CRAFT_SLOT_RECTS[i].collidepoint(mouse_pos) and crafting_table[i] is None:
                            crafting_table[i] = drag_item
                            dropped_in_crafting = True
                            break

                #외부 제작창
                if is_spaceship_crafting_open and not dropped_in_crafting:
                    if SPACESHIP_DROP_AREA.collidepoint(mouse_pos):
                        item_name = drag_item
                        required_count = SPACESHIP_REQUIREMENTS.get(item_name, 0)
                        current_count = spaceship_assembly_storage.count(item_name)
                        
                        if required_count > 0 and current_count < required_count:
                            spaceship_assembly_storage.append(item_name)
                            dropped_in_spaceship = True
                            
                            assigned_slots = sum(ASSEMBLED_SLOT_MAP.values(), [])
                            for slot_index in range(MAX_SPACESHIP_PARTS):
                                if slot_index not in assigned_slots:
                                    if item_name not in ASSEMBLED_SLOT_MAP:
                                        ASSEMBLED_SLOT_MAP[item_name] = []
                                    ASSEMBLED_SLOT_MAP[item_name].append(slot_index)
                                    break
                            
                #우주선 제작
                if (open_door or is_spaceship_crafting_open) and not dropped_in_crafting and not dropped_in_spaceship:
                    if current_map == "outside2" and SPACESHIP_AREA.collidepoint(mouse_pos):
                        item_name = drag_item
                        required_count = SPACESHIP_REQUIREMENTS.get(item_name, 0)
                        current_count = spaceship_assembly_storage.count(item_name)
                        
                        if required_count > 0 and current_count < required_count:
                            spaceship_assembly_storage.append(item_name)
                            dropped_on_spaceship_area = True

                            assigned_slots = sum(ASSEMBLED_SLOT_MAP.values(), [])
                            for slot_index in range(MAX_SPACESHIP_PARTS):
                                if slot_index not in assigned_slots:
                                    if item_name not in ASSEMBLED_SLOT_MAP:
                                        ASSEMBLED_SLOT_MAP[item_name] = []
                                    ASSEMBLED_SLOT_MAP[item_name].append(slot_index)
                                    break
                
                #드롭 실패
                if not dropped_in_crafting and not dropped_in_spaceship and not dropped_on_spaceship_area:
                    inventory.append(drag_item)
                
                is_drag = False
                drag_item = None
                drag_item_original = None
                drag_offset_x, drag_offset_y = 0, 0


        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not is_flying_animation_active and not is_player_walking_into_spaceship:
            mouse_pos = pygame.mouse.get_pos()
            
            is_icon_clicked = False
            
            #사전 아이콘
            if DIC_ICON_AREA.collidepoint(mouse_pos):
                dic_open = not dic_open
                if dic_open:
                    open_door = False
                    is_crafting_open = False
                    is_spaceship_crafting_open = False 
                is_icon_clicked = True
            
            #가방 아이콘
            elif BAG_ICON_AREA.collidepoint(mouse_pos):
                
                if open_door and not is_crafting_open:
                    open_door = False
                else:
                    open_door = True 
                
                is_crafting_open = False 
                is_spaceship_crafting_open = False 
                    
                if open_door:
                    dic_open = False
                
                is_icon_clicked = True
            
            if is_icon_clicked:
                if is_drag:
                    inventory.append(drag_item)
                    is_drag = False
                    drag_item = None
                
                continue 

            #사전 페이지
            if dic_open:
                dic_window_rect = dic_image.get_rect(topleft=(dic_image_x, dic_image_y))
                
                if dic_window_rect.collidepoint(mouse_pos):
                    dic_center_x = dic_window_rect.centerx
                    
                    if mouse_pos[0] < dic_center_x:
                        if current_dic_page > 1:
                            current_dic_page -= 1
                    else:
                        if current_dic_page < MAX_DIC_PAGES:
                            current_dic_page += 1
                    continue

                else:
                    dic_open = False
            
            #창 닫기
            elif open_door:
                inven_window_rect = inven_image.get_rect(topleft=(inven_image_x, inven_image_y))
                
                hitbox_shift_x = INV_CENTER_SHIFT_X if not is_crafting_open else 0

                if is_crafting_open:
                    make_window_rect = make2_image.get_rect(topleft=(make2_image_x, make2_image_y))
                    is_on_window = inven_window_rect.collidepoint(mouse_pos) or make_window_rect.collidepoint(mouse_pos)
                else:
                    temp_rect = inven_window_rect.move(hitbox_shift_x, 0)
                    is_on_window = temp_rect.collidepoint(mouse_pos)
                
                is_on_icon = DIC_ICON_AREA.collidepoint(mouse_pos) or BAG_ICON_AREA.collidepoint(mouse_pos)
                
                if not is_on_window and not is_on_icon:
                    if is_drag:
                        inventory.append(drag_item)
                        is_drag = False
                        drag_item = None
                    open_door = False
                    is_crafting_open = False
            
            #창 닫기
            elif is_spaceship_crafting_open:
                spaceship_make_window_rect = spaceship_make_image.get_rect(topleft=(spaceship_make_image_x, spaceship_make_image_y))
                is_on_icon = DIC_ICON_AREA.collidepoint(mouse_pos) or BAG_ICON_AREA.collidepoint(mouse_pos)

                if not spaceship_make_window_rect.collidepoint(mouse_pos) and \
                   not is_on_icon:
                    is_spaceship_crafting_open = False
            
            if not open_door and not dic_open and not is_spaceship_crafting_open:
                
                if current_map == "outside1":
                    if TREE_AREA.collidepoint(mouse_pos):
                        if not is_tree_pressing:
                            is_tree_pressing = True
                            tree_press_start_time = pygame.time.get_ticks()
                        continue

                    item_collected = False
                    for i in range(len(DROPPED_ITEMS) - 1, -1, -1):
                        item = DROPPED_ITEMS[i]
                        if item['rect'].collidepoint(mouse_pos):
                            inventory.append(item['item_name'])
                            DROPPED_ITEMS.pop(i)
                            item_collected = True
                            break
                    if item_collected:
                        continue

                    if OUTSIDE_DOOR_AREA.collidepoint(mouse_pos):
                        current_map = "inside"
                        person_x = 100
                        current_frame_index = 0
                        animation_counter = 0
                        continue

                    if STAGE1_AREA.collidepoint(mouse_pos):
                        if not is_fading_out:
                            is_fading_out=True
                            player_alpha=255
                        continue
                        

                elif current_map == "inside":
                    
                    if DIC_AREA.collidepoint(mouse_pos):
                        dic_open = not dic_open
                        if dic_open:
                            open_door = False
                            is_crafting_open = False
                            is_spaceship_crafting_open = False
                        continue

                    if CLICK_AREA.collidepoint(mouse_pos):
                        open_door = True
                        is_crafting_open = True 
                        dic_open = False
                        is_spaceship_crafting_open = False
                        continue

                
                elif current_map == "outside2":
                    
                    if OUTSIDE_MAKE_AREA.collidepoint(mouse_pos):
                        open_door = True
                        is_crafting_open = True 
                        dic_open = False
                        is_spaceship_crafting_open = False
                        continue
                        
                    #stage 3으로
                    if SPACESHIP_AREA.collidepoint(mouse_pos) and is_completed:
                        open_door = False
                        is_crafting_open = False 
                        dic_open = False
                        is_spaceship_crafting_open = False
                        
                        is_player_walking_into_spaceship = True
                        person_x = 0
                        person_y = 500
                        person_direction_right = True
                        current_frame_index = 0
                        animation_counter = 0
                        continue
                        
                    #우주선 조각 창 열기
                    if SPACESHIP_AREA.collidepoint(mouse_pos) and check_spaceship_condition(inventory) and not is_completed:
                        is_spaceship_crafting_open = True
                        open_door = False
                        is_crafting_open = False 
                        dic_open = False
                        continue

            
            if (open_door or is_spaceship_crafting_open) and not dic_open:
                
                hitbox_shift_x = INV_CENTER_SHIFT_X if open_door and not is_crafting_open else 0

                #M버튼
                if open_door and is_crafting_open and MAKE_BUTTON_AREA.collidepoint(mouse_pos):
                    found_recipe = False
                    for recipe_data in RECIPES:
                        if crafting_table == recipe_data['recipe']:
                            if recipe_data['result'] is not None:
                                for item_name in crafting_table:
                                    if item_name is not None:
                                        try:
                                            inventory.remove(item_name)
                                        except ValueError:
                                            pass

                                inventory.append(recipe_data['result'])
                            
                            crafting_table=[None]*9
                            found_recipe=True
                            break
                        
                    if not found_recipe:
                        game_over = True
                        open_door = False
                        is_crafting_open = False
                    continue
                    
                if not is_drag:
                    stacked_inventory=get_stacked_inventory(inventory)
                    
                    #드래그
                    for i in range(min(len(stacked_inventory), len(INVENTORY_SLOT_RECTS))):
                        temp_rect = INVENTORY_SLOT_RECTS[i].move(hitbox_shift_x, 0)
                        if is_spaceship_crafting_open:
                            temp_rect = INVENTORY_SLOT_RECTS[i].move(0, 0) 
                            
                        if temp_rect.collidepoint(mouse_pos):
                            item_name=stacked_inventory[i]['name']

                            try:
                                flat_index=inventory.index(item_name)

                                is_drag=True
                                drag_item=inventory[flat_index]
                                inventory.pop(flat_index)
                                drag_item_original=f"inventory_slot_{i}"

                                drag_offset_x=mouse_pos[0]-temp_rect.x
                                drag_offset_y=mouse_pos[1]-temp_rect.y
                            except ValueError:
                                pass

                            break

                    
                    #드래그
                    if not is_drag and open_door and is_crafting_open:
                        for i in range(len(crafting_table)):
                            if crafting_table[i] is not None and CRAFT_SLOT_RECTS[i].collidepoint(mouse_pos):
                                drag_item = crafting_table[i]
                                drag_item_original = f"crafting_slot_{i}"
                                crafting_table[i] = None
                                is_drag = True
                                drag_offset_x = mouse_pos[0] - CRAFT_SLOT_RECTS[i].x
                                drag_offset_y = mouse_pos[1] - CRAFT_SLOT_RECTS[i].y
                                break
    

########메인루프@#########
    

    if game_over:
        screen.fill(BLACK)
        game_over_text = font.render("GAME OVER", True, RED)
        sub_text = small_font_40.render("Press ESC to Quit", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(sub_text, (SCREEN_WIDTH // 2 - sub_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    #stage3가는 애니
    elif is_flying_animation_active:
        screen.blit(new_background_image, (0, 0))
        
        elapsed_time = current_time - fly_animation_start_time

    #stage3 가는 애니
    elif is_player_walking_into_spaceship:
        screen.blit(new_background_image, (0, 0))
        
        person_x += person_speed
        person_y=590
        is_moving = True
        person_direction_right = True

        animation_counter += 1
        if animation_counter >= ANIMATION_SPEED:
            animation_counter = 0
            if active_set and active_set['right']:
                current_frame_index = (current_frame_index + 1) % len(active_set['right'])
            else:
                current_frame_index = 0
        
        person_image = active_set['right'][current_frame_index] if active_set else person_image
        
        screen.blit(person_image, (person_x, person_y))
        
        if person_x >= SCREEN_WIDTH - person_image.get_width():
            is_player_walking_into_spaceship = False
            is_flying_animation_active = True
            fly_animation_start_time = pygame.time.get_ticks()

    
    else:
        keys = pygame.key.get_pressed()
        is_moving = False

        if not open_door and not dic_open and not is_spaceship_crafting_open and not is_tree_pressing:
            if keys[pygame.K_a]:
                person_x -= person_speed
                person_direction_right = False
                is_moving = True
            elif keys[pygame.K_d]:
                person_x += person_speed
                person_direction_right = True
                is_moving = True

        if is_moving or is_tree_pressing:
            animation_counter += 1
            if animation_counter >= ANIMATION_SPEED:
                animation_counter = 0
                if active_set and active_set['right']:
                    current_frame_index = (current_frame_index + 1) % len(active_set['right'])
                else:
                     current_frame_index = 0
            
            if person_direction_right:
                person_image = active_set['right'][current_frame_index] if active_set else person_image
            else:
                person_image = active_set['left'][current_frame_index] if active_set else person_image
        else:
            animation_counter = 0
            current_frame_index = 0
            if person_direction_right:
                person_image = active_set['stand_right'] if active_set else person_image
            else:
                person_image = active_set['stand_left'] if active_set else person_image
                
        if current_map == "outside1":
            if person_x < 0:
                person_x = 0
            elif person_x > SCREEN_WIDTH - person_image.get_width():
                current_map = "outside2"
                person_x = 5
                current_frame_index = 0
                animation_counter = 0

            screen.blit(start_background_image, (0, 0))
            temp_image=person_image.copy()
            temp_image.set_alpha(player_alpha)
            screen.blit(temp_image, (person_x, person_y))
            
            for item in DROPPED_ITEMS:
                item_draw = item_images.get(item['item_name'])
                if item_draw:
                    screen.blit(item_draw, item['rect'])
            
            if is_tree_pressing:
                elapsed = pygame.time.get_ticks() - tree_press_start_time
                progress = min(1.0, elapsed / GATHER_DURATION)
                bar_width = 100
                bar_height = 10
                bar_x = TREE_AREA.x + TREE_AREA.width // 2 - bar_width // 2
                bar_y = TREE_AREA.y - bar_height - 5
                pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
                pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, bar_width * progress, bar_height))


        elif current_map == "inside":
            if person_x < 0:
                current_map = "outside1"
                person_x = SCREEN_WIDTH - person_image.get_width() - 5
                current_frame_index = 0
                animation_counter = 0

            elif person_x > SCREEN_WIDTH - person_image.get_width():
                person_x = SCREEN_WIDTH - person_image.get_width()
            
            screen.blit(background_image, (0, 0))
            screen.blit(person_image, (person_x, person_y))

            
        elif current_map == "outside2":
            if person_x < 0:
                current_map = "outside1"
                person_x = SCREEN_WIDTH - person_image.get_width() - 5
                current_frame_index = 0
                animation_counter = 0

            elif person_x > SCREEN_WIDTH - person_image.get_width():
                person_x = SCREEN_WIDTH - person_image.get_width()
            
            screen.blit(second_background_image, (0, 0))
            screen.blit(person_image, (person_x, person_y))
            
            if check_spaceship_condition(inventory):
                
                #우주선 깜빡깜빡
                if is_completed:
                    
                    original_w, original_h = SPACESHIP_COMPLETED_IMAGE.get_size()
                    new_w = int(original_w * current_scale)
                    new_h = int(original_h * current_scale)
                    
                    scaled_image = pygame.transform.scale(SPACESHIP_COMPLETED_IMAGE, (new_w, new_h))
                    
                    center_x = SPACESHIP_AREA.x + SPACESHIP_AREA.width // 2
                    top_y = SPACESHIP_AREA.y - new_h-50
                    draw_x = center_x - new_w // 2
                    draw_y = top_y
                    
                    screen.blit(scaled_image, (draw_x, draw_y))
                    
                #우주선 게이지
                gauge_width = 280
                gauge_height = 20
                
                gauge_x = SPACESHIP_AREA.x
                gauge_y = SPACESHIP_AREA.y + SPACESHIP_AREA.height + 10 
                
                gauge_rect_outer = pygame.Rect(gauge_x, gauge_y, gauge_width, gauge_height)
                pygame.draw.rect(screen, BLACK, gauge_rect_outer, 3) 

                progress_ratio = min(1.0, spaceship_part_count / MAX_SPACESHIP_PARTS) 
                filled_width = int(gauge_width * progress_ratio)
                gauge_color = (0,255,0) if is_completed else (255,0,0)

                gauge_rect_filled = pygame.Rect(
                    gauge_x, 
                    gauge_y, 
                    filled_width, 
                    gauge_height
                )
                pygame.draw.rect(screen, gauge_color, gauge_rect_filled) 
                
                progress_text = small_font.render(f"{spaceship_part_count}/{MAX_SPACESHIP_PARTS}", True, WHITE)
                text_x = gauge_x + gauge_width // 2 - progress_text.get_width() // 2
                text_y = gauge_y + gauge_height // 2 - progress_text.get_height() // 2
                screen.blit(progress_text, (text_x, text_y))


        if open_door and not dic_open and not is_spaceship_crafting_open:
            
            if is_crafting_open:
                current_inv_x = inven_image_x
                current_shift_x = 0
            else:
                current_inv_x = CENTERED_INV_X
                current_shift_x = INV_CENTER_SHIFT_X
            
            #제작 창
            if is_crafting_open:
                screen.blit(make2_image, (make2_image_x, make2_image_y))

            #인벤 창
            screen.blit(inven_image, (current_inv_x, INV_DRAW_Y))
            
            stacked_inventory=get_stacked_inventory(inventory)

            #인벤 슬롯
            have_num = min(len(stacked_inventory), len(INVENTORY_SLOT_POSITIONS)) 
            for i in range(have_num):
                slot_x, slot_y = INVENTORY_SLOT_POSITIONS[i]
                
                draw_x = slot_x + current_shift_x
                draw_y = slot_y
                
                item_data=stacked_inventory[i]
                item_name = item_data['name']
                item_count=item_data['count']
                item_draw = item_images.get(item_name)

                if item_draw:
                    screen.blit(item_draw, (draw_x, draw_y))

                    count_text=micro_font.render(f"x{item_count}", True, YELLOW)
                    text_x=draw_x+ITEM_SIZE-count_text.get_width()-5
                    text_y=draw_y+ITEM_SIZE-count_text.get_height()-5
                    screen.blit(count_text, (text_x, text_y))

            #제작 슬롯
            if is_crafting_open:
                for i in range(len(crafting_table)):
                    item_name = crafting_table[i]
                    if item_name is not None:
                        slot_x, slot_y = CRAFT_SLOT_POSITIONS[i]
                        item_draw = item_images.get(item_name)
                        if item_draw:
                            screen.blit(item_draw, (slot_x, slot_y))
                            
        #우주선 제작 창
        if is_spaceship_crafting_open and not open_door and not dic_open:
            screen.blit(spaceship_make_image, (spaceship_make_image_x, spaceship_make_image_y))

            for item_name, slot_indices in ASSEMBLED_SLOT_MAP.items():
                item_draw_original = item_images.get(item_name)
                
                if item_draw_original:

                    item_draw_scaled = pygame.transform.scale(item_draw_original, (SPACESHIP_ITEM_SIZE, SPACESHIP_ITEM_SIZE))
                    
                    for slot_index in slot_indices:
                        if slot_index < len(SPACESHIP_SLOT_POSITIONS):
                            slot_x, slot_y = SPACESHIP_SLOT_POSITIONS[slot_index]
                            
                            offset = (SLOT_SIZE_PX - SPACESHIP_ITEM_SIZE) // 2
                            draw_x = slot_x + offset
                            draw_y = slot_y + offset
                            
                            screen.blit(item_draw_scaled, (draw_x, draw_y))

        #사전 창
        if dic_open and not open_door and not is_spaceship_crafting_open:
            screen.blit(dic_image, (dic_image_x, dic_image_y))
            
            dic_page_name = f'dic_p{current_dic_page}'
            dic_page_image = item_images.get(dic_page_name)
            
            if dic_page_image:
                page_x = dic_image_x + (dic_image.get_width() - dic_page_image.get_width()) // 2
                page_y = dic_image_y + (dic_image.get_height() - dic_image.get_height()) // 2
                screen.blit(dic_page_image, (page_x, page_y))

            page_text = small_font.render(f"{current_dic_page} / {MAX_DIC_PAGES}", True, BLACK)
            screen.blit(page_text, (dic_image_x + dic_image.get_width() / 2 - page_text.get_width() / 2, dic_image_y + dic_image.get_height() - 30))


        #아이콘
        if not is_flying_animation_active and not is_player_walking_into_spaceship:
            screen.blit(icon_bag_image, (BAG_ICON_X, BAG_ICON_Y))
            screen.blit(icon_dic_image, (DIC_ICON_X, DIC_ICON_Y))

        #드래그
        if is_drag and drag_item is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            drag_item_draw = item_images.get(drag_item)

            if drag_item_draw:
                screen.blit(drag_item_draw, (mouse_x - drag_offset_x, mouse_y - drag_offset_y))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()