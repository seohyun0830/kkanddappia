import pygame
from setting import *
import images

class Player:
    def __init__(self):
        self.x = 100
        self.y = 630
        self.speed = 5
        self.direction_right = True
        self.is_moving = False
        
        # 애니메이션 관련
        self.current_frame_index = 0
        self.animation_counter = 0
        self.alpha = 255 
        
        self.is_walking_into_spaceship = False
        
    def update(self):
        if self.is_moving or self.is_walking_into_spaceship:
            self.animation_counter += 1
            if self.animation_counter >= ANIMATION_SPEED:
                self.animation_counter = 0
                active_anim = self.get_active_animation()
                if active_anim and 'right' in active_anim:
                    self.current_frame_index = (self.current_frame_index + 1) % len(active_anim['right'])
        else:
            self.animation_counter = 0
            self.current_frame_index = 0

    def get_active_animation(self):
        if self.is_walking_into_spaceship:
             return images.animations.get('in')
        return images.animations.get('bag') 

    def move(self, keys):
        self.is_moving = False
        
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction_right = False
            self.is_moving = True
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction_right = True
            self.is_moving = True
            
        # [중요] 여기에 if self.x < 0... 같은 코드가 있으면 절대 안됩니다!
        # 플레이어는 그냥 숫자를 계속 줄이고(-5, -10...), 
        # 맵 매니저가 그걸 보고 "어? 맵 넘어갔네" 하고 처리해야 합니다.

    def draw(self, screen):
        active_set = self.get_active_animation()
        
        if not active_set:
            return

        if self.direction_right:
            if self.is_moving or self.is_walking_into_spaceship:
                image = active_set['right'][self.current_frame_index]
            else:
                image = active_set['stand_right']
        else:
            if self.is_moving:
                image = active_set['left'][self.current_frame_index]
            else:
                image = active_set['stand_left']
        
        if self.alpha < 255:
            image = image.copy()
            image.set_alpha(self.alpha)
            
        screen.blit(image, (self.x, self.y))