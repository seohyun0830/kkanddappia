import pygame
from collections import Counter
from .setting import *
from . import images

class Inventory:
    def __init__(self):
        # 초기 아이템 (테스트용 혹은 기본 지급)
        self.items = (['fire']*1 + ['water']*1 + ['stone']*15 + 
                      ['spaceship'] * 1 + 
                      ['spaceship-side'] * 4 + 
                      ['spaceship-roof'] * 4 + 
                      ['fuel tank'] * 7)
        
        self.is_open = False
        
        # UI 이미지 및 위치
        self.image = images.ui_images['inventory']
        # 기본 위치 (화면 중앙)
        self.center_x = (SCREEN_WIDTH - self.image.get_width()) // 2
        self.y = (SCREEN_HEIGHT - self.image.get_height()) // 2
        
        # 아이콘 (가방 아이콘)
        self.icon_rect = pygame.Rect(BAG_ICON_X, BAG_ICON_Y, ICON_SIZE, ICON_SIZE)

        # 슬롯 좌표 계산 (상대 좌표)
        self.slot_rel_positions = []
        rel_coords = [50, 142, 234, 326, 418, 512]
        for rel_y in rel_coords:
            for rel_x in rel_coords:
                # 아이템 중심 보정을 위해 약간의 오프셋(+20, ITEM_SIZE//2 등) 원본 로직 반영
                self.slot_rel_positions.append((rel_x - (ITEM_SIZE // 2) + 20, rel_y - (ITEM_SIZE // 2) + 20))

    def toggle(self):
        self.is_open = not self.is_open
        return self.is_open

    def add_item(self, item_name):
        self.items.append(item_name)

    def remove_item(self, item_name):
        """아이템 이름으로 하나 제거 (성공 시 True)"""
        try:
            self.items.remove(item_name)
            return True
        except ValueError:
            return False

    def get_stacked_items(self):
        """같은 아이템을 묶어서 반환 (UI 표시용)"""
        counts = Counter(self.items)
        stacked = []
        sorted_names = sorted(counts.keys())
        
        for name in sorted_names:
            total = counts[name]
            # 이미지가 있는 아이템만 표시
            if name in images.item_images:
                while total > 0:
                    count = min(total, MAX_STACK_SIZE)
                    stacked.append({'name': name, 'count': count})
                    total -= count
        return stacked

    def get_slot_rects(self, draw_x):
        """현재 그려진 위치(draw_x) 기준 절대 좌표 슬롯 Rect 리스트 반환"""
        rects = []
        for rx, ry in self.slot_rel_positions:
            abs_x = draw_x + rx
            abs_y = self.y + ry
            rects.append(pygame.Rect(abs_x, abs_y, ITEM_SIZE, ITEM_SIZE))
        return rects

    def draw(self, screen, shift_x=0):
        """
        shift_x: 제작창이 열렸을 때 인벤토리 위치를 오른쪽으로 밀기 위한 값
        """
        # 1. 아이콘 그리기
        screen.blit(images.ui_images['icon_bag'], self.icon_rect)

        if not self.is_open:
            return

        # 2. 배경 그리기
        # shift_x가 0이면 중앙, 아니면 제작창 옆 위치
        # 원본 로직: inven_image_x(제작창 옆) vs CENTERED_INV_X(중앙)
        # 여기서 draw_x를 계산
        draw_x = self.center_x + shift_x
        screen.blit(self.image, (draw_x, self.y))

        # 3. 아이템 그리기
        stacked = self.get_stacked_items()
        slot_rects = self.get_slot_rects(draw_x)
        
        # 가지고 있는 아이템만큼만 루프
        limit = min(len(stacked), len(slot_rects))
        
        for i in range(limit):
            item_data = stacked[i]
            rect = slot_rects[i]
            
            # 아이템 이미지
            img = images.item_images.get(item_data['name'])
            if img:
                screen.blit(img, rect.topleft)
                
                # 개수 표시
                count_text = images.fonts['micro'].render(f"x{item_data['count']}", True, YELLOW)
                text_pos = (rect.right - count_text.get_width() - 5, rect.bottom - count_text.get_height() - 5)
                screen.blit(count_text, text_pos)

    def handle_click_item(self, mouse_pos, shift_x=0):
        """클릭한 위치에 있는 아이템 정보를 반환 (드래그 시작용)"""
        if not self.is_open:
            return None

        draw_x = self.center_x + shift_x
        slot_rects = self.get_slot_rects(draw_x)
        stacked = self.get_stacked_items()

        for i, rect in enumerate(slot_rects):
            if i < len(stacked) and rect.collidepoint(mouse_pos):
                item_name = stacked[i]['name']
                # 실제 리스트에서 제거하고 드래그 시작
                # (주의: 스택된 것 중 하나만 꺼냄. 로직상 실제 items 리스트에서 맨 앞의 해당 이름을 pop)
                if self.remove_item(item_name):
                    return item_name
        return None