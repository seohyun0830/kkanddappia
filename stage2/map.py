import pygame
import math
from setting import *

class MapManager:
    def __init__(self, stage):
        self.stage = stage
        self.images = stage.images
        
        # 현재 맵 상태 ("outside1", "inside", "outside2")
        self.current_map = "outside1"
        
        # 나무 캐기 관련
        self.is_tree_pressing = False
        self.tree_press_start_time = 0
        
        # 우주선 깜박임 효과 관련
        self.pulsate_time_start = pygame.time.get_ticks()
        self.current_scale = 1.0

    def update(self):
        """맵 상태 업데이트 (나무 캐기 완료 체크, 깜박임 계산)"""
        current_time = pygame.time.get_ticks()

        # 1. 나무 캐기 완료 체크
        if self.current_map == "outside1" and self.is_tree_pressing:
            if current_time - self.tree_press_start_time >= GATHER_DURATION:
                self.drop_wood()
                self.is_tree_pressing = False
                self.tree_press_start_time = 0
                
                # 작업 완료 시 소리 끄기
                if self.stage.sounds.tree_sound:
                    self.stage.sounds.tree_sound.stop()

        # 2. 우주선 깜박임 효과 계산 (Sine 파동)
        time_factor = (current_time - self.pulsate_time_start) * PULSATE_SPEED
        scale_offset = (math.sin(time_factor) + 1) / 2
        self.current_scale = PULSATE_MIN_SCALE + scale_offset * (PULSATE_MAX_SCALE - PULSATE_MIN_SCALE)

    def handle_click(self, mouse_pos):
        """맵 상의 오브젝트 클릭 처리"""
        
        # --- Outside 1 ---
        if self.current_map == "outside1":
            # 나무 클릭 (채집 시작)
            if TREE_AREA.collidepoint(mouse_pos):
                if not self.is_tree_pressing:
                    self.is_tree_pressing = True
                    self.tree_press_start_time = pygame.time.get_ticks()
                    
                    # 소리 재생
                    if self.stage.sounds.tree_sound:
                        self.stage.sounds.tree_sound.play(loops=-1)
                return

            # 떨어진 아이템 줍기
            if self.check_item_pickup(mouse_pos):
                return

            # 문 클릭 (Inside로 이동)
            if OUTSIDE_DOOR_AREA.collidepoint(mouse_pos):
                self.current_map = "inside"
                self.stage.player.x = 100
                self.stage.player.reset_animation()
                return

            # Stage 1 영역 (페이드 아웃 효과)
            if STAGE1_AREA.collidepoint(mouse_pos):
                if not self.stage.player.is_fading_out:
                    self.stage.player.is_fading_out = True
                    self.stage.player.alpha = 255
                return

        # --- Inside ---
        elif self.current_map == "inside":
            # 사전 클릭
            if DIC_AREA.collidepoint(mouse_pos):
                self.stage.dic_open = not self.stage.dic_open
                if self.stage.dic_open:
                    self.stage.close_all_popups()
                    self.stage.dic_open = True
                return

            # 특정 영역 클릭 시 제작창/문 열기
            if CLICK_AREA.collidepoint(mouse_pos):
                self.stage.open_door = True
                self.stage.is_crafting_open = True
                self.stage.dic_open = False
                return

        # --- Outside 2 ---
        elif self.current_map == "outside2":
            # 외부 제작대 클릭
            if OUTSIDE_MAKE_AREA.collidepoint(mouse_pos):
                self.stage.open_door = True
                self.stage.is_crafting_open = True
                self.stage.dic_open = False
                return

            # 우주선 영역 클릭
            if SPACESHIP_AREA.collidepoint(mouse_pos):
                self.handle_spaceship_click()
                return

    def handle_spaceship_click(self):
        """우주선 클릭 로직 분리"""
        # 1. 우주선 완성 시 -> 엔딩(탑승) 시작
        is_completed = len(self.stage.spaceship_assembly_storage) == MAX_SPACESHIP_PARTS
        
        if is_completed:
            self.stage.close_all_popups()
            self.stage.player.start_walking_into_spaceship()
            return

        # 2. 미완성 && 인벤토리에 우주선 아이템 보유 시 -> 우주선 제작창 열기
        has_spaceship_item = 'spaceship' in self.stage.inventory
        if has_spaceship_item and not is_completed:
            self.stage.is_spaceship_crafting_open = True
            self.stage.open_door = False
            self.stage.is_crafting_open = False
            self.stage.dic_open = False

    def check_item_pickup(self, mouse_pos):
        """떨어진 아이템 줍기"""
        for i in range(len(self.stage.dropped_items) - 1, -1, -1):
            item = self.stage.dropped_items[i]
            if item['rect'].collidepoint(mouse_pos):
                self.stage.inventory.append(item['item_name'])
                self.stage.dropped_items.pop(i)
                return True
        return False

    def drop_wood(self):
        """나무 캐기 완료 시 아이템 드롭"""
        wood_drop_x = TREE_AREA.x + TREE_AREA.width // 2 - ITEM_SIZE // 2
        wood_drop_y = self.stage.player.y + self.stage.player.image.get_height()
        
        self.stage.dropped_items.append({
            'item_name': 'wood',
            'rect': pygame.Rect(wood_drop_x, wood_drop_y, ITEM_SIZE, ITEM_SIZE)
        })

    def draw(self):
        """배경 및 맵 요소 그리기"""
        # 엔딩(비행) 애니메이션 중일 때는 배경만 그림
        if self.stage.player.is_flying_animation_active:
            self.stage.screen.blit(self.images.new_background_image, (0, 0))
            return
        
        # 우주선으로 걸어가는 중일 때도 배경 변경
        if self.stage.player.is_walking_into_spaceship:
            self.stage.screen.blit(self.images.new_background_image, (0, 0))
            return

        # 맵별 배경 그리기
        if self.current_map == "outside1":
            self.stage.screen.blit(self.images.start_background_image, (0, 0))
            self.draw_tree_progress()

        elif self.current_map == "inside":
            self.stage.screen.blit(self.images.background_image, (0, 0))

        elif self.current_map == "outside2":
            self.stage.screen.blit(self.images.second_background_image, (0, 0))
            
            # 우주선 그리기 (진행 상황에 따라 다르게 표시)
            has_parts = len(self.stage.spaceship_assembly_storage) > 0
            has_item = 'spaceship' in self.stage.inventory
            
            if has_parts or has_item:
                is_completed = len(self.stage.spaceship_assembly_storage) == MAX_SPACESHIP_PARTS
                
                if is_completed:
                    self.draw_pulsating_spaceship()
                else:
                    # [핵심] 밑에서부터 차오르는 함수 호출
                    self.draw_progress_spaceship()

    def draw_progress_spaceship(self):
        """[핵심] 우주선 이미지를 부품 비율만큼 밑에서부터 잘라서 보여줌"""
        current_parts = len(self.stage.spaceship_assembly_storage)
        if current_parts == 0:
            return

        full_image = self.images.spaceship_completed_image
        w, h = full_image.get_size()
        
        # 1. 현재 진행 비율 (0.0 ~ 1.0)
        ratio = current_parts / MAX_SPACESHIP_PARTS
        
        # 2. 보여줄 높이 계산
        visible_height = int(h * ratio)
        
        # 3. 이미지의 어느 부분을 가져올지 설정 (밑에서부터 visible_height 만큼)
        # Rect(x, y, width, height) : 원본 이미지 기준
        src_rect = pygame.Rect(0, h - visible_height, w, visible_height)
        
        # 4. 화면에 그릴 위치 계산
        # 완성본의 Top Y 좌표 (기준점)
        center_x = SPACESHIP_AREA.x + SPACESHIP_AREA.width // 2
        top_y = SPACESHIP_AREA.y - h - 50 
        
        # 잘린 이미지는 그만큼 아래쪽에 그려야 바닥이 맞음
        draw_x = center_x - w // 2
        draw_y = top_y + (h - visible_height)
        
        # 5. 부분 그리기
        self.stage.screen.blit(full_image, (draw_x, draw_y), src_rect)

    def draw_pulsating_spaceship(self):
        """완성된 우주선 깜박임 효과 그리기"""
        original_w, original_h = self.images.spaceship_completed_image.get_size()
        new_w = int(original_w * self.current_scale)
        new_h = int(original_h * self.current_scale)
        
        scaled_image = pygame.transform.scale(self.images.spaceship_completed_image, (new_w, new_h))
        
        center_x = SPACESHIP_AREA.x + SPACESHIP_AREA.width // 2
        top_y = SPACESHIP_AREA.y - new_h - 50 
        draw_x = center_x - new_w // 2
        draw_y = top_y
        
        self.stage.screen.blit(scaled_image, (draw_x, draw_y))

    def draw_spaceship_gauge(self):
        """우주선 제작 진행도 게이지 그리기"""
        if self.stage.player.is_walking_into_spaceship or self.stage.player.is_flying_animation_active:
            return

        if not ('spaceship' in self.stage.inventory or self.stage.spaceship_assembly_storage):
            return

        part_count = len(self.stage.spaceship_assembly_storage)
        is_completed = part_count == MAX_SPACESHIP_PARTS

        gauge_width = 280
        gauge_height = 20
        
        gauge_x = SPACESHIP_AREA.x
        gauge_y = SPACESHIP_AREA.y + SPACESHIP_AREA.height + 10 
        
        # 외곽선
        gauge_rect_outer = pygame.Rect(gauge_x, gauge_y, gauge_width, gauge_height)
        pygame.draw.rect(self.stage.screen, BLACK, gauge_rect_outer, 3)

        # 채워진 부분
        progress_ratio = min(1.0, part_count / MAX_SPACESHIP_PARTS)
        filled_width = int(gauge_width * progress_ratio)
        gauge_color = GREEN if is_completed else RED

        gauge_rect_filled = pygame.Rect(gauge_x, gauge_y, filled_width, gauge_height)
        pygame.draw.rect(self.stage.screen, gauge_color, gauge_rect_filled)
        
        # 텍스트
        font = pygame.font.Font(None, 30)
        progress_text = font.render(f"{part_count}/{MAX_SPACESHIP_PARTS}", True, WHITE)
        text_x = gauge_x + gauge_width // 2 - progress_text.get_width() // 2
        text_y = gauge_y + gauge_height // 2 - progress_text.get_height() // 2
        self.stage.screen.blit(progress_text, (text_x, text_y))

    def draw_tree_progress(self):
        """나무 캐기 진행바 그리기"""
        if self.is_tree_pressing:
            elapsed = pygame.time.get_ticks() - self.tree_press_start_time
            progress = min(1.0, elapsed / GATHER_DURATION)
            
            bar_width = 100
            bar_height = 10
            bar_x = TREE_AREA.x + TREE_AREA.width // 2 - bar_width // 2
            bar_y = TREE_AREA.y - bar_height - 5
            
            # 배경바
            pygame.draw.rect(self.stage.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            # 진행바 (초록색)
            pygame.draw.rect(self.stage.screen, GREEN, (bar_x, bar_y, bar_width * progress, bar_height))

    def draw_dropped_items(self):
        """바닥에 떨어진 아이템 그리기"""
        if self.current_map == "outside1":
            for item in self.stage.dropped_items:
                item_draw = self.images.item_images.get(item['item_name'])
                if item_draw:
                    self.stage.screen.blit(item_draw, item['rect'])


'''
import pygame
import math
import random
from setting import *

class MapManager:
    def __init__(self, stage):
        self.stage = stage
        self.images = stage.images
        
        self.current_map = "outside1"
        
        # 나무
        self.is_tree_pressing = False
        self.tree_press_start_time = 0
        
        # 우주선 완성 깜빡
        self.pulsate_time_start = pygame.time.get_ticks()
        self.current_scale = 1.0

        #우주선 조각
        self.part_spaceship(range(MAX_SPACESHIP_PARTS))
        random.shuffle(self.part_spaceship)

    def update(self):
        current_time = pygame.time.get_ticks()

        # 나무 베기
        if self.current_map == "outside1" and self.is_tree_pressing:
            if current_time - self.tree_press_start_time >= GATHER_DURATION:
                self.drop_wood()
                self.is_tree_pressing = False
                self.tree_press_start_time = 0
                
                if self.stage.sounds.tree_sound:
                    self.stage.sounds.tree_sound.stop()

        # 우주선 깜빡임
        time_factor = (current_time - self.pulsate_time_start) * PULSATE_SPEED
        scale_offset = (math.sin(time_factor) + 1) / 2
        self.current_scale = PULSATE_MIN_SCALE + scale_offset * (PULSATE_MAX_SCALE - PULSATE_MIN_SCALE)

    def handle_click(self, mouse_pos):
        
        if self.current_map == "outside1":
            if TREE_AREA.collidepoint(mouse_pos):
                if not self.is_tree_pressing:
                    self.is_tree_pressing = True
                    self.tree_press_start_time = pygame.time.get_ticks()
                    
                    if self.stage.sounds.tree_sound:
                        self.stage.sounds.tree_sound.play(loops=-1)
                return

            if self.check_item_pickup(mouse_pos):
                return

            if OUTSIDE_DOOR_AREA.collidepoint(mouse_pos):
                self.current_map = "inside"
                self.stage.player.x = 100
                self.stage.player.reset_animation()
                return

            if STAGE1_AREA.collidepoint(mouse_pos):
                if not self.stage.player.is_fading_out:
                    self.stage.player.is_fading_out = True
                    self.stage.player.alpha = 255
                return

        elif self.current_map == "inside":
            # 사전 클릭
            if EASY_MODE and DIC_AREA.collidepoint(mouse_pos):
                self.stage.dic_open = not self.stage.dic_open
                if self.stage.dic_open:
                    self.stage.close_all_popups()
                    self.stage.dic_open = True
                return

            # 내부 들어가기, 제작창/사전 열기
            if CLICK_AREA.collidepoint(mouse_pos):
                self.stage.open_door = True
                self.stage.is_crafting_open = True
                self.stage.dic_open = False
                return

        elif self.current_map == "outside2":
            if OUTSIDE_MAKE_AREA.collidepoint(mouse_pos):
                self.stage.open_door = True
                self.stage.is_crafting_open = True
                self.stage.dic_open = False
                return

            if SPACESHIP_AREA.collidepoint(mouse_pos):
                self.handle_spaceship_click()
                return

    def handle_spaceship_click(self):
        is_completed = len(self.stage.spaceship_assembly_storage) == MAX_SPACESHIP_PARTS
        
        if is_completed:
            self.stage.close_all_popups()
            self.stage.player.start_walking_into_spaceship()
            return

        has_spaceship_item = 'spaceship' in self.stage.inventory
        if has_spaceship_item and not is_completed:
            self.stage.is_spaceship_crafting_open = True
            self.stage.open_door = False
            self.stage.is_crafting_open = False
            self.stage.dic_open = False

    def check_item_pickup(self, mouse_pos):
        for i in range(len(self.stage.dropped_items) - 1, -1, -1):
            item = self.stage.dropped_items[i]
            if item['rect'].collidepoint(mouse_pos):
                self.stage.inventory.append(item['item_name'])
                self.stage.dropped_items.pop(i)
                return True
        return False

    def drop_wood(self):
        wood_drop_x = TREE_AREA.x + TREE_AREA.width // 2 - ITEM_SIZE // 2
        wood_drop_y = self.stage.player.y + self.stage.player.image.get_height()
        
        self.stage.dropped_items.append({
            'item_name': 'wood',
            'rect': pygame.Rect(wood_drop_x, wood_drop_y, ITEM_SIZE, ITEM_SIZE)
        })

    def draw(self):
        if self.stage.player.is_flying_animation_active:
            self.stage.screen.blit(self.images.new_background_image, (0, 0))
            return
        
        if self.stage.player.is_walking_into_spaceship:
            self.stage.screen.blit(self.images.new_background_image, (0, 0))
            return

        if self.current_map == "outside1":
            self.stage.screen.blit(self.images.start_background_image, (0, 0))
            self.draw_tree_progress()

        elif self.current_map == "inside":
            self.stage.screen.blit(self.images.background_image, (0, 0))

        elif self.current_map == "outside2":
            self.stage.screen.blit(self.images.second_background_image, (0, 0))

            has_spaceship_item = 'spaceship' in self.stage.inventory
            is_completed = len(self.stage.spaceship_assembly_storage) == MAX_SPACESHIP_PARTS
            
            if has_spaceship_item or self.stage.spaceship_assembly_storage:
                if is_completed:
                    self.draw_pulsating_spaceship()

    def draw_tree_progress(self):
        if self.is_tree_pressing:
            elapsed = pygame.time.get_ticks() - self.tree_press_start_time
            progress = min(1.0, elapsed / GATHER_DURATION)
            
            bar_width = 100
            bar_height = 10
            bar_x = TREE_AREA.x + TREE_AREA.width // 2 - bar_width // 2
            bar_y = TREE_AREA.y - bar_height - 5
            
            pygame.draw.rect(self.stage.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(self.stage.screen, GREEN, (bar_x, bar_y, bar_width * progress, bar_height))

    def draw_dropped_items(self):
        if self.current_map == "outside1":
            for item in self.stage.dropped_items:
                item_draw = self.images.item_images.get(item['item_name'])
                if item_draw:
                    self.stage.screen.blit(item_draw, item['rect'])

    def draw_pulsating_spaceship(self):
        original_w, original_h = self.images.spaceship_completed_image.get_size()
        new_w = int(original_w * self.current_scale)
        new_h = int(original_h * self.current_scale)
        
        scaled_image = pygame.transform.scale(self.images.spaceship_completed_image, (new_w, new_h))
        
        center_x = SPACESHIP_AREA.x + SPACESHIP_AREA.width // 2
        top_y = SPACESHIP_AREA.y - new_h - 50
        draw_x = center_x - new_w // 2
        draw_y = top_y
        
        self.stage.screen.blit(scaled_image, (draw_x, draw_y))

    def draw_spaceship_gauge(self):

        if self.stage.player.is_walking_into_spaceship or self.stage.player.is_flying_animation_active:
            return

        if not ('spaceship' in self.stage.inventory or self.stage.spaceship_assembly_storage):
            return

        part_count = len(self.stage.spaceship_assembly_storage)
        is_completed = part_count == MAX_SPACESHIP_PARTS

        gauge_width = 280
        gauge_height = 20
        
        gauge_x = SPACESHIP_AREA.x
        gauge_y = SPACESHIP_AREA.y + SPACESHIP_AREA.height + 10 
        
        gauge_rect_outer = pygame.Rect(gauge_x, gauge_y, gauge_width, gauge_height)
        pygame.draw.rect(self.stage.screen, BLACK, gauge_rect_outer, 3)

        progress_ratio = min(1.0, part_count / MAX_SPACESHIP_PARTS)
        filled_width = int(gauge_width * progress_ratio)
        gauge_color = GREEN if is_completed else RED

        gauge_rect_filled = pygame.Rect(gauge_x, gauge_y, filled_width, gauge_height)
        pygame.draw.rect(self.stage.screen, gauge_color, gauge_rect_filled)
        
        font = pygame.font.Font(None, 30)
        progress_text = font.render(f"{part_count}/{MAX_SPACESHIP_PARTS}", True, WHITE)
        text_x = gauge_x + gauge_width // 2 - progress_text.get_width() // 2
        text_y = gauge_y + gauge_height // 2 - progress_text.get_height() // 2
        self.stage.screen.blit(progress_text, (text_x, text_y))
'''