import pygame
from collections import Counter
from setting import *

class Inventory:
    def __init__(self, stage):
        self.stage = stage
        self.images = stage.images
        self.font = pygame.font.Font(None, 24)
        
        # 현재 인벤토리 페이지 (1: 재료 / 2: 우주선 부품)
        self.current_page = 1
        
        # 페이지 전환 안전장치 (페이지 넘김과 동시에 아이템이 집히는 것 방지)
        self.just_turned_page = False

    def get_stacked_inventory(self, flat_inventory):
        """전체 인벤토리를 스택(개수) 형태로 변환"""
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
        """현재 페이지에 보여줄 아이템만 필터링해서 반환"""
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
        """현재 페이지에 맞는 배경과 아이템 그리기"""
        # 1. 배경 그리기
        if self.current_page == 1:
            self.stage.screen.blit(self.images.inven_image, (x_pos, INV_DRAW_Y))
        else:
            self.stage.screen.blit(self.images.inven2_image, (x_pos, INV_DRAW_Y))

        # 2. 현재 페이지 아이템 가져오기
        visible_items = self.get_current_page_items()
        shift_x = x_pos - INVEN_IMAGE_X 

        # 3. 슬롯 좌표 및 크기 선택
        if self.current_page == 1:
            slot_positions = INVENTORY_SLOT_POSITIONS
            draw_size = ITEM_SIZE
        else:
            slot_positions = INVENTORY_PAGE2_SLOT_POSITIONS
            draw_size = SPACESHIP_ITEM_SIZE

        # 4. 아이템 그리기
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
                
                count_text = self.font.render(f"x{item_count}", True, YELLOW)
                text_x = draw_x + draw_size - count_text.get_width() - 5
                text_y = draw_y + draw_size - count_text.get_height() - 5
                self.stage.screen.blit(count_text, (text_x, text_y))

        # [삭제됨] 페이지 전환 버튼 그리기 제거 (화면 클릭으로 대체)

    def handle_drag_start(self, mouse_pos):
        """현재 페이지의 아이템 드래그"""
        
        # [안전장치] 방금 페이지를 넘겼다면 이번 클릭은 드래그로 처리하지 않음
        if self.just_turned_page:
            self.just_turned_page = False
            return False

        current_shift_x = 0 if self.stage.is_crafting_open else INV_CENTER_SHIFT_X
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
                 self.stage.inventory.append(self.stage.drag_item)
                 self.stage.reset_drag()
            return True
        return False

    def is_click_inside_ui(self, mouse_pos):
        """
        UI 내부 클릭 확인 및 페이지 넘김 처리 (사전 방식)
        - 아이템 슬롯 위를 클릭하면 -> 페이지 안 넘김 (드래그 동작을 위해)
        - 빈 공간 왼쪽/오른쪽 클릭하면 -> 페이지 넘김
        """
        current_x = INVEN_IMAGE_X if self.stage.is_crafting_open else CENTERED_INV_X
        inven_rect = pygame.Rect(current_x, INV_DRAW_Y, IMG_SIZE_INVEN[0], IMG_SIZE_INVEN[1])
        
        if not inven_rect.collidepoint(mouse_pos):
            return False

        # 1. 아이템 슬롯 위를 클릭했는지 확인 (오작동 방지)
        shift_x = current_x - INVEN_IMAGE_X
        if self.current_page == 1:
            slot_rects = INVENTORY_SLOT_RECTS
        else:
            slot_rects = INVENTORY_PAGE2_SLOT_RECTS
            
        for rect in slot_rects:
            shifted_rect = rect.move(shift_x, 0)
            if shifted_rect.collidepoint(mouse_pos):
                # 슬롯을 클릭했다면 페이지를 넘기지 않고 'UI 내부 클릭'으로만 처리
                self.just_turned_page = False
                return True

        # 2. 빈 공간 클릭 시 페이지 넘김 로직 (왼쪽/오른쪽)
        center_x = inven_rect.centerx
        if mouse_pos[0] < center_x:
            # 왼쪽 클릭: 이전 페이지
            if self.current_page > 1:
                self.current_page -= 1
                self.just_turned_page = True
        else:
            # 오른쪽 클릭: 다음 페이지 (현재 최대 2페이지)
            if self.current_page < 2:
                self.current_page += 1
                self.just_turned_page = True
                
        return True
'''
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
'''