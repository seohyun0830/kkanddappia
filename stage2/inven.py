import pygame
from collections import Counter
from .setting import *

class Inventory:
    def __init__(self, stage):
        self.stage = stage
        self.images = stage.images
        self.font = pygame.font.Font('DungGeunMO.ttf', 24)
        
        # 페이지(1:자원, 2:우주선 부품)
        self.current_page = 1
        self.just_turned_page = False

    def get_stacked_inventory(self, flat_inventory):
        counts = Counter(flat_inventory)
        stacked_inventory = []
        sorted_item_names = sorted(counts.keys())
        
        for item_name in sorted_item_names:
            if item_name in self.images.item_images:
                total_count = counts[item_name]
                while total_count > 0:
                    stack_count = min(total_count, MAX_STACK_SIZE)
                    stacked_inventory.append({'name': item_name, 'count': stack_count})
                    total_count -= stack_count
        return stacked_inventory

    def get_current_page_items(self):
        full_stacked = self.get_stacked_inventory(self.stage.inventory)
        page_items = []
        
        for item in full_stacked:
            name = item['name']
            is_spaceship_part = name in SPACESHIP_PART_NAMES
            
            if self.current_page == 1:
                if not is_spaceship_part:
                    page_items.append(item)
            elif self.current_page == 2:
                if is_spaceship_part:
                    page_items.append(item)
                    
        return page_items

    def draw(self, x_pos):
        if self.current_page == 1:
            self.stage.screen.blit(self.images.inven_image, (x_pos, INV_DRAW_Y))
        else:
            self.stage.screen.blit(self.images.inven2_image, (x_pos, INV_DRAW_Y))

        visible_items = self.get_current_page_items()
        shift_x = x_pos - INVEN_IMAGE_X 

        if self.current_page == 1:
            slot_positions = INVENTORY_SLOT_POSITIONS
            draw_size = ITEM_SIZE
        else:
            slot_positions = INVENTORY_PAGE2_SLOT_POSITIONS
            draw_size = SPACESHIP_ITEM_SIZE * 2 # 2배 크기로 그리기

        limit = min(len(visible_items), len(slot_positions))
        
        for i in range(limit):
            base_x, base_y = slot_positions[i]
            
            draw_x = base_x + shift_x
            draw_y = base_y
            
            item_data = visible_items[i]
            item_name = item_data['name']
            item_count = item_data['count']
            
            item_img = self.images.item_images.get(item_name)

            if item_img:
                if self.current_page == 2:
                    item_img = pygame.transform.scale(item_img, (draw_size, draw_size))

                self.stage.screen.blit(item_img, (draw_x, draw_y))
                
                if item_name in ['fire', 'water']:
                    count_text = self.font.render("", True, YELLOW) 
                else:
                    count_text = self.font.render(f"x{item_count}", True, YELLOW)
                
                text_x = draw_x + draw_size - count_text.get_width() - 5
                text_y = draw_y + draw_size - count_text.get_height() - 5
                self.stage.screen.blit(count_text, (text_x, text_y))

    def handle_drag_start(self, mouse_pos):
        """드래그 시작 (클릭 판정 영역 수정)"""
        if self.just_turned_page:
            self.just_turned_page = False
            return False

        if self.stage.is_crafting_open:
            current_shift_x = 0
        else:
            current_shift_x = INV_CENTER_SHIFT_X
            
        visible_items = self.get_current_page_items()
        
        # [수정] 페이지에 따라 클릭 판정 영역(Hitbox) 크기를 다르게 설정
        if self.current_page == 1:
            base_positions = INVENTORY_SLOT_POSITIONS
            hitbox_size = ITEM_SIZE
        else:
            base_positions = INVENTORY_PAGE2_SLOT_POSITIONS
            # draw 함수에서 그리는 크기와 똑같이 설정 (2배)
            hitbox_size = SPACESHIP_ITEM_SIZE * 2 

        limit = min(len(visible_items), len(base_positions))
        
        for i in range(limit):
            # 좌표 리스트에서 기본 위치 가져오기
            base_x, base_y = base_positions[i]
            
            # 현재 UI 위치에 맞게 이동시킨 Rect 생성
            slot_rect = pygame.Rect(base_x + current_shift_x, base_y, hitbox_size, hitbox_size)
            
            if slot_rect.collidepoint(mouse_pos):
                item_name = visible_items[i]['name']
                
                try:
                    flat_index = self.stage.inventory.index(item_name)
                    
                    self.stage.is_drag = True
                    self.stage.drag_item = self.stage.inventory[flat_index]
                    
                    if item_name not in ['fire', 'water']:
                        self.stage.inventory.pop(flat_index)
                    
                    self.stage.drag_item_original = f"inventory_slot_{i}_p{self.current_page}"
                    
                    # 오프셋 계산
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
                 if self.stage.drag_item not in ['fire', 'water']:
                     self.stage.inventory.append(self.stage.drag_item)
                 self.stage.reset_drag()
                 
            return True
        return False

    def is_click_inside_ui(self, mouse_pos):
        """UI 내부 클릭 확인 및 페이지 넘김 처리"""
        current_x = INVEN_IMAGE_X if self.stage.is_crafting_open else CENTERED_INV_X
        inven_rect = pygame.Rect(current_x, INV_DRAW_Y, IMG_SIZE_INVEN[0], IMG_SIZE_INVEN[1])
        
        if not inven_rect.collidepoint(mouse_pos):
            return False

        # [수정] 슬롯 클릭 감지 (페이지 넘김 오작동 방지용)
        shift_x = current_x - INVEN_IMAGE_X
        
        if self.current_page == 1:
            base_positions = INVENTORY_SLOT_POSITIONS
            hitbox_size = ITEM_SIZE
        else:
            base_positions = INVENTORY_PAGE2_SLOT_POSITIONS
            hitbox_size = SPACESHIP_ITEM_SIZE * 2 # 여기도 2배 크기로 맞춰야 함
            
        for pos in base_positions:
            base_x, base_y = pos
            slot_rect = pygame.Rect(base_x + shift_x, base_y, hitbox_size, hitbox_size)
            
            if slot_rect.collidepoint(mouse_pos):
                self.just_turned_page = False
                return True # 슬롯 위를 클릭했다면 페이지 안 넘김

        # 빈 공간 클릭 시 페이지 넘김
        center_x = inven_rect.centerx
        if mouse_pos[0] < center_x: 
            if self.current_page > 1:
                self.current_page -= 1
                self.just_turned_page = True
        else: 
            if self.current_page < 2:
                self.current_page += 1
                self.just_turned_page = True
        
        return True

