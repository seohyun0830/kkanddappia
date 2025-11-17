import pygame
import random
import math
class Meteor:
    images=[]
    def __init__(self, current_time, screen_width, screen_height):
        
        self.size = 70
        self.radius = self.size/2*0.8

        self.idx = random.randint(0, 3) 
        
        if current_time < 10: 
            self.speed = random.randint(2, 3) 
        else:
            self.speed = random.randint(3, 4) 
        
        if self.idx == 0:  # 오른쪽 위
            self.pos_x = random.randint(screen_width, screen_width + 200)
            self.pos_y = random.randint(-200, 0)
            self.to_x = -self.speed
            self.to_y = self.speed
        elif self.idx == 1:  # 왼쪽 위
            self.pos_x = random.randint(-200, 0)
            self.pos_y = random.randint(-200, 0)
            self.to_x = self.speed
            self.to_y = self.speed
        elif self.idx == 2:  # 오른쪽 아래
            self.pos_x = random.randint(screen_width, screen_width + 200)
            self.pos_y = random.randint(screen_height, screen_height + 200)
            self.to_x = -self.speed
            self.to_y = -self.speed
        else:  # 왼쪽 아래
            self.pos_x = random.randint(-200, 0)
            self.pos_y = random.randint(screen_height, screen_height + 200)
            self.to_x = self.speed
            self.to_y = -self.speed
            
        self.image = Meteor.images[self.idx]


    def update(self):
        
        self.to_x += random.uniform(-0.3, 0.3) 
        self.to_y += random.uniform(-0.3, 0.3)

        
        self.pos_x += self.to_x
        self.pos_y += self.to_y


    def draw(self, screen):
        screen.blit(self.image, (self.pos_x, self.pos_y))


    def is_off_screen(self, screen_width, screen_height):
        return not (-200 < self.pos_x < screen_width + 200 and \
                    -200 < self.pos_y < screen_height + 200)

    @property
    def center_x(self):
        return self.pos_x + self.size / 2
    
    @property
    def center_y(self):
        return self.pos_y + self.size / 2