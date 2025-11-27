import pygame
import math
class Bubble: 
    def __init__(self,image):
        self.image=image
        self.size=120
        self.image=pygame.transform.scale(self.image,(self.size,self.size))
        
    def draw(self,sh_x_pos,sh_y_pos,w,h,screen):
        center_x = sh_x_pos + w / 2
        center_y = sh_y_pos + h / 2
        
        rect = self.image.get_rect(center=(center_x, center_y))
        screen.blit(self.image, rect)
    
   