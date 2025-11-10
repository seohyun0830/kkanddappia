import pygame
import os

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.init()
pygame.display.set_caption("KKANDDABBIA!")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'kkanddabbia')

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 30)
small_font_40 = pygame.font.Font(None, 40)

start_background_image = pygame.image.load(os.path.join(assets_path, 'outside.jpg'))
start_background_image = pygame.transform.scale(start_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

current_map = "outside1"

background_image = pygame.image.load(os.path.join(assets_path, 'inside.jpg'))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

second_background_image = pygame.image.load(os.path.join(assets_path, 'outside2.jpg'))
second_background_image = pygame.transform.scale(second_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


origin_person_image = pygame.image.load(os.path.join(assets_path, 'person.png')).convert()
origin_person_image.set_colorkey(WHITE)
origin_person_image = pygame.transform.scale(origin_person_image, (250, 250))

flip_person_image = pygame.transform.flip(origin_person_image, True, False)
person_image = origin_person_image

make_image = pygame.image.load(os.path.join(assets_path, 'make.png'))
make_image = pygame.transform.scale(make_image, (600, 600))

make_image_x = (SCREEN_WIDTH - make_image.get_width()) // 2
make_image_y = (SCREEN_HEIGHT - make_image.get_height()) // 2

# make2_image 및 inven_image 로드 (새로운 파일명 사용)
make2_image = pygame.image.load(os.path.join(assets_path, 'make2.PNG'))
make2_image = pygame.transform.scale(make2_image, (546, 380))

make2_image_x = (SCREEN_WIDTH - make2_image.get_width()) // 2 - 310
make2_image_y = (SCREEN_HEIGHT - make2_image.get_height()) // 2

inven_image = pygame.image.load(os.path.join(assets_path, 'inventory.PNG'))
inven_image = pygame.transform.scale(inven_image, (600, 600))

inven_image_x = (SCREEN_WIDTH - inven_image.get_width()) // 2 + 280
inven_image_y = (SCREEN_HEIGHT - inven_image.get_height()) // 2 # Y 위치 상향 조정

make_outside_image = pygame.image.load(os.path.join(assets_path, 'make_outside.png'))
make_outside_image = pygame.transform.scale(make_image, (600, 600))

make_outside_image_x = (SCREEN_WIDTH - make_outside_image.get_width()) // 2
make_outside_image_y = (SCREEN_HEIGHT - make_outside_image.get_height()) // 2

dic_image = pygame.image.load(os.path.join(assets_path, 'dic.png'))
dic_image = pygame.transform.scale(dic_image, (600, 600))

dic_image_x = (SCREEN_WIDTH - dic_image.get_width()) // 2
dic_image_y = (SCREEN_HEIGHT - dic_image.get_height()) // 2

person_x = 100
person_y = 500
person_speed = 5
person_direction_right = True

open_door = False

done = False

game_over = False

outside_make_door = False

# 🌟🌟🌟 채집 상태 변수 통일 및 초기화 🌟🌟🌟
is_tree_pressing = False
tree_press_start_time = 0
GATHER_DURATION = 3000

DROPPED_ITEMS = [] # 바닥 아이템 리스트 이름 통일

CLICK_AREA = pygame.Rect(900, 400, 210, 260)
OUTSIDE_DOOR_AREA = pygame.Rect(400, 400, 400, 300)
OUTSIDE_MAKE_AREA = pygame.Rect(70, 355, 270, 370)
TREE_AREA = pygame.Rect(1000, 400, 100, 290)
DIC_AREA = pygame.Rect(70, 500, 250, 80)

MAKE_BUTTON_X = 120
MAKE_BUTTON_Y = 158
MAKE_BUTTON_W = 115
MAKE_BUTTON_H = 115

MAKE_BUTTON_AREA = pygame.Rect(
    make_image_x + MAKE_BUTTON_X,
    make_image_y + MAKE_BUTTON_Y,
    MAKE_BUTTON_W,
    MAKE_BUTTON_H
)

is_drag = False
drag_item = None
drag_item_original = None
dic_open = False

drag_offset_x = 0
drag_offset_y = 0


#################아이템################


ITEM_SIZE = 70

inventory = ['fire', 'stone', 'stone', 'wood', 'stick', 'glass', 'window', 'soil', 'stick', 'glass', 'stone', 'wood'] * 3 # 인벤토리 36칸 채우기

crafting_table = [None] * 9

item_images = {}

def load_item(name, filename):
    try:
        image = pygame.image.load(os.path.join(assets_path, filename))
        image = image.convert_alpha()
        image.set_colorkey(WHITE)
        item_images[name] = pygame.transform.scale(image, (ITEM_SIZE, ITEM_SIZE))
    except pygame.error:
        print(f"Warning: Error loading {filename}. Using placeholder.")
        placeholder = pygame.Surface((ITEM_SIZE, ITEM_SIZE), pygame.SRCALPHA)
        item_images[name] = placeholder

# 모든 아이템 로딩
load_item('fire', 'fire.png')
load_item('stone', 'stone.png')
load_item('soil', 'soil.png')
load_item('wood', 'wood.png')
load_item('stick', 'stick.png')
load_item('glass', 'glass.png')
load_item('window', 'window-piece.png')
load_item('screw', 'screw.png')
load_item('steel', 'steel.png')
load_item('axe', 'axe.png')
load_item('fossil', 'fossil.png')
load_item('fuel tank', 'fuel tank.png')
load_item('fuel', 'fuel.png')
load_item('hammer', 'hammer.png')
load_item('ladder', 'ladder.png')
load_item('water', 'water.png')
load_item('window-piece', 'window-piece.png')
load_item('steel', 'steel.png')


##################연구실 안 제작 조합#################


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
                  'stone', 'stone', 'fire',
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
        'recipe':[None, 'stick', 'steel',
                  None, 'stick', 'steel',
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


#################연구실 제작창################


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


#########메인루프#########


while not done:

    if current_map == "outside1" and is_tree_pressing:
        current_time = pygame.time.get_ticks()
        if current_time - tree_press_start_time >= GATHER_DURATION:
            wood_drop_x = TREE_AREA.x + TREE_AREA.width // 2 - ITEM_SIZE // 2
            wood_drop_y = person_y + origin_person_image.get_height() - ITEM_SIZE
            DROPPED_ITEMS.append({
                'item_name': 'wood',
                'rect': pygame.Rect(wood_drop_x, wood_drop_y, ITEM_SIZE, ITEM_SIZE)
            })
            is_tree_pressing = False
            tree_press_start_time = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and game_over:
            done = True
        
        if event.type == pygame.MOUSEBUTTONUP and not game_over:
            
            if current_map == "outside1" and is_tree_pressing:
                is_tree_pressing = False
                tree_press_start_time = 0
            
            mouse_pos = pygame.mouse.get_pos()
            
            if is_drag:
                dropped_in_crafting = False
                
                #슬롯에 넣기 시도
                for i in range(len(CRAFT_SLOT_RECTS)):
                    if CRAFT_SLOT_RECTS[i].collidepoint(mouse_pos) and crafting_table[i] is None:
                        crafting_table[i] = drag_item
                        dropped_in_crafting = True
                        break

                #넣지 못했을 때
                if not dropped_in_crafting:
                    if drag_item_original and drag_item_original.startswith("inventory"):
                        try:
                            original_idx = int(drag_item_original.split('_')[-1])

                            if original_idx <= len(inventory):
                                inventory.insert(original_idx, drag_item)
                            else:
                                inventory.append(drag_item)
                        except ValueError:
                            inventory.append(drag_item)
                    else:
                        inventory.append(drag_item)
                
                is_drag = False
                drag_item = None
                drag_item_original = None
                drag_offset_x, drag_offset_y = 0, 0


        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_pos = pygame.mouse.get_pos()
            
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
                    continue

            elif current_map == "inside":
                
                if DIC_AREA.collidepoint(mouse_pos):
                    dic_open = not dic_open
                    if dic_open:
                        open_door = False
                    continue

                #제작/인벤창 열기
                if CLICK_AREA.collidepoint(mouse_pos):
                    if not open_door:
                        open_door = True
                        continue
                
                if open_door:
                    if MAKE_BUTTON_AREA.collidepoint(mouse_pos):
                        found_recipe = False
                        for recipe_data in RECIPES:
                            if crafting_table == recipe_data['recipe']:
                                inventory.append(recipe_data['result'])
                                crafting_table = [None] * 9
                                found_recipe = True
                                break
                        if not found_recipe:
                            game_over = True
                            open_door = False
                        continue
                    
                    if not is_drag:
                        for i in range(len(inventory)):
                            if i < len(INVENTORY_SLOT_RECTS) and INVENTORY_SLOT_RECTS[i].collidepoint(mouse_pos):
                                is_drag = True
                                drag_item = inventory[i]
                                inventory.pop(i) 
                                drag_item_original = f"inventory_slot_{i}"
                                
                                drag_offset_x = mouse_pos[0] - INVENTORY_SLOT_RECTS[i].x
                                drag_offset_y = mouse_pos[1] - INVENTORY_SLOT_RECTS[i].y
                                break
                        
                        if not is_drag:
                            for i in range(len(crafting_table)):
                                if crafting_table[i] is not None and CRAFT_SLOT_RECTS[i].collidepoint(mouse_pos):
                                    drag_item = crafting_table[i]
                                    drag_item_original = f"crafting_slot_{i}"
                                    crafting_table[i] = None
                                    is_drag = True
                                    drag_offset_x = mouse_pos[0] - CRAFT_SLOT_RECTS[i].x
                                    drag_offset_y = mouse_pos[1] - CRAFT_SLOT_RECTS[i].y
                                    break

                make_window_rect = make2_image.get_rect(topleft=(make2_image_x, make2_image_y))
                inven_window_rect = inven_image.get_rect(topleft=(inven_image_x, inven_image_y))

                if open_door and not make_window_rect.collidepoint(mouse_pos) and not CLICK_AREA.collidepoint(mouse_pos) and not inven_window_rect.collidepoint(mouse_pos):
                    open_door = False

                dic_window_rect = dic_image.get_rect(topleft=(dic_image_x, dic_image_y))
                if dic_open and not dic_window_rect.collidepoint(mouse_pos) and not CLICK_AREA.collidepoint(mouse_pos) and not DIC_AREA.collidepoint(mouse_pos):
                    dic_open = False

            elif current_map == "outside2":
                if OUTSIDE_MAKE_AREA.collidepoint(mouse_pos):
                    outside_make_door = not outside_make_door
                    continue
                
                outside_make_window_rect = make_outside_image.get_rect(topleft=(make_outside_image_x, make_outside_image_y))
                if outside_make_door and not outside_make_window_rect.collidepoint(mouse_pos) and not OUTSIDE_MAKE_AREA.collidepoint(mouse_pos):
                    outside_make_door = False
                    continue
    
    if game_over:
        screen.fill(BLACK)
        game_over_text = font.render("GAME OVER", True, RED)
        sub_text = small_font_40.render("Press ESC to Quit", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(sub_text, (SCREEN_WIDTH // 2 - sub_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    else:
        keys = pygame.key.get_pressed()
        
        if current_map == "outside1":
            if keys[pygame.K_LEFT]:
                person_x -= person_speed
                person_image = flip_person_image
                person_direction_right = False
            if keys[pygame.K_RIGHT]:
                person_x += person_speed
                person_image = origin_person_image
                person_direction_right = True

            if person_x < 0:
                person_x = 0
            elif person_x > SCREEN_WIDTH - person_image.get_width():
                current_map = "outside2"
                person_x = 5

            screen.blit(start_background_image, (0, 0))
            screen.blit(person_image, (person_x, person_y))
            
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
            if keys[pygame.K_LEFT]:
                person_x -= person_speed
                person_image = flip_person_image
                person_direction_right = False
            if keys[pygame.K_RIGHT]:
                person_x += person_speed
                person_image = origin_person_image
                person_direction_right = True

            if person_x < 0:
                current_map = "outside1"
                person_x = SCREEN_WIDTH - person_image.get_width() - 5
            elif person_x > SCREEN_WIDTH - person_image.get_width():
                person_x = SCREEN_WIDTH - person_image.get_width()
            
            screen.blit(background_image, (0, 0))
            screen.blit(person_image, (person_x, person_y))

            if open_door and not dic_open:
                screen.blit(make2_image, (make2_image_x, make2_image_y))
                screen.blit(inven_image, (inven_image_x, inven_image_y))
                #pygame.draw.rect(screen, RED, MAKE_BUTTON_AREA, 3)

                have_num = min(len(inventory), len(INVENTORY_SLOT_POSITIONS))
                for i in range(have_num):
                    slot_x, slot_y = INVENTORY_SLOT_POSITIONS[i]
                    item_name = inventory[i]
                    item_draw = item_images.get(item_name)
                    if item_draw:
                        screen.blit(item_draw, (slot_x, slot_y))
                
                for i in range(len(crafting_table)):
                    item_name = crafting_table[i]
                    if item_name is not None:
                        slot_x, slot_y = CRAFT_SLOT_POSITIONS[i]
                        item_draw = item_images.get(item_name)
                        if item_draw:
                            screen.blit(item_draw, (slot_x, slot_y))

            if dic_open and not open_door:
                screen.blit(dic_image, (dic_image_x, dic_image_y))

        elif current_map == "outside2":
            if keys[pygame.K_LEFT]:
                person_x -= person_speed
                person_image = flip_person_image
                person_direction_right = False

            if keys[pygame.K_RIGHT]:
                person_x += person_speed
                person_image = origin_person_image
                person_direction_right = True

            if person_x < 0:
                current_map = "outside1"
                person_x = SCREEN_WIDTH - person_image.get_width() - 5
            elif person_x > SCREEN_WIDTH - person_image.get_width():
                person_x = SCREEN_WIDTH - person_image.get_width()
            
            screen.blit(second_background_image, (0, 0))
            screen.blit(person_image, (person_x, person_y))

            if outside_make_door:
                screen.blit(make_outside_image, (make_outside_image_x, make_outside_image_y))

    if is_drag and drag_item is not None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        drag_item_draw = item_images.get(drag_item)

        if drag_item_draw:
            screen.blit(drag_item_draw, (mouse_x - drag_offset_x, mouse_y - drag_offset_y))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()