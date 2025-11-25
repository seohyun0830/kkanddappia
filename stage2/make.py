import pygame
from .setting import *

class Crafting:
    def __init__(self, stage):
        self.stage = stage
        self.images = stage.images
        
        self.crafted_item_display = None 
        self.popup_font = pygame.font.Font(None, 50)

    def draw_normal_crafting(self):
        # 6*6
        self.stage.screen.blit(self.images.make2_image, (MAKE2_IMAGE_X, MAKE2_IMAGE_Y))

        for i in range(len(self.stage.crafting_table)):
            item_name = self.stage.crafting_table[i]
            if item_name is not None:
                slot_x, slot_y = CRAFT_SLOT_POSITIONS[i]
                item_draw = self.images.item_images.get(item_name)
                if item_draw:
                    self.stage.screen.blit(item_draw, (slot_x, slot_y))

    def draw_spaceship_crafting(self):
        # 4*4
        self.stage.screen.blit(self.images.spaceship_make_image, (SPACESHIP_MAKE_IMAGE_X, SPACESHIP_MAKE_IMAGE_Y))

        for item_name, slot_indices in self.stage.assembled_slot_map.items():
            item_draw_original = self.images.item_images.get(item_name)
            
            if item_draw_original:
                item_draw_scaled = pygame.transform.scale(item_draw_original, (SPACESHIP_ITEM_SIZE, SPACESHIP_ITEM_SIZE))
                
                for slot_index in slot_indices:
                    if slot_index < len(SPACESHIP_SLOT_POSITIONS):
                        slot_x, slot_y = SPACESHIP_SLOT_POSITIONS[slot_index]
                        offset = (SLOT_SIZE_PX - SPACESHIP_ITEM_SIZE) // 2
                        draw_x = slot_x + offset
                        draw_y = slot_y + offset
                        self.stage.screen.blit(item_draw_scaled, (draw_x, draw_y))

    def draw_result_popup(self):
        if self.crafted_item_display:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.stage.screen.blit(overlay, (0, 0))
            
            item_img = self.images.item_images.get(self.crafted_item_display)
            if item_img:
                scaled_img = pygame.transform.scale(item_img, (200, 200))
                img_x = SCREEN_WIDTH // 2 - 100
                img_y = SCREEN_HEIGHT // 2 - 100
                self.stage.screen.blit(scaled_img, (img_x, img_y))
            
            text_surf = self.popup_font.render("SUCCESS", True, YELLOW)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
            self.stage.screen.blit(text_surf, text_rect)
            
            click_text = self.popup_font.render("Click to Get", True, WHITE)
            click_rect = click_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
            self.stage.screen.blit(click_text, click_rect)

    def handle_drag_start(self, mouse_pos):
        if MAKE_BUTTON_AREA.collidepoint(mouse_pos):
            self.process_crafting()
            return

        for i in range(len(self.stage.crafting_table)):
            if self.stage.crafting_table[i] is not None:
                if CRAFT_SLOT_RECTS[i].collidepoint(mouse_pos):
                    self.stage.drag_item = self.stage.crafting_table[i]
                    self.stage.crafting_table[i] = None
                    
                    self.stage.is_drag = True
                    self.stage.drag_item_original = f"crafting_slot_{i}"
                    
                    self.stage.drag_offset_x = mouse_pos[0] - CRAFT_SLOT_RECTS[i].x
                    self.stage.drag_offset_y = mouse_pos[1] - CRAFT_SLOT_RECTS[i].y
                    break

    def handle_drop_in_crafting(self, mouse_pos):
        for i in range(len(CRAFT_SLOT_RECTS)):
            if CRAFT_SLOT_RECTS[i].collidepoint(mouse_pos):
                if self.stage.crafting_table[i] is None:
                    self.stage.crafting_table[i] = self.stage.drag_item
                    return True
                else:
                    return False
        return False

    def process_crafting(self):
        found_recipe = False
        
        for recipe_data in RECIPES:
            if self.stage.crafting_table == recipe_data['recipe']:
                result_item = recipe_data['result']
                
                if result_item:
                    self.crafted_item_display = result_item
                
                self.stage.crafting_table = [None] * 9
                found_recipe = True
                break
        
        if not found_recipe:
            self.stage.game_over = True
            self.stage.close_all_popups()

            if self.stage.sounds.bomb_sound:
                self.stage.sounds.bomb_sound.play()

    def confirm_crafting_result(self):
        if self.crafted_item_display:
            self.stage.inventory.append(self.crafted_item_display)
            self.crafted_item_display = None
            return True
        return False

    def handle_drop_in_spaceship_window(self, mouse_pos):
        if SPACESHIP_DROP_AREA.collidepoint(mouse_pos):
            return self.add_part_to_spaceship(self.stage.drag_item)
        return False

    def handle_drop_on_spaceship_area(self, mouse_pos):
        if SPACESHIP_AREA.collidepoint(mouse_pos):
            return self.add_part_to_spaceship(self.stage.drag_item)
        return False

    def add_part_to_spaceship(self, item_name):
        required_count = SPACESHIP_REQUIREMENTS.get(item_name, 0)
        current_count = self.stage.spaceship_assembly_storage.count(item_name)
        
        if required_count > 0 and current_count < required_count:
            self.stage.spaceship_assembly_storage.append(item_name)
            
            assigned_slots = sum(self.stage.assembled_slot_map.values(), [])
            
            for slot_index in range(MAX_SPACESHIP_PARTS):
                if slot_index not in assigned_slots:
                    if item_name not in self.stage.assembled_slot_map:
                        self.stage.assembled_slot_map[item_name] = []
                    
                    self.stage.assembled_slot_map[item_name].append(slot_index)
                    break
            return True
        return False

    def is_click_inside_ui(self, mouse_pos):
        make_rect = pygame.Rect(MAKE2_IMAGE_X, MAKE2_IMAGE_Y, IMG_SIZE_MAKE2[0], IMG_SIZE_MAKE2[1])
        return make_rect.collidepoint(mouse_pos)

    def is_click_inside_spaceship_ui(self, mouse_pos):
        rect = pygame.Rect(SPACESHIP_MAKE_IMAGE_X, SPACESHIP_MAKE_IMAGE_Y, IMG_SIZE_SPACESHIP_MAKE[0], IMG_SIZE_SPACESHIP_MAKE[1])
        return rect.collidepoint(mouse_pos)