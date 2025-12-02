import pygame
from stage2_back.setting import *

class Player:
    def __init__(self, images):
        self.images = images
        
        #시작 위치
        self.x = 100
        self.y = GROUND_Y
        
        self.direction = "right"
        self.is_moving = False
        
        #점프
        self.vel_y = 0
        self.is_jumping = False
        
        self.is_cutscene_mode = False
        
        self.frame_index = 0
        self.animation_timer = 0
        
        self.image = self.images.player_walk_right[0]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        if self.is_cutscene_mode:
            self.update_cutscene()
            return

        keys = pygame.key.get_pressed()
        self.is_moving = False
        
        if keys[pygame.K_LEFT]:
            self.x -= PLAYER_SPEED
            self.direction = "left"
            self.is_moving = True
        elif keys[pygame.K_RIGHT]:
            self.x += PLAYER_SPEED
            self.direction = "right"
            self.is_moving = True
            
        if keys[pygame.K_UP] and not self.is_jumping:
            self.vel_y = -JUMP_STRENGTH
            self.is_jumping = True
            self.is_moving = True
            
        self.vel_y += GRAVITY
        self.y += self.vel_y
        
        if self.y >= GROUND_Y:
            self.y = GROUND_Y
            self.vel_y = 0
            self.is_jumping = False
            
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.rect.width))
        
        self.rect.topleft = (self.x, self.y)
        
        self.animate()

    def start_cutscene(self):
        self.is_cutscene_mode = True
        self.x = 0
        self.y = GROUND_Y-50
        self.direction = "right"
        self.is_moving = True

    def update_cutscene(self):
        self.x += PLAYER_SPEED
        self.animate()

    def animate(self):
        if self.is_moving:
            self.animation_timer += 1
            if self.animation_timer >= ANIMATION_SPEED:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % 2
        else:
            self.frame_index = 0 
            
        if self.direction == "right":
            self.image = self.images.player_walk_right[self.frame_index]
        else:
            self.image = self.images.player_walk_left[self.frame_index]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))