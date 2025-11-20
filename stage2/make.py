import pygame
from setting import *
import images

class CraftingManager:
    def __init__(self):
        self.is_open = False # 일반 제작창
        self.is_spaceship_open = False # 우주선 조립창
        
        # --- 일반 제작 (3x3) 설정 ---
        self.table = [None] * 9 # 3x3 그리드
        self.bg_image = images.ui_images['make2']
        # 위치: 원본 코드의 make2_image_x 계산식 (중앙에서 -310 이동)
        self.x = (SCREEN_WIDTH - self.bg_image.get_width()) // 2 - 310
        self.y = (SCREEN_HEIGHT - self.bg_image.get_height()) // 2
        
        # 제작 버튼
        self.button_rect = pygame.Rect(420, 260, 115, 115)

        # 슬롯 좌표 (절대 좌표 계산용 상대값)
        self.slot_rects = []
        cx_pos = [51, 151, 251]
        cy_pos = [56, 154, 255]
        for ry in cy_pos:
            for rx in cx_pos:
                self.slot_rects.append(pygame.Rect(self.x + rx, self.y + ry, ITEM_SIZE, ITEM_SIZE))

        # --- 우주선 조립 설정 ---
        self.spaceship_bg = images.ui_images['spaceship_make']
        self.sp_x = (SCREEN_WIDTH - self.spaceship_bg.get_width()) // 2
        self.sp_y = (SCREEN_HEIGHT - self.spaceship_bg.get_height()) // 2
        
        self.assembled_parts = [] # 조립된 부품 리스트
        self.assembled_slot_map = {} # { 'item_name': [slot_index1, slot_index2], ... }
        
        # 드롭 영역 (큰 사각형)
        self.sp_drop_area = pygame.Rect(self.sp_x + 50, self.sp_y + 50, 500, 500)

        # 표시용 슬롯 (4x4)
        self.sp_slots = []
        sp_rel = [55, 188, 321, 454]
        slot_size_px = 92
        
        count = 0
        for ry in sp_rel:
            for rx in sp_rel:
                if count < MAX_SPACESHIP_PARTS:
                    self.sp_slots.append(pygame.Rect(self.sp_x + rx, self.sp_y + ry, slot_size_px, slot_size_px))
                    count += 1

    def check_recipe(self, inventory_obj):
        """제작 버튼 클릭 시 레시피 확인 및 결과물 지급"""
        for recipe_data in RECIPES:
            if self.table == recipe_data['recipe']:
                result = recipe_data['result']
                if result:
                    # 재료 소모 (self.table은 이미 None이 아닌 것들이 있음)
                    # 여기서는 table만 비우면 됨 (이미 드래그해서 table에 넣을 때 인벤에서 빠짐)
                    # 하지만 혹시 모르니 로직상 inventory_obj.add_item(result) 만 수행
                    inventory_obj.add_item(result)
                    
                    # 테이블 비우기
                    self.table = [None] * 9
                    return True # 제작 성공
        
        # 실패 시 로직 (게임 오버? 혹은 그냥 아무일 없음?)
        # 원본 코드는 실패 시 game_over = True 였음.
        return False

    def handle_click_craft_slot(self, mouse_pos):
        """제작 슬롯 클릭 (이미 있는 아이템 회수용)"""
        if not self.is_open: return None
        
        for i, rect in enumerate(self.slot_rects):
            if rect.collidepoint(mouse_pos) and self.table[i] is not None:
                item = self.table[i]
                self.table[i] = None
                return item # 드래그 시작할 아이템
        return None

    def handle_drop(self, mouse_pos, item_name, inventory_obj):
        """
        드래그 드롭 처리
        return: True(성공적으로 어딘가에 들어감), False(실패, 인벤토리로 복구해야 함)
        """
        # 1. 일반 제작창 드롭
        if self.is_open:
            for i, rect in enumerate(self.slot_rects):
                if rect.collidepoint(mouse_pos) and self.table[i] is None:
                    self.table[i] = item_name
                    return True

        # 2. 우주선 조립창 드롭
        if self.is_spaceship_open:
            if self.sp_drop_area.collidepoint(mouse_pos):
                if self.add_spaceship_part(item_name):
                    return True
        
        # 3. 외부 맵 우주선 영역 드롭 (스테이지2 -> 3 연결)
        # 이 부분은 map manager나 main에서 영역 체크를 해야 할 수도 있지만
        # 편의상 여기서 체크하거나 main에서 처리하는게 나음.
        # 여기서는 "제작창 내부 로직"만 담당하는게 깔끔하므로 False 리턴하여 메인에서 추가 처리 유도 가능
        # 일단은 제작창 관련만 처리.
        
        return False

    def add_spaceship_part(self, item_name):
        """우주선 부품 추가 로직"""
        req = SPACESHIP_REQUIREMENTS.get(item_name, 0)
        curr = self.assembled_parts.count(item_name)
        
        if req > 0 and curr < req:
            self.assembled_parts.append(item_name)
            
            # 시각적 슬롯 매핑
            all_assigned = sum(self.assembled_slot_map.values(), [])
            for i in range(MAX_SPACESHIP_PARTS):
                if i not in all_assigned:
                    if item_name not in self.assembled_slot_map:
                        self.assembled_slot_map[item_name] = []
                    self.assembled_slot_map[item_name].append(i)
                    break
            return True
        return False

    def get_spaceship_progress(self):
        return len(self.assembled_parts)

    def is_spaceship_complete(self):
        return len(self.assembled_parts) >= MAX_SPACESHIP_PARTS

    def draw(self, screen):
        # 1. 일반 제작창
        if self.is_open:
            screen.blit(self.bg_image, (self.x, self.y))
            # 슬롯 내용
            for i, item in enumerate(self.table):
                if item:
                    img = images.item_images.get(item)
                    if img: screen.blit(img, self.slot_rects[i])

        # 2. 우주선 조립창
        if self.is_spaceship_open:
            screen.blit(self.spaceship_bg, (self.sp_x, self.sp_y))
            
            # 조립된 부품 그리기
            for name, slots in self.assembled_slot_map.items():
                img = images.item_images.get(name)
                if img:
                    scaled = pygame.transform.scale(img, (SPACESHIP_ITEM_SIZE, SPACESHIP_ITEM_SIZE))
                    offset = (92 - SPACESHIP_ITEM_SIZE) // 2
                    for idx in slots:
                        if idx < len(self.sp_slots):
                            rect = self.sp_slots[idx]
                            screen.blit(scaled, (rect.x + offset, rect.y + offset))