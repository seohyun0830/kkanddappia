import pygame
import random
import math

class Meteor:
    images=[]
    def __init__(self, current_time, screen_width, screen_height,is_blackhole_active=False):
        
        self.size = 70
        self.radius = self.size/2*0.8

        self.idx = random.randint(0, 3) 
        if is_blackhole_active:
            self.speed = random.randint(6, 7) 

        elif current_time < 10: 
            self.speed = random.randint(2, 3) 
        else:
            self.speed = random.randint(3, 4) 
        
        if self.idx == 0:  # 오른쪽 위
            self.pos_x = random.randint(screen_width, screen_width + 200)
            self.pos_y = random.randint(-200, 0)
            self.to_x = -self.speed
            self.to_y = self.speed
            self.base_angle = 135

        elif self.idx == 1:  # 왼쪽 위
            self.pos_x = random.randint(-200, 0)
            self.pos_y = random.randint(-200, 0)
            self.to_x = self.speed
            self.to_y = self.speed
            self.base_angle = 45

        elif self.idx == 2:  # 오른쪽 아래
            self.pos_x = random.randint(screen_width, screen_width + 200)
            self.pos_y = random.randint(screen_height, screen_height + 200)
            self.to_x = -self.speed
            self.to_y = -self.speed
            self.base_angle = -135
        else:  # 왼쪽 아래
            self.pos_x = random.randint(-200, 0)
            self.pos_y = random.randint(screen_height, screen_height + 200)
            self.to_x = self.speed
            self.to_y = -self.speed
            self.base_angle = -45
            
        self.original_image = Meteor.images[self.idx]
        self.image = self.original_image

    
    def blackhole_appeared_func(self):
        old_speed = math.sqrt(self.to_x**2 + self.to_y**2) 
        new_speed = random.randint(6, 7)

        # 속도 비율 
        ratio = new_speed / old_speed
      
        self.to_x *= ratio
        self.to_y *= ratio

    def check_collision(self, target_x, target_y, target_radius):
        distance = math.sqrt((self.center_x - target_x)**2 + (self.center_y - target_y)**2)
        if distance<self.radius+target_radius:
            return 1
        return 0
    
    def update(self):
        
        self.to_x += random.uniform(-0.15, 0.15) 
        self.to_y += random.uniform(-0.12, 0.12)

        self.pos_x += self.to_x
        self.pos_y += self.to_y

        move_angle = math.degrees(math.atan2(self.to_y, self.to_x))
       
        final_angle = -move_angle + self.base_angle
        self.image = pygame.transform.rotate(self.original_image, final_angle)



    def draw(self, screen):
        new_rect = self.image.get_rect(center=(self.center_x, self.center_y))
        screen.blit(self.image, new_rect.topleft)
        #screen.blit(self.image, (self.pos_x, self.pos_y))


    def is_off_screen(self, screen_width, screen_height):
        return not (-200 < self.pos_x < screen_width + 200 and \
                    -200 < self.pos_y < screen_height + 200)

    @property
    def center_x(self):
        return self.pos_x + self.size / 2
    
    @property
    def center_y(self):
        return self.pos_y + self.size / 2