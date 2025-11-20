import pygame
from .setting import *
from . import images

class Dictionary:
    def __init__(self):
        self.is_open = False
        self.current_page = 1
        
        # 사전 창 위치 계산
        self.image = images.ui_images['dic']
        self.x = (SCREEN_WIDTH - self.image.get_width()) // 2
        self.y = (SCREEN_HEIGHT - self.image.get_height()) // 2
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

        # 아이콘 위치 (우측 상단)
        self.icon_rect = pygame.Rect(
            SCREEN_WIDTH - ICON_MARGIN - ICON_SIZE, 
            ICON_MARGIN, 
            ICON_SIZE, 
            ICON_SIZE
        )

    def toggle(self):
        self.is_open = not self.is_open
        # 열릴 때 다른 창들을 닫아야 하므로, 메인 루프에서 이 리턴값을 활용하면 좋음
        return self.is_open

    def handle_click(self, mouse_pos):
        """클릭 이벤트 처리"""
        # 아이콘 클릭 확인
        if self.icon_rect.collidepoint(mouse_pos):
            return self.toggle() # 상태 변경됨을 알림

        # 사전이 열려있을 때 페이지 넘김 처리
        if self.is_open and self.rect.collidepoint(mouse_pos):
            center_x = self.rect.centerx
            if mouse_pos[0] < center_x:
                if self.current_page > 1:
                    self.current_page -= 1
            else:
                if self.current_page < MAX_DIC_PAGES:
                    self.current_page += 1
            return True # 클릭 처리됨

        return False # 아무것도 클릭하지 않음

    def draw(self, screen):
        # 아이콘 그리기
        screen.blit(images.ui_images['icon_dic'], self.icon_rect)

        # 사전 창 그리기
        if self.is_open:
            screen.blit(self.image, (self.x, self.y))
            
            # 페이지 내용 그리기
            page_key = f'dic_p{self.current_page}'
            page_img = images.item_images.get(page_key)
            
            if page_img:
                # 사전 배경 중앙에 페이지 이미지 배치
                page_x = self.x + (self.image.get_width() - page_img.get_width()) // 2
                page_y = self.y + (self.image.get_height() - self.image.get_height()) // 2 
                # 원본 코드 로직 유지 (다만 y좌표 계산이 원본도 0이 되게 되어있어서 확인 필요, 일단 중앙 정렬로 가정)
                # 원본: (dic_image.get_height() - dic_image.get_height()) // 2 => 0
                # 이미지가 dic 배경 크기에 맞춰져 있다면 (page_x, self.y) 등이 맞을 수 있음.
                # 여기선 안전하게 rect center 기준 배치
                page_rect = page_img.get_rect(center=self.rect.center)
                screen.blit(page_img, page_rect)

            # 페이지 번호 텍스트
            text = images.fonts['small'].render(f"{self.current_page} / {MAX_DIC_PAGES}", True, BLACK)
            text_rect = text.get_rect(centerx=self.rect.centerx, bottom=self.rect.bottom - 30)
            screen.blit(text, text_rect)