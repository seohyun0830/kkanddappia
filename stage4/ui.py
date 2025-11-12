import pygame
import math
import os

screen_width=1200
screen_height=800

# 연료 게이지 클래스
class fuelgauge:
    def __init__(self,x,y,image):
        self.image=image
        self.rect=image.get_rect(topleft=(x,y))
    def draw(self,screen):
        screen.blit(self.image,self.rect)
# 인디케이터 클래스:
class fuel_indicator:
    def __init__(self,x,y,image,max_val):   #x,y 중심mcvvvvvvvvvvvvvvvvvvvvve
        self.original_image = image 
        self.x = x
        self.y = y
        self.max_val = max_val
        self.angle = -75

    def update(self,val):
        ratio=val/self.max_val
        self.angle=75-(ratio*150)

    def draw(self,screen):
        r_image=pygame.transform.rotozoom(self.original_image,self.angle,1)
        new_rect=r_image.get_rect(center=(self.x,self.y))
        screen.blit(r_image,new_rect)
