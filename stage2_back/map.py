import pygame
import random
import math
from setting import *

class MapManager:
    def __init__(self, images):
        self.images = images
        
        # 부서진 조각
        self.ground_pieces = []
        for _ in range(TOTAL_PIECES):
            px = random.randint(90, 1100)
            py = random.randint(500, 650)
            rect = pygame.Rect(px, py, PIECE_SIZE, PIECE_SIZE)
            self.ground_pieces.append(rect)
            
        #발사대 조각 수
        self.assembled_count = 0
        
        self.reveal_order = list(range(TOTAL_PIECES))
        random.shuffle(self.reveal_order)
        
        self.pulsate_start_time = pygame.time.get_ticks()

    def draw_background(self, screen, is_cutscene=False):
        if is_cutscene:
            screen.blit(self.images.back_to3_bg, (0, 0))
        else:
            screen.blit(self.images.background, (0, 0))

    def draw_ground_pieces(self, screen):
        for rect in self.ground_pieces:
            screen.blit(self.images.broken_piece, rect.topleft)

    def draw_launchpad_info(self, screen):
        center_x = LAUNCHPAD_RECT.centerx
        bottom_y = LAUNCHPAD_RECT.bottom - 20

        SCALE_FACTOR = 0.2
        
        if self.images.spaceship_parts:
            sample = self.images.spaceship_parts[0]
            part_w = int(sample.get_width() * SCALE_FACTOR)
            part_h = int(sample.get_height() * SCALE_FACTOR)
        else:
            part_w, part_h = int(80 * SCALE_FACTOR), int(60 * SCALE_FACTOR)

        total_w = part_w * 3
        total_h = part_h * 3
        
        draw_base_x = center_x - total_w // 2
        draw_base_y = bottom_y - total_h-80

        if self.assembled_count < TOTAL_PIECES:
            cols = 3
            for i in range(self.assembled_count):
                part_idx = self.reveal_order[i]
                
                if part_idx < len(self.images.spaceship_parts):
                    part_img_original = self.images.spaceship_parts[part_idx]
                    part_img_scaled = pygame.transform.scale(part_img_original, (part_w, part_h))
                    
                    r = part_idx // cols
                    c = part_idx % cols
                    
                    px = draw_base_x + (c * part_w)
                    py = draw_base_y + (r * part_h)
                    
                    screen.blit(part_img_scaled, (px, py))

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

        #게이지
        gauge_w = 200
        gauge_h = 20
        gauge_x = LAUNCHPAD_RECT.centerx - gauge_w // 2
        gauge_y = LAUNCHPAD_RECT.bottom + 10
        
        pygame.draw.rect(screen, BLACK, (gauge_x, gauge_y, gauge_w, gauge_h), 3)
        ratio = self.assembled_count / TOTAL_PIECES
        fill_w = int(gauge_w * ratio)
        color = GREEN if self.assembled_count >= TOTAL_PIECES else RED
        if fill_w > 0:
            pygame.draw.rect(screen, color, (gauge_x + 3, gauge_y + 3, fill_w - 6, gauge_h - 6))
        
        font = pygame.font.Font(None, 30)

        percent=int(ratio*100)

        text = font.render(f"{percent}%", True, WHITE)
        screen.blit(text, (gauge_x + gauge_w + 10, gauge_y))

    def check_collection(self, player_rect):
        collected_count = 0
        for i in range(len(self.ground_pieces) - 1, -1, -1):
            piece_rect = self.ground_pieces[i]
            
            if player_rect.colliderect(piece_rect):
                self.ground_pieces.pop(i)
                collected_count += 1
                
        return collected_count