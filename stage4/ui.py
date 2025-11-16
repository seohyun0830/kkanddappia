import pygame
import math
import os

#꺾이는 지점
#(170,200)
#(150,150)
#(105,140)
#(100,97)
#(55,84)

class navigation:
    def __init__(self,image):
        self.original_image=image

        self.base_x = 950 
        self.base_y = 550

        self.rel_x = 200.0
        self.rel_y = 210.0

        self.angle = -60
        self.rect = image.get_rect(center=(self.base_x + self.rel_x, self.base_y + self.rel_y))

    def update(self,mode):
        if mode == 1:
            self.angle = 60 
            dx=0.035
            dy=0.01
        elif mode == 2:
            self.angle = 10
            dx=0.02
            dy=0.05
        elif mode == 3:
            self.angle = 50
            dx=0.04
            dy=0.01
        elif mode == 4:
            self.angle = 10
            dx=0.005
            dy=0.045
        elif mode == 5:
            self.angle = 60
            dx=0.047
            dy=0.01
        elif mode == 6:
            self.angle = 5
            dx=0.01
            dy=0.017
        self.rel_x-=dx
        self.rel_y-=dy
        self.rect.center = (self.base_x + int(self.rel_x), self.base_y + int(self.rel_y))

    def draw(self,screen):
        r_image=pygame.transform.rotozoom(self.original_image,self.angle,1)
        new_rect=r_image.get_rect(center=self.rect.center)
        screen.blit(r_image,new_rect)
# 연료 게이지 클래스
class fuelgauge:
    def __init__(self,x,y,image):
        self.image=image
        self.rect=image.get_rect(topleft=(x,y))
    def draw(self,screen):
        screen.blit(self.image,self.rect)
# 인디케이터 클래스:
class fuel_indicator:
    def __init__(self,x,y,image,max_val):   #x,y 중심
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
