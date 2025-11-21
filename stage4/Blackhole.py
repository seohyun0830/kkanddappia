import pygame
import math
import random


class Blackhole:
    def __init__(self,image):
        self.image=image
        self.size=120
        self.image=pygame.transform.scale(self.image,(self.size,self.size))
        
        self.radius=self.size/2*0.7 #충돌범위
        self.x_pos=0
        self.y_pos=0

    def make_blackhole(self):
        margin_top = 100    
        margin_bottom = 250 
        margin_left = 200    
        margin_right = 250   

        safe_x_min = margin_left
        safe_x_max = 1200 - margin_right - self.size
        safe_y_min = margin_top
        safe_y_max = 800 - margin_bottom - self.size

        side=random.choice(['top','bottom','left','right'])

        if side=='top':
            self.x_pos=random.randint(safe_x_min,safe_x_max)
            self.y_pos = safe_y_min 
        elif side == 'bottom':
            self.x_pos = random.randint(safe_x_min, safe_x_max)
            self.y_pos = safe_y_max
        elif side == 'left':
            self.x_pos = safe_x_min
            self.y_pos = random.randint(safe_y_min, safe_y_max)
        else: 
            self.x_pos = safe_x_max
            self.y_pos = random.randint(safe_y_min, safe_y_max)

    def draw(self,screen):
        screen.blit(self.image,(self.x_pos,self.y_pos))
        
    @property
    def center_x(self):
        return self.x_pos+self.radius

    @property
    def center_y(self):
        return self.y_pos+self.radius
    
       









            
        