'''

class Inventory:
    def __init__(self, stage):
        self.stage = stage
        self.images = stage.images
        self.font = pygame.font.Font(None, 24)
        
        # 페이지(1:자원, 2:우주선 부품)
        self.current_page = 1
        self.just_turned_page = False

    def get_stacked_inventory(self, flat_inventory):
        counts = Counter(flat_inventory)
        stacked_inventory = []
        sorted_item_names = sorted(counts.keys())
        
        for item_name in sorted_item_names:
            if item_name in self.images.item_images:
                total_count = counts[item_name]
                while total_count > 0:
                    stack_count = min(total_count, MAX_STACK_SIZE)
                    stacked_inventory.append({'name': item_name, 'count': stack_count})
                    total_count -= stack_count
        return stacked_inventory

    def get_current_page_items(self):
        full_stacked = self.get_stacked_inventory(self.stage.inventory)
        page_items = []
        
        for item in full_stacked:
            name = item['name']
            # settings.py에 정의된 우주선 부품 리스트에 있는지 확인
            is_spaceship_part = name in SPACESHIP_PART_NAMES
            
            if self.current_page == 1:
                if not is_spaceship_part:
                    page_items.append(item)
            elif self.current_page == 2:
                if is_spaceship_part:
                    page_items.append(item)
                    
        return page_items

    def draw(self, x_pos):

        if self.current_page == 1:
            self.stage.screen.blit(self.images.inven_image, (x_pos, INV_DRAW_Y))
        else:
            self.stage.screen.blit(self.images.inven2_image, (x_pos, INV_DRAW_Y))

        visible_items = self.get_current_page_items()
        shift_x = x_pos - INVEN_IMAGE_X 

        if self.current_page == 1:
            slot_positions = INVENTORY_SLOT_POSITIONS
            draw_size = ITEM_SIZE
        else:
            slot_positions = INVENTORY_PAGE2_SLOT_POSITIONS
            draw_size = SPACESHIP_ITEM_SIZE*2

        limit = min(len(visible_items), len(slot_positions))
        
        for i in range(limit):
            base_x, base_y = slot_positions[i]
            draw_x = base_x + shift_x
            draw_y = base_y
            
            item_data = visible_items[i]
            item_name = item_data['name']
            item_count = item_data['count']
            
            item_img = self.images.item_images.get(item_name)

            if item_img:
                if self.current_page == 2:
                    item_img = pygame.transform.scale(item_img, (draw_size, draw_size))

                self.stage.screen.blit(item_img, (draw_x, draw_y))
                
                # 불/물 무한
                if item_name in ['fire', 'water']:
                    count_text = self.font.render("", True, YELLOW) 
                else:
                    count_text = self.font.render(f"x{item_count}", True, YELLOW)
                
                text_x = draw_x + draw_size - count_text.get_width() - 5
                text_y = draw_y + draw_size - count_text.get_height() - 5
                self.stage.screen.blit(count_text, (text_x, text_y))

    def handle_drag_start(self, mouse_pos):
        if self.just_turned_page:
            self.just_turned_page = False
            return False

        if self.stage.is_crafting_open:
            current_shift_x = 0
        else:
            current_shift_x = INV_CENTER_SHIFT_X
            
        visible_items = self.get_current_page_items()
        
        if self.current_page == 1:
            base_rects = INVENTORY_SLOT_RECTS
        else:
            base_rects = INVENTORY_PAGE2_SLOT_RECTS

        limit = min(len(visible_items), len(base_rects))
        
        for i in range(limit):
            slot_rect = base_rects[i].move(current_shift_x, 0)
            
            if slot_rect.collidepoint(mouse_pos):
                item_name = visible_items[i]['name']
                
                try:
                    flat_index = self.stage.inventory.index(item_name)
                    
                    self.stage.is_drag = True
                    self.stage.drag_item = self.stage.inventory[flat_index]
                    
                    if item_name not in ['fire', 'water']:
                        self.stage.inventory.pop(flat_index)
                    
                    self.stage.drag_item_original = f"inventory_slot_{i}_p{self.current_page}"
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
                self.current_page = 1
            
            self.stage.is_crafting_open = False
            self.stage.is_spaceship_crafting_open = False
            
            if self.stage.open_door:
                self.stage.dic_open = False
                
            if self.stage.is_drag:
                 if self.stage.drag_item not in ['fire', 'water']:
                     self.stage.inventory.append(self.stage.drag_item)
                 self.stage.reset_drag()
                 
            return True
        return False

    def is_click_inside_ui(self, mouse_pos):
        """UI 내부 클릭 확인 및 페이지 넘김 처리 (사전 방식)"""
        current_x = INVEN_IMAGE_X if self.stage.is_crafting_open else CENTERED_INV_X
        inven_rect = pygame.Rect(current_x, INV_DRAW_Y, IMG_SIZE_INVEN[0], IMG_SIZE_INVEN[1])
        
        if not inven_rect.collidepoint(mouse_pos):
            return False

        #슬롯 클릭
        shift_x = current_x - INVEN_IMAGE_X
        if self.current_page == 1:
            slot_rects = INVENTORY_SLOT_RECTS
        else:
            slot_rects = INVENTORY_PAGE2_SLOT_RECTS
            
        for rect in slot_rects:
            shifted_rect = rect.move(shift_x, 0)
            if shifted_rect.collidepoint(mouse_pos):
                self.just_turned_page = False
                return True

        #빈 공간 클릭
        center_x = inven_rect.centerx
        if mouse_pos[0] < center_x: 
            if self.current_page > 1:
                self.current_page -= 1
                self.just_turned_page = True
        else: 
            if self.current_page < 2:
                self.current_page += 1
                self.just_turned_page = True
        
        return True
        '''