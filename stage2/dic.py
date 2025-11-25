import pygame
from .setting import *

class Dictionary:
    def __init__(self, stage):
        self.stage = stage
        self.images = stage.images
        
        self.current_page = 1
        
        self.font = pygame.font.Font(None, 30)
        
        self.rect = pygame.Rect(DIC_IMAGE_X, DIC_IMAGE_Y, IMG_SIZE_DIC[0], IMG_SIZE_DIC[1])

    def handle_click(self, mouse_pos):

        if self.rect.collidepoint(mouse_pos):
            dic_center_x = self.rect.centerx
            
            if mouse_pos[0] < dic_center_x:
                if self.current_page > 1:
                    self.current_page -= 1
            else:
                if self.current_page < MAX_DIC_PAGES:
                    self.current_page += 1
            
            return True
        
        return False

    def draw(self):

        self.stage.screen.blit(self.images.dic_image, (DIC_IMAGE_X, DIC_IMAGE_Y))
        
        dic_page_name = f'dic_p{self.current_page}'
        dic_page_image = self.images.item_images.get(dic_page_name)
        
        if dic_page_image:
            bg_width = self.images.dic_image.get_width()
            bg_height = self.images.dic_image.get_height()
            page_width = dic_page_image.get_width()
            page_height = dic_page_image.get_height()
            
            page_x = DIC_IMAGE_X + (bg_width - page_width) // 2
            page_y = DIC_IMAGE_Y + (bg_height - page_height) // 2
            
            self.stage.screen.blit(dic_page_image, (page_x, page_y))

        page_text = self.font.render(f"{self.current_page} / {MAX_DIC_PAGES}", True, BLACK)
        
        text_x = DIC_IMAGE_X + (self.images.dic_image.get_width() // 2) - (page_text.get_width() // 2)
        text_y = DIC_IMAGE_Y + self.images.dic_image.get_height() - 30
        
        self.stage.screen.blit(page_text, (text_x, text_y))