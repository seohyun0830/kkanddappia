import pygame
import random
import math
from setting import *

class MapManager:
    def __init__(self, images):
        self.images = images
        
        # 1. 바닥 조각 생성 (9개)
        self.ground_pieces = []
        for _ in range(TOTAL_PIECES):
            # 바닥 범위 내 랜덤 생성 (플레이어 이동 경로 근처)
            # x: 50 ~ 1100, y: 500 ~ 650
            px = random.randint(50, 1100)
            py = random.randint(500, 650)
            rect = pygame.Rect(px, py, PIECE_SIZE, PIECE_SIZE)
            self.ground_pieces.append(rect)
            
        # 발사대에 조립된 개수
        self.assembled_count = 0
        
        # 조각이 나타날 랜덤 순서 (0~8 인덱스 섞기)
        self.reveal_order = list(range(TOTAL_PIECES))
        random.shuffle(self.reveal_order)
        
        # 완성 후 효과 타이머
        self.pulsate_start_time = pygame.time.get_ticks()

    def draw_background(self, screen, is_cutscene=False):
        """배경 그리기 (컷신 모드 지원)"""
        if is_cutscene:
            screen.blit(self.images.back_to3_bg, (0, 0))
        else:
            screen.blit(self.images.background, (0, 0))

    def draw_ground_pieces(self, screen):
        """바닥에 남은 조각 그리기"""
        for rect in self.ground_pieces:
            screen.blit(self.images.broken_piece, rect.topleft)

    def draw_launchpad_info(self, screen):
        """발사대 정보 그리기 (조립 과정 -> 완성 -> 게이지)"""
        center_x = LAUNCHPAD_RECT.centerx
        bottom_y = LAUNCHPAD_RECT.bottom - 20

        # 발사대에 그려질 조각 크기 축소 설정 (0.7배)
        SCALE_FACTOR = 0.2
        
        if self.images.spaceship_parts:
            sample = self.images.spaceship_parts[0]
            part_w = int(sample.get_width() * SCALE_FACTOR)
            part_h = int(sample.get_height() * SCALE_FACTOR)
        else:
            part_w, part_h = int(80 * SCALE_FACTOR), int(60 * SCALE_FACTOR)

        # 전체 3x3 완성본의 크기 계산
        total_w = part_w * 3
        total_h = part_h * 3
        
        # 그리기 시작점 (중앙 정렬)
        draw_base_x = center_x - total_w // 2
        draw_base_y = bottom_y - total_h-80

        # 1. [미완성] 모은 개수만큼 랜덤 조각 그리기
        if self.assembled_count < TOTAL_PIECES:
            cols = 3
            for i in range(self.assembled_count):
                part_idx = self.reveal_order[i]
                
                if part_idx < len(self.images.spaceship_parts):
                    part_img_original = self.images.spaceship_parts[part_idx]
                    part_img_scaled = pygame.transform.scale(part_img_original, (part_w, part_h))
                    
                    # 3x3 격자 위치 계산
                    r = part_idx // cols
                    c = part_idx % cols
                    
                    px = draw_base_x + (c * part_w)
                    py = draw_base_y + (r * part_h)
                    
                    screen.blit(part_img_scaled, (px, py))

        # 2. [완성] 원본 이미지로 Pulsate 효과
        else:
            current_time = pygame.time.get_ticks()
            time_factor = (current_time - self.pulsate_start_time) * PULSATE_SPEED
            scale_offset = (math.sin(time_factor) + 1) / 2 
            current_scale = PULSATE_MIN_SCALE + scale_offset * (PULSATE_MAX_SCALE - PULSATE_MIN_SCALE)
            
            original_img = self.images.completed_spaceship
            w = int(original_img.get_width() * current_scale)
            h = int(original_img.get_height() * current_scale)
            scaled_img = pygame.transform.scale(original_img, (w, h))
            
            draw_x = LAUNCHPAD_RECT.centerx - w // 2
            draw_y = LAUNCHPAD_RECT.bottom - h - 90
            
            screen.blit(scaled_img, (draw_x, draw_y))

        # 3. 진행도 게이지
        gauge_w = 200
        gauge_h = 20
        gauge_x = LAUNCHPAD_RECT.centerx - gauge_w // 2
        gauge_y = LAUNCHPAD_RECT.bottom + 10
        
        pygame.draw.rect(screen, BLACK, (gauge_x, gauge_y, gauge_w, gauge_h), 3)
        ratio = self.assembled_count / TOTAL_PIECES
        fill_w = int(gauge_w * ratio)
        color = GREEN if self.assembled_count >= TOTAL_PIECES else YELLOW
        if fill_w > 0:
            pygame.draw.rect(screen, color, (gauge_x + 3, gauge_y + 3, fill_w - 6, gauge_h - 6))
        
        font = pygame.font.Font(None, 30)
        text = font.render(f"{self.assembled_count}/{TOTAL_PIECES}", True, WHITE)
        screen.blit(text, (gauge_x + gauge_w + 10, gauge_y))

    # [핵심 수정] 마우스 클릭 없이, 플레이어 몸체와 닿으면 획득
    def check_collection(self, player_rect):
        """
        플레이어와 조각이 닿으면(충돌하면) 수집 처리
        Returns: 수집한 개수 (한 번에 여러 개 먹을 수도 있음)
        """
        collected_count = 0
        # 리스트 역순 순회 (안전한 삭제를 위해)
        for i in range(len(self.ground_pieces) - 1, -1, -1):
            piece_rect = self.ground_pieces[i]
            
            # colliderect: 두 사각형이 겹치는지 확인 (충돌 감지)
            if player_rect.colliderect(piece_rect):
                self.ground_pieces.pop(i) # 바닥 리스트에서 제거
                collected_count += 1
                
        return collected_count