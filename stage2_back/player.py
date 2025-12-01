import pygame
from setting import *

class Player:
    def __init__(self, images):
        self.images = images
        
        # 초기 위치
        self.x = 100
        self.y = GROUND_Y
        
        self.direction = "right"
        self.is_moving = False
        
        # 점프 관련 변수
        self.vel_y = 0
        self.is_jumping = False
        
        # 컷신 모드 변수
        self.is_cutscene_mode = False
        
        # 애니메이션 변수
        self.frame_index = 0
        self.animation_timer = 0
        
        self.image = self.images.player_walk_right[0]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        # 컷신 모드일 때는 플레이어 조작 불가 (자동 이동)
        if self.is_cutscene_mode:
            self.update_cutscene()
            return

        keys = pygame.key.get_pressed()
        self.is_moving = False
        
        # --- 좌우 이동 ---
        if keys[pygame.K_LEFT]:
            self.x -= PLAYER_SPEED
            self.direction = "left"
            self.is_moving = True
        elif keys[pygame.K_RIGHT]:
            self.x += PLAYER_SPEED
            self.direction = "right"
            self.is_moving = True
            
        # --- 점프 로직 (위 방향키) ---
        if keys[pygame.K_UP] and not self.is_jumping:
            self.vel_y = -JUMP_STRENGTH # 위로 솟구침
            self.is_jumping = True
            self.is_moving = True # 점프 중에도 걷는 모션 유지
            
        # --- 중력 적용 ---
        self.vel_y += GRAVITY
        self.y += self.vel_y
        
        # --- 바닥 충돌 처리 ---
        if self.y >= GROUND_Y:
            self.y = GROUND_Y
            self.vel_y = 0
            self.is_jumping = False
            
        # --- 화면 좌우 경계 처리 ---
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.rect.width))
        
        # rect 위치 업데이트 (충돌 감지용)
        self.rect.topleft = (self.x, self.y)
        
        # 애니메이션 처리
        self.animate()

    def start_cutscene(self):
        """컷신 시작: 위치 초기화 및 모드 변경"""
        self.is_cutscene_mode = True
        self.x = 0 # 화면 왼쪽 끝에서 시작
        # 배경이 바뀌면 땅 높이가 다를 수 있으므로 위치 조정 (필요시 수정)
        self.y = GROUND_Y-50
        self.direction = "right"
        self.is_moving = True

    def update_cutscene(self):
        """컷신 중 자동 이동"""
        self.x += PLAYER_SPEED
        self.animate()
        # 화면 밖으로 나가는 체크는 Main에서 함

    def animate(self):
        """움직임 상태에 따라 이미지 프레임 교체"""
        if self.is_moving:
            self.animation_timer += 1
            if self.animation_timer >= ANIMATION_SPEED:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % 2
        else:
            # 멈추면 서 있는 자세
            self.frame_index = 0 
            
        if self.direction == "right":
            self.image = self.images.player_walk_right[self.frame_index]
        else:
            self.image = self.images.player_walk_left[self.frame_index]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))