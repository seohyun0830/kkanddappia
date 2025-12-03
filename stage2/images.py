import pygame
import os
from .setting import *

class ImageManager:
    def __init__(self):
        self.item_images = {}
        self.all_animations = {}
        self.spaceship_parts = []
        
        self.BAG_FRAMES = ['person_bag1.png', 'person_bag2.png', 'person_bag3.png']
        self.IN_FRAMES = ['person_in1.png', 'person_in2.png', 'person_in3.png']
        self.TREE_FRAMES = ['person_tree1.png', 'person_tree2.png']
        
        self.load_all_assets()

    def safe_load_image(self, filename, size=None, convert_alpha=True):
        path = os.path.join(ASSETS_PATH, filename)
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

    def load_animation_set(self, frame_names, set_name):
        right_frames = []
        left_frames = []
        
        for name in frame_names:
            img = self.safe_load_image(name, PLAYER_SIZE, True) 
            
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
            
        self.all_animations[set_name] = {
            'right': right_frames,
            'left': left_frames,
            'stand_right': stand_right,
            'stand_left': stand_left
        }

    def load_item(self, name, filename):
        size = (ITEM_SIZE, ITEM_SIZE)
        convert_alpha = True
        
        if name.startswith('dic_p'):
            size = (IMG_SIZE_DIC[0] - 150, IMG_SIZE_DIC[1] - 40)
            convert_alpha = False
            
        self.item_images[name] = self.safe_load_image(filename, size, convert_alpha)

    def load_all_assets(self):
        # 배경
        self.start_background_image = self.safe_load_image('outside.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), False)
        self.background_image = self.safe_load_image('inside.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), False)
        self.second_background_image = self.safe_load_image('outside2.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), False)
        self.new_background_image = self.safe_load_image('2to3.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), False)
        self.bomb_ending_image=self.safe_load_image('bomb_ending.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), False)
        # 사람
        self.load_animation_set(self.BAG_FRAMES, 'bag')
        self.load_animation_set(self.IN_FRAMES, 'in')
        self.load_animation_set(self.TREE_FRAMES, 'tree')

        # 아이콘
        self.icon_bag_image = self.safe_load_image('icon_bag.png', IMG_SIZE_ICON)
        self.icon_dic_image = self.safe_load_image('icon_dic.png', IMG_SIZE_ICON)

        self.make_image = self.safe_load_image('make.png', IMG_SIZE_MAKE)
        self.make2_image = self.safe_load_image('make2.PNG', IMG_SIZE_MAKE2)
        self.inven_image = self.safe_load_image('inventory.PNG', IMG_SIZE_INVEN)
        self.inven2_image = self.safe_load_image('inventory2.PNG', IMG_SIZE_INVEN)
        self.make_outside_image = self.safe_load_image('make_outside.png', IMG_SIZE_MAKE)
        self.spaceship_make_image = self.safe_load_image('spaceship_make.png', IMG_SIZE_SPACESHIP_MAKE)
        self.dic_image = self.safe_load_image('dic.png', IMG_SIZE_DIC)

        self.fly_spaceship_image = self.safe_load_image('fly_spaceship.png', (250, 200), True)
        self.spaceship_display_image = self.safe_load_image('spaceship.png', (190, 100))
        self.spaceship_completed_image = self.safe_load_image('spaceship.png', (250, 200))

        for i in range(1, 10):
            part_name = f'piece_{i}.png'
            img = self.safe_load_image(part_name, convert_alpha=True)
            self.spaceship_parts.append(img)

        # 아이템
        items = {
            'fire': 'fire.png', 'stone': 'stone.png', 'soil': 'soil.png',
            'wood': 'wood.png', 'stick': 'stick.png', 'glass': 'glass.png',
            'window': 'window.png', 'screw': 'screw.png', 'steel': 'steel.png',
            'axe': 'axe.png', 'fossil': 'fossil.png', 'fuel tank': 'fuel tank.png',
            'fuel': 'fuel.png', 'hammer': 'hammer.png', 'ladder': 'ladder.png',
            'water': 'water.png', 'window-piece': 'window_piece.png',
            'spaceship': 'spaceship.png',
            'spaceship-side': 'spaceship_side_piece.png',
            'spaceship-side-piece': 'spaceship_side_1_9.png',
            'spaceship-roof': 'spaceship_roof_piece.png',
            'spaceship-roof-piece': 'spaceship_roof_1_4.png'
        }

        #쪽지

        self.paper_image=self.safe_load_image('paper.png', (PAPER_SIZE, PAPER_SIZE))

        for name, filename in items.items():
            self.load_item(name, filename)

        # 사전
        for i in range(1, MAX_DIC_PAGES + 1):
            self.load_item(f'dic_p{i}', f'dic_{i}.jpg')