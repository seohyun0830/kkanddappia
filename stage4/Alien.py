import pygame
import math

class Alien:
    def __init__(self,image):
        self.image=image
        self.image=pygame.transform.scale(self.image,(60,100))

        self.radius=100/2*0.8
        self.x_pos=0
        self.y_pos=0
        self.is_active = False
    def appearance(self):
            self.is_active=True
            self.x_pos=1200/2-self.image.get_width()/2
            self.y_pos=100
    
    def draw(self,screen):
        if self.is_active:
            screen.blit(self.image,(self.x_pos,self.y_pos))
    def detect_collision(self,sh_x_pos,sh_y_pos,sh_r,is_shield_active):
         if not self.is_active:
            return False
         sh_center_x=sh_x_pos+sh_r
         sh_center_y=sh_y_pos+sh_r
         distance=math.sqrt((sh_center_x-self.center_x)**2+(sh_center_y-self.center_y)**2)

         if distance<sh_r+self.radius:
              is_shield_active=True
              self.x_pos=-2000
              self.y_pos=-2000
              self.is_active=False
              return True
         return False
              
    @property
    def center_x(self):
         return self.x_pos+self.radius
    @property
    def center_y(self):
         return self.y_pos+self.radius
    
         


