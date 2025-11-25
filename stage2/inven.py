import pygame
from collections import Counter
from setting import *

class Inventory:
    def __init__(self, stage):
        self.stage = stage
        self.images = stage.images
        
        self.font = pygame.font.Font(None, 24)

    def get_stacked_inventory(self, flat_inventory):
        counts = Counter(flat_inventory)
        stacked_inventory = []
        sorted_item_names = sorted(counts.keys())
        
        for item_name in sorted_item_names:
            # 이미지 리소스가 있는 아이템만 처리
            if item_name in self.images.item_images:
                total_count = counts[item_name]
                while total_count > 0:
                    stack_count = min(total_count, MAX_STACK_SIZE)
                    stacked_inventory.append({'name': item_name, 'count': stack_count})
                    total_count -= stack_count
                    
        return stacked_inventory

    def draw(self, x_pos):
        self.stage.screen.blit(self.images.inven_image, (x_pos, INV_DRAW_Y))

        stacked_inventory = self.get_stacked_inventory(self.stage.inventory)
        
        shift_x = x_pos - INVEN_IMAGE_X 

        limit = min(len(stacked_inventory), len(INVENTORY_SLOT_POSITIONS))
        
        for i in range(limit):
            base_x, base_y = INVENTORY_SLOT_POSITIONS[i]
            
            draw_x = base_x + shift_x
            draw_y = base_y
            
            item_data = stacked_inventory[i]
            item_name = item_data['name']
            item_count = item_data['count']
            
            item_img = self.images.item_images.get(item_name)
            if item_img:
                self.stage.screen.blit(item_img, (draw_x, draw_y))
                
                count_text = self.font.render(f"x{item_count}", True, YELLOW)
                text_x = draw_x + ITEM_SIZE - count_text.get_width() - 5
                text_y = draw_y + ITEM_SIZE - count_text.get_height() - 5
                self.stage.screen.blit(count_text, (text_x, text_y))

    def handle_drag_start(self, mouse_pos):

        if self.stage.is_crafting_open:
            current_shift_x = 0
        else:
            current_shift_x = INV_CENTER_SHIFT_X
            
        stacked_inventory = self.get_stacked_inventory(self.stage.inventory)
        limit = min(len(stacked_inventory), len(INVENTORY_SLOT_RECTS))
        
        for i in range(limit):
            slot_rect = INVENTORY_SLOT_RECTS[i].move(current_shift_x, 0)
            
            if self.stage.is_spaceship_crafting_open:
                pass 

            if slot_rect.collidepoint(mouse_pos):
                item_name = stacked_inventory[i]['name']
                
                try:
                    flat_index = self.stage.inventory.index(item_name)
                    
                    self.stage.is_drag = True
                    self.stage.drag_item = self.stage.inventory[flat_index]
                    self.stage.inventory.pop(flat_index)
                    self.stage.drag_item_original = f"inventory_slot_{i}"
                    
                    self.stage.drag_offset_x = mouse_pos[0] - slot_rect.x
                    self.stage.drag_offset_y = mouse_pos[1] - slot_rect.y
                    
                    return True
                except ValueError:
                    pass
                
                break
        
        return False

    def handle_icon_click(self, mouse_pos):
        if BAG_ICON_AREA.collidepoint(mouse_pos):
            if self.stage.open_door and not self.stage.is_crafting_open:
                self.stage.open_door = False
            else:
                self.stage.open_door = True
            
            self.stage.is_crafting_open = False
            self.stage.is_spaceship_crafting_open = False
            
            if self.stage.open_door:
                self.stage.dic_open = False
                
            if self.stage.is_drag:
                 self.stage.inventory.append(self.stage.drag_item)
                 self.stage.reset_drag()
                 
            return True
        return False

    def is_click_inside_ui(self, mouse_pos):

        current_x = INVEN_IMAGE_X if self.stage.is_crafting_open else CENTERED_INV_X
        
        inven_rect = pygame.Rect(current_x, INV_DRAW_Y, IMG_SIZE_INVEN[0], IMG_SIZE_INVEN[1])
        return inven_rect.collidepoint(mouse_pos)