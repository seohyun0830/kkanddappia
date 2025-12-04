import pygame
import os

class Spaceship:
    def __init__(self,image_path):
        self.images=[]
        for path in image_path:
            img=pygame.image.load(path)
            img=pygame.transform.scale(img,(80,80))
            self.images.append(img)
        self.width=80
        self.height=80
        self.radius=self.width/2*0.7
        self.speed=7

        self.x_pos=(1200-self.width)/2
        self.y_pos=(800-self.height)/2
        self.to_x=0
        self.to_y=0

        self.idx=0
        self.is_invincible=False
        self.invincible_start_time=0
    def update(self):
        self.x_pos+=self.to_x
        self.y_pos+=self.to_y
        # 화면 경계 처리
        if self.x_pos < 0: self.x_pos = 0
        elif self.x_pos > 1200 - self.width: self.x_pos = 1200 - self.width
        
        if self.y_pos < 0: self.y_pos = 0
        elif self.y_pos > 800 - self.height: self.y_pos = 800 - self.height

    def draw(self,screen):
        cur_img=self.images[self.idx]
        if self.is_invincible:
            if(pygame.time.get_ticks()//100)%2==0:
                screen.blit(cur_img,(self.x_pos,self.y_pos))
        else:
            screen.blit(cur_img,(self.x_pos,self.y_pos))

    def hard_handle_input(self,event):
        if event.type == pygame.KEYDOWN:
            # a좌 d우 w상 s하
            if self.idx == 0:
                if event.key == pygame.K_a: self.to_x = -self.speed
                elif event.key == pygame.K_d: self.to_x = self.speed
                elif event.key == pygame.K_s: self.to_y = self.speed
                elif event.key == pygame.K_w: self.to_y = -self.speed
            elif self.idx == 1:
                if event.key == pygame.K_a: self.to_y = -self.speed
                elif event.key == pygame.K_d: self.to_y = self.speed
                elif event.key == pygame.k_s: self.to_x = -self.speed
                elif event.key == pygame.K_w: self.to_x = self.speed
            elif self.idx == 2:
                if event.key == pygame.K_a: self.to_x = self.speed
                elif event.key == pygame.K_d: self.to_x = -self.speed
                elif event.key == pygame.K_s: self.to_y = -self.speed
                elif event.key == pygame.K_w: self.to_y = self.speed
            else: 
                if event.key == pygame.K_a: self.to_y = self.speed
                elif event.key == pygame.K_d: self.to_y = -self.speed
                elif event.key == pygame.K_s: self.to_x = self.speed
                elif event.key == pygame.K_w: self.to_x = -self.speed
        
        if event.type == pygame.KEYUP:
            if self.idx == 0:
                if event.key == pygame.K_a or event.key == pygame.K_d: self.to_x = 0
                elif event.key == pygame.K_w or event.key == pygame.K_s: self.to_y = 0
            elif self.idx == 1:
                if event.key == pygame.K_w or event.key == pygame.K_s: self.to_x = 0
                elif event.key == pygame.K_a or event.key == pygame.K_d: self.to_y = 0
            elif self.idx == 2:
                if event.key == pygame.K_a or event.key == pygame.K_d: self.to_x = 0
                elif event.key == pygame.K_w or event.key == pygame.K_s: self.to_y = 0
            else: # 3
                if event.key == pygame.K_w or event.key == pygame.K_s: self.to_x = 0
                elif event.key == pygame.K_a or event.key == pygame.K_d: self.to_y = 0
    
    
    # 무적 상태 설정
    def set_invincible(self, start_time):
        self.is_invincible = True
        self.invincible_start_time = start_time

    # 무적 상태 해제 검사
    def check_invincible_end(self, current_time):
        if self.is_invincible and current_time - self.invincible_start_time > 2:
            self.is_invincible = False

    @property
    def center_x(self):
        return self.x_pos + self.radius 
    @property
    def center_y(self):
        return self.y_pos + self.radius
    
    @property
    def cur_img(self):
        return self.images[self.idx]