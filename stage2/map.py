import pygame
import math
import random
from .setting import *

class MapManager:
    def __init__(self, stage):
        self.stage = stage
        self.images = stage.images
        
        self.current_map = "outside1"
        self.is_tree_pressing = False
        self.tree_press_start_time = 0
        
        self.pulsate_time_start = pygame.time.get_ticks()
        self.current_scale = 1.0

        # 우주선 조각 랜덤 순서
        self.part_reveal_order = list(range(9))
        random.shuffle(self.part_reveal_order)

        # [추가] 쪽지 시스템 초기화
        self.start_time = pygame.time.get_ticks()
        self.spawned_notes = [] 
        self.next_note_index = 0

        # [최적화] 폰트 미리 로드 (draw에서 매번 로드하면 렉 걸림)
        try:
            self.font = pygame.font.Font("DungGeunMO.ttf", 30)
        except:
            self.font = pygame.font.Font(None, 30)

    def update(self):
        current_time = pygame.time.get_ticks()

        # [추가] 1. 시간에 따라 쪽지 생성
        if not self.stage.is_easy_mode:
            if self.next_note_index < len(NOTE_DATA):
                # (인덱스+1) * 간격 만큼 시간이 지나면 생성
                if current_time - self.start_time > (self.next_note_index + 1) * NOTE_APPEAR_INTERVAL:
                    note_info = NOTE_DATA[self.next_note_index]
                    
                    new_note = {
                        'map': note_info['map'],
                        'rect': pygame.Rect(note_info['pos'][0], note_info['pos'][1], PAPER_SIZE, PAPER_SIZE)
                    }
                    self.spawned_notes.append(new_note)
                    self.next_note_index += 1

        # 2. 나무 캐기 완료 체크
        if self.current_map == "outside1" and self.is_tree_pressing:
            if current_time - self.tree_press_start_time >= GATHER_DURATION:
                self.drop_wood()
                self.is_tree_pressing = False
                self.tree_press_start_time = 0
                
                if self.stage.sounds.tree_sound:
                    self.stage.sounds.tree_sound.stop()

        # 3. 우주선 깜박임
        time_factor = (current_time - self.pulsate_time_start) * PULSATE_SPEED
        scale_offset = (math.sin(time_factor) + 1) / 2
        self.current_scale = PULSATE_MIN_SCALE + scale_offset * (PULSATE_MAX_SCALE - PULSATE_MIN_SCALE)

    def is_player_near(self, target_rect):
        player_center = self.stage.player.rect.center
        target_center = target_rect.center
        
        distance = math.hypot(player_center[0] - target_center[0], player_center[1] - target_center[1])
        
        return distance <= INTERACTION_RANGE

    def handle_click(self, mouse_pos):
        if self.current_map == "outside1":
            if TREE_AREA.collidepoint(mouse_pos):
                if self.is_player_near(TREE_AREA):
                    if not self.is_tree_pressing:
                        self.is_tree_pressing = True
                        self.tree_press_start_time = pygame.time.get_ticks()
                        if self.stage.sounds.tree_sound:
                            self.stage.sounds.tree_sound.play(loops=-1)
                return

            # 문 클릭
            if OUTSIDE_DOOR_AREA.collidepoint(mouse_pos):
                if self.is_player_near(OUTSIDE_DOOR_AREA):
                    self.current_map = "inside"
                    self.stage.player.x = 100
                    self.stage.player.reset_animation()
                return
            
            # 지하 이동
            if STAGE1_AREA.collidepoint(mouse_pos):
                if self.is_player_near(STAGE1_AREA):
                    if not self.stage.player.is_fading_out:
                        self.stage.player.is_fading_out = True
                        self.stage.player.alpha = 255
                return

        elif self.current_map == "inside":
            if DIC_AREA.collidepoint(mouse_pos):
                # 거리 체크 추가 (선택사항)
                # if self.is_player_near(DIC_AREA):
                self.stage.dic_open = not self.stage.dic_open
                if self.stage.dic_open:
                    self.stage.close_all_popups()
                    self.stage.dic_open = True
                return
            
            if CLICK_AREA.collidepoint(mouse_pos):
                # if self.is_player_near(CLICK_AREA):
                self.stage.open_door = True
                self.stage.is_crafting_open = True
                self.stage.dic_open = False
                return

        elif self.current_map == "outside2":
            # 외부 제작대 -> 내부로 이동
            if OUTSIDE_MAKE_AREA.collidepoint(mouse_pos):
                if self.is_player_near(OUTSIDE_MAKE_AREA):
                    self.current_map = "inside"
                    self.stage.player.x = SCREEN_WIDTH - 150 
                    self.stage.player.reset_animation()

                    self.stage.open_door = False
                    self.stage.is_crafting_open = False
                    self.stage.dic_open = False
                return
            
            # 우주선 조립
            if SPACESHIP_AREA.collidepoint(mouse_pos):
                if self.is_player_near(SPACESHIP_AREA):
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

    def check_item_pickup(self, player_rect):
        """자동 습득 (아이템 + 쪽지)"""
        # 1. 아이템 습득
        for i in range(len(self.stage.dropped_items) - 1, -1, -1):
            item = self.stage.dropped_items[i]
            if player_rect.colliderect(item['rect']):
                self.stage.inventory.append(item['item_name'])
                self.stage.dropped_items.pop(i)

        # 2. [추가] 쪽지 습득 (현재 맵에 있는 것만)
        if not self.stage.is_easy_mode:
            for i in range(len(self.spawned_notes) - 1, -1, -1):
                note = self.spawned_notes[i]
                if note['map'] == self.current_map:
                    if player_rect.colliderect(note['rect']):
                        self.spawned_notes.pop(i)
                        self.stage.collected_notes_count += 1
                        # print(f"쪽지 획득! 해금 페이지: {self.stage.collected_notes_count}")

    def drop_wood(self):
        wood_drop_x = TREE_AREA.x + TREE_AREA.width // 2 - ITEM_SIZE // 2
        wood_drop_y = self.stage.player.y + self.stage.player.image.get_height()
        self.stage.dropped_items.append({
            'item_name': 'wood',
            'rect': pygame.Rect(wood_drop_x, wood_drop_y - 15, ITEM_SIZE, ITEM_SIZE)
        })

    def draw(self, timer=None):
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
            
            has_parts = len(self.stage.spaceship_assembly_storage) > 0
            has_item = 'spaceship' in self.stage.inventory
            
            if has_parts or has_item:
                is_completed = len(self.stage.spaceship_assembly_storage) == MAX_SPACESHIP_PARTS
                
                if is_completed:
                    self.draw_pulsating_spaceship()
                else:
                    self.draw_progress_spaceship()
        
        # [추가] 쪽지 그리기
        if not self.stage.is_easy_mode:
            for note in self.spawned_notes:
                if note['map'] == self.current_map:
                    self.stage.screen.blit(self.images.paper_image, note['rect'].topleft)

        # 타이머 표시 (timer 객체가 넘어왔을 때만)
        if timer:
            timeText = timer.get_time_text()
            self.stage.screen.blit(timeText, (10, 10))

    def draw_progress_spaceship(self):
        current_parts = len(self.stage.spaceship_assembly_storage)
        if current_parts == 0: return

        # 비율 계산
        ratio = current_parts / MAX_SPACESHIP_PARTS
        num_pieces_to_show = int(ratio * 9)
        
        if current_parts > 0 and num_pieces_to_show == 0:
            num_pieces_to_show = 1

        cols = 3
        SCALE_FACTOR = 0.3
        
        if not self.images.spaceship_parts:
            return

        sample = self.images.spaceship_parts[0]
        part_w = int(sample.get_width() * SCALE_FACTOR)
        part_h = int(sample.get_height() * SCALE_FACTOR)
        
        total_w = part_w * 3
        total_h = part_h * 3
        
        center_x = SPACESHIP_AREA.x + SPACESHIP_AREA.width // 2
        top_y = SPACESHIP_AREA.y - total_h - 40
        
        draw_base_x = center_x - total_w // 2
        draw_base_y = top_y
        
        # 랜덤 순서대로 그리기
        for i in range(num_pieces_to_show):
            if i >= len(self.part_reveal_order): break
            
            part_idx = self.part_reveal_order[i]
            
            if part_idx < len(self.images.spaceship_parts):
                part_img_original = self.images.spaceship_parts[part_idx]
                part_img_scaled = pygame.transform.scale(part_img_original, (part_w, part_h))
                
                r = part_idx // cols
                c = part_idx % cols
                
                px = draw_base_x + (c * part_w)
                py = draw_base_y + (r * part_h)
                
                self.stage.screen.blit(part_img_scaled, (px, py))

    def draw_pulsating_spaceship(self):
        SCALE_FACTOR = 0.7 # 크기 비율 맞추기
        original_w, original_h = self.images.spaceship_completed_image.get_size()
        
        base_w = int(original_w * SCALE_FACTOR)
        base_h = int(original_h * SCALE_FACTOR)
        
        new_w = int(base_w * self.current_scale)
        new_h = int(base_h * self.current_scale)
        
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
        
        percent = int(progress_ratio * 100)
        # [최적화] self.font 사용
        progress_text = self.font.render(f"{percent}%", True, WHITE)
        
        text_x = gauge_x + gauge_width // 2 - progress_text.get_width() // 2
        text_y = gauge_y + gauge_height // 2 - progress_text.get_height() // 2
        self.stage.screen.blit(progress_text, (text_x, text_y))

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

