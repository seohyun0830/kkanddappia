import pygame
import os
from stage2_back.setting import *

class ImageManager:
    def __init__(self):
        
        #배경
        self.background = self.safe_load_image('back_stage2.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.back_to3_bg = self.safe_load_image('backto3.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        #플레이어
        player_size = (100, 100)
        self.player_walk_right = [
            self.safe_load_image('player_walk1.png', player_size),
            self.safe_load_image('player_walk2.png', player_size)
        ]
        
        self.player_walk_left = [
            pygame.transform.flip(img, True, False) for img in self.player_walk_right
        ]
        
        #우주선 조각
        self.broken_piece = self.safe_load_image('broken_piece.png', (PIECE_SIZE, PIECE_SIZE))
        
        #우주선 완성
        self.completed_spaceship = self.safe_load_image('back_spaceship.png', (250, 200))

        self.arrow_image=self.safe_load_image('arrow.png', (ARROW_SIZE, ARROW_SIZE))

        self.spaceship_parts = []
        for i in range(1, 10):
            part_name = f'piece{i}.png'
            img = self.safe_load_image(part_name)
            self.spaceship_parts.append(img)
            
    def safe_load_image(self, filename, size=None):
        path = os.path.join(ASSETS_PATH, filename)
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"파일 없음: {path}")
                
            img = pygame.image.load(path).convert_alpha()
            
            if size:
                img = pygame.transform.scale(img, size)
            return img
            
        except Exception as e:
            print(f"[System] 이미지 로드 실패: {filename} - {e}")
            fallback = pygame.Surface(size if size else (50, 50))
            fallback.fill(RED)
            return fallback