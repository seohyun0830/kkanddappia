import pygame
from .setting import *

class Dictionary:
    def __init__(self, stage):
        self.stage = stage
        self.images = stage.images
        
        self.current_page = 1
        
        # 폰트 설정 (잠금 메시지용 큰 폰트 추가)
        try:
            self.font = pygame.font.Font('DungGeunMO.ttf', 30)
            self.lock_font = pygame.font.Font('DungGeunMO.ttf', 50)
        except:
            self.font = pygame.font.Font(None, 30)
            self.lock_font = pygame.font.Font(None, 50)
        
        self.rect = pygame.Rect(DIC_IMAGE_X, DIC_IMAGE_Y, IMG_SIZE_DIC[0], IMG_SIZE_DIC[1])

    def handle_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            dic_center_x = self.rect.centerx
            
            # 1. 왼쪽 클릭 (이전 페이지)
            if mouse_pos[0] < dic_center_x:
                if self.current_page > 1:
                    self.current_page -= 1
            
            # 2. 오른쪽 클릭 (다음 페이지)
            else:
                # [해금 제한]
                # Easy 모드면 무제한, Hard 모드면 (1 + 쪽지 수)페이지까지만 이동 가능
                if self.stage.is_easy_mode:
                    limit = MAX_DIC_PAGES
                else:
                    # 0개면 1페이지, 1개면 2페이지... 까지 가능
                    limit = 1 + self.stage.collected_notes_count
                
                # 최대 페이지 수(11)를 넘지 않도록 조정
                final_limit = min(limit, MAX_DIC_PAGES)
                
                if self.current_page < final_limit:
                    self.current_page += 1
                else:
                    # 아직 해금되지 않았을 때 (디버깅용 메시지)
                    print(f"잠겨있습니다! 쪽지를 더 찾아주세요. (현재 {self.stage.collected_notes_count}개)")
            
            return True
        
        return False

    def draw(self):
        # 1. 배경(프레임) 그리기
        self.stage.screen.blit(self.images.dic_image, (DIC_IMAGE_X, DIC_IMAGE_Y))
        
        # 2. 현재 페이지 해금 여부 확인
        if self.stage.is_easy_mode:
            is_unlocked = True
        else:
            # n페이지를 보려면 n-1개의 쪽지가 필요함 (1페이지는 0개)
            needed_notes = self.current_page - 1
            is_unlocked = self.stage.collected_notes_count >= needed_notes

        if is_unlocked:
            # [해금됨] 페이지 내용 이미지 그리기
            dic_page_name = f'dic_p{self.current_page}'
            dic_page_image = self.images.item_images.get(dic_page_name)
            
            if dic_page_image:
                bg_width = self.images.dic_image.get_width()
                bg_height = self.images.dic_image.get_height()
                page_width = dic_page_image.get_width()
                page_height = dic_page_image.get_height()
                
                # 중앙 정렬
                page_x = DIC_IMAGE_X + (bg_width - page_width) // 2
                page_y = DIC_IMAGE_Y + (bg_height - page_height) // 2
                
                self.stage.screen.blit(dic_page_image, (page_x, page_y))
        else:
            # [잠김] 자물쇠 메시지 그리기
            lock_text = self.lock_font.render("LOCKED", True, RED)
            
            needed = self.current_page - 1
            desc_text = self.font.render(f"Find {needed} Notes to unlock!", True, BLACK)
            
            # 텍스트 중앙 정렬
            cx = DIC_IMAGE_X + self.images.dic_image.get_width() // 2
            cy = DIC_IMAGE_Y + self.images.dic_image.get_height() // 2
            
            lock_rect = lock_text.get_rect(center=(cx, cy - 30))
            desc_rect = desc_text.get_rect(center=(cx, cy + 30))
            
            self.stage.screen.blit(lock_text, lock_rect)
            self.stage.screen.blit(desc_text, desc_rect)

        # 3. 페이지 번호 표시
        page_str = f"{self.current_page} / {MAX_DIC_PAGES}"
        page_text = self.font.render(page_str, True, BLACK)
        
        text_x = DIC_IMAGE_X + (self.images.dic_image.get_width() // 2) - (page_text.get_width() // 2)
        text_y = DIC_IMAGE_Y + self.images.dic_image.get_height() - 40
        
        self.stage.screen.blit(page_text, (text_x, text_y))