'''
class MapManager:
    def __init__(self, stage):
        self.stage = stage
        self.images = stage.images
        
        self.current_map = "outside1"
        self.is_tree_pressing = False
        self.tree_press_start_time = 0
        
        self.pulsate_time_start = pygame.time.get_ticks()
        self.current_scale = 1.0

        self.part_reveal_order = list(range(MAX_SPACESHIP_PARTS))
        random.shuffle(self.part_reveal_order)

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.current_map == "outside1" and self.is_tree_pressing:
            if current_time - self.tree_press_start_time >= GATHER_DURATION:
                self.drop_wood()
                self.is_tree_pressing = False
                self.tree_press_start_time = 0
                
                if self.stage.sounds.tree_sound:
                    self.stage.sounds.tree_sound.stop()

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
            if DIC_AREA.collidepoint(mouse_pos):
                self.stage.dic_open = not self.stage.dic_open
                if self.stage.dic_open:
                    self.stage.close_all_popups()
                    self.stage.dic_open = True
                return

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
        """[수정됨] 우주선 아이템 없이도 미완성이면 창이 열리도록 변경"""
        is_completed = len(self.stage.spaceship_assembly_storage) == MAX_SPACESHIP_PARTS
        
        if is_completed:
            self.stage.close_all_popups()
            self.stage.player.start_walking_into_spaceship()
            return

        if not is_completed:
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
            
            has_parts = len(self.stage.spaceship_assembly_storage) > 0
            
            if has_parts:
                is_completed = len(self.stage.spaceship_assembly_storage) == MAX_SPACESHIP_PARTS
                
                if is_completed:
                    self.draw_pulsating_spaceship()
                else:
                    self.draw_progress_spaceship()

    def draw_progress_spaceship(self):
        current_parts = len(self.stage.spaceship_assembly_storage)
        if current_parts == 0:
            return

        full_image = self.images.spaceship_completed_image
        w, h = full_image.get_size()
        
        ratio = current_parts / MAX_SPACESHIP_PARTS
        visible_height = int(h * ratio)
        src_rect = pygame.Rect(0, h - visible_height, w, visible_height)
        
        center_x = SPACESHIP_AREA.x + SPACESHIP_AREA.width // 2
        top_y = SPACESHIP_AREA.y - h - 50 
        draw_x = center_x - w // 2
        draw_y = top_y + (h - visible_height)
        
        self.stage.screen.blit(full_image, (draw_x, draw_y), src_rect)

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

        if not self.stage.spaceship_assembly_storage:
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

'''


'''
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