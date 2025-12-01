import pygame
import os
from setting import *

class ImageManager:
    def __init__(self):
        # --- 이미지 로드 시작 ---
        
        # 1. 배경 이미지 (일반 게임용)
        self.background = self.safe_load_image('back_stage2.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # [추가됨] 2. 엔딩 컷신 배경 이미지
        self.back_to3_bg = self.safe_load_image('backto3.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # 3. 플레이어 애니메이션 (걷는 모습)
        # 원본 파일이 오른쪽을 보고 있다고 가정하고 로드 (크기는 100x100 정도로 고정)
        player_size = (100, 100)
        self.player_walk_right = [
            self.safe_load_image('player_walk1.png', player_size),
            self.safe_load_image('player_walk2.png', player_size)
        ]
        
        # 왼쪽 보는 모습은 오른쪽 이미지를 좌우 반전(flip)시켜서 생성
        self.player_walk_left = [
            pygame.transform.flip(img, True, False) for img in self.player_walk_right
        ]
        
        # 4. 우주선 조각 (설정된 크기로 로드)
        self.broken_piece = self.safe_load_image('broken_piece.png', (PIECE_SIZE, PIECE_SIZE))
        
        # 5. 완성된 우주선 (발사대 위에 올라갈 크기)
        self.completed_spaceship = self.safe_load_image('back_spaceship.png', (250, 200))

        self.spaceship_parts = []
        for i in range(1, 10): # 1부터 9까지 반복
            part_name = f'piece{i}.png'
            # 원본 크기 그대로 로드 (이미 3x3 크기에 맞춰 잘라두셨다고 가정)
            # 만약 크기 조절이 필요하면 safe_load_image 두 번째 인자에 (w, h)를 넣으세요.
            img = self.safe_load_image(part_name)
            self.spaceship_parts.append(img)
            
    def safe_load_image(self, filename, size=None):
        """이미지를 안전하게 불러오고, 실패 시 빨간 네모를 반환하는 함수"""
        path = os.path.join(ASSETS_PATH, filename)
        try:
            # 파일 존재 여부 확인
            if not os.path.exists(path):
                raise FileNotFoundError(f"파일 없음: {path}")
                
            # 이미지 로드 및 투명 배경 지원(convert_alpha)
            img = pygame.image.load(path).convert_alpha()
            
            # 크기 조절이 필요한 경우
            if size:
                img = pygame.transform.scale(img, size)
            return img
            
        except Exception as e:
            print(f"[System] 이미지 로드 실패: {filename} - {e}")
            # 로드 실패 시 게임이 꺼지지 않게 빨간색 네모(Placeholder) 반환
            fallback = pygame.Surface(size if size else (50, 50))
            fallback.fill(RED)
            return fallback