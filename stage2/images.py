import pygame
import os
from setting import *

# --- 전역 이미지 저장소 ---
backgrounds = {}
ui_images = {}
item_images = {}
animations = {}
fonts = {}

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
        print(f"Error loading {filename}: {e}")
        placeholder = pygame.Surface(size or (100, 100))
        placeholder.fill(RED)
        if convert_alpha:
            placeholder.set_colorkey(RED)
        return placeholder

def load_animation_set(frame_names, set_name):
    right_frames = []
    left_frames = []
    
    for name in frame_names:
        img = safe_load_image(name, PLAYER_SIZE, True) 
        
        # 빨간색 플레이스홀더인지 확인 (로드 실패 시)
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
    
    animations[set_name] = {
        'right': right_frames,
        'left': left_frames,
        'stand_right': right_frames[stand_index],
        'stand_left': left_frames[stand_index]
    }

def load_item(name, filename, dic_image_size=None):
    size = (ITEM_SIZE, ITEM_SIZE)
    convert_alpha = True
    
    if name.startswith('dic_p') and dic_image_size:
        size = (dic_image_size[0] - 150, dic_image_size[1] - 40)
        convert_alpha = False
        
    item_images[name] = safe_load_image(filename, size, convert_alpha)

def load_all_assets():
    """메인 게임 시작 전 모든 이미지를 로드하는 함수"""
    
    # 1. 폰트 로드
    fonts['default'] = pygame.font.Font(None, 74)
    fonts['small'] = pygame.font.Font(None, 30)
    fonts['small_40'] = pygame.font.Font(None, 40)
    fonts['micro'] = pygame.font.Font(None, 24)

    # 2. 배경 로드
    backgrounds['outside1'] = safe_load_image('outside.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), False)
    backgrounds['inside'] = safe_load_image('inside.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), False)
    backgrounds['outside2'] = safe_load_image('outside2.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), False)
    backgrounds['2to3'] = safe_load_image('2to3.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), False)

    # 3. UI 이미지 로드
    ui_images['icon_bag'] = safe_load_image('icon_bag.png', (ICON_SIZE, ICON_SIZE))
    ui_images['icon_dic'] = safe_load_image('icon_dic.png', (ICON_SIZE, ICON_SIZE))
    
    ui_images['make'] = safe_load_image('make.png', (600, 600))
    ui_images['make2'] = safe_load_image('make2.PNG', (546, 380))
    ui_images['inventory'] = safe_load_image('inventory.PNG', (600, 600))
    ui_images['make_outside'] = safe_load_image('make_outside.png', (600, 600))
    ui_images['spaceship_make'] = safe_load_image('spaceship_make.png', (600, 600))
    ui_images['dic'] = safe_load_image('dic.png', (600, 600))
    
    # 4. 애니메이션 로드
    BAG_FRAMES = ['person_bag1.png', 'person_bag2.png', 'person_bag3.png']
    IN_FRAMES = ['person_in1.png', 'person_in2.png', 'person_in3.png']
    TREE_FRAMES = ['person_tree1.png', 'person_tree2.png']
    
    load_animation_set(BAG_FRAMES, 'bag')
    load_animation_set(IN_FRAMES, 'in')
    load_animation_set(TREE_FRAMES, 'tree')
    
    # 우주선 비행 이미지 별도 로드
    animations['fly_spaceship'] = safe_load_image('fly_spaceship.png', (250, 200), True)

    # 5. 아이템 로드
    item_list = [
        ('fire', 'fire.png'), ('stone', 'stone.png'), ('soil', 'soil.png'),
        ('wood', 'wood.png'), ('stick', 'stick.png'), ('glass', 'glass.png'),
        ('window', 'window.png'), ('screw', 'screw.png'), ('steel', 'steel.png'),
        ('axe', 'axe.png'), ('fossil', 'fossil.png'), ('fuel tank', 'fuel tank.png'),
        ('fuel', 'fuel.png'), ('hammer', 'hammer.png'), ('ladder', 'ladder.png'),
        ('water', 'water.png'), ('window-piece', 'window_piece.png')
    ]
    for name, file in item_list:
        load_item(name, file)
        
    # 우주선 관련 아이템
    load_item('spaceship', 'spaceship.png')
    load_item('spaceship-side', 'spaceship_side_piece.png')
    load_item('spaceship-side-piece', 'spaceship_side_1_9.png')
    load_item('spaceship-roof', 'spaceship_roof_piece.png')
    load_item('spaceship-roof-piece', 'spaceship_roof_1_4.png')
    
    # 우주선 완성/조립용 이미지 (아이템 딕셔너리에 추가하거나 별도 관리 가능)
    item_images['spaceship_display'] = safe_load_image('spaceship.png', (190, 100))
    item_images['spaceship_completed'] = safe_load_image('spaceship.png', (250, 200))

    # 사전 페이지 로드
    dic_size = (ui_images['dic'].get_width(), ui_images['dic'].get_height())
    for i in range(1, MAX_DIC_PAGES + 1):
        load_item(f'dic_p{i}', f'dic_{i}.jpg', dic_size)