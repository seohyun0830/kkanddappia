import pygame
import math
from .setting import *

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