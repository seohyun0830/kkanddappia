import pygame
from .setting import *

class Player:
    def __init__(self, stage):
        self.stage = stage
        self.images = stage.images
        
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.speed = PLAYER_SPEED
        self.direction_right = True
        self.is_moving = False
        
        self.current_frame_index = 0
        self.animation_counter = 0
        self.image = self.images.all_animations['bag']['stand_right']

        self.rect = pygame.Rect(self.x, self.y, PLAYER_SIZE[0], PLAYER_SIZE[1])
        
        self.alpha = 255
        self.is_fading_out = False
        
        self.is_walking_into_spaceship = False
        self.is_flying_animation_active = False # 사용 안 함 (호환성 위해 변수는 남겨둠)
        self.fly_animation_start_time = 0
        self.is_sound_playing = False

    def update(self):
        # [수정됨] 비행 애니메이션 로직 제거됨

        # 우주선으로 걸어가는 중 (엔딩)
        if self.is_walking_into_spaceship:
            self.update_walking_into_spaceship()
            self.update_sound()
            self.rect.topleft = (self.x, self.y)
            return

        # 일반 플레이
        self.handle_input()
        self.update_animation()
        self.handle_map_boundaries()
        self.update_fade()
        self.update_sound() 
        
        self.rect.topleft = (self.x, self.y)

    def update_sound(self):
        should_play = (self.is_moving or self.is_walking_into_spaceship) and not self.is_flying_animation_active
        if should_play:
            if not self.is_sound_playing:
                if self.stage.sounds.walk_sound:
                    self.stage.sounds.walk_sound.play(loops=-1)
                self.is_sound_playing = True
        else:
            if self.is_sound_playing:
                if self.stage.sounds.walk_sound:
                    self.stage.sounds.walk_sound.stop()
                self.is_sound_playing = False

    def handle_input(self):
        if (self.stage.open_door or self.stage.dic_open or 
            self.stage.is_spaceship_crafting_open or self.stage.map_manager.is_tree_pressing):
            self.is_moving = False
            return
        keys = pygame.key.get_pressed()
        self.is_moving = False
        if keys[pygame.K_a]:
            self.x -= self.speed
            self.direction_right = False
            self.is_moving = True
        elif keys[pygame.K_d]:
            self.x += self.speed
            self.direction_right = True
            self.is_moving = True

    def update_animation(self):
        target_speed = ANIMATION_SPEED
        if self.stage.map_manager.is_tree_pressing:
            active_set = self.images.all_animations['tree']
            target_speed = TREE_ANIMATION_SPEED 
            self.is_moving = True 
        elif self.stage.map_manager.current_map == "inside":
            active_set = self.images.all_animations['in']
        else:
            active_set = self.images.all_animations['bag']

        if active_set['right']:
            total_frames = len(active_set['right'])
            if self.current_frame_index >= total_frames:
                self.current_frame_index = self.current_frame_index % total_frames

        if self.is_moving:
            self.animation_counter += 1
            if self.animation_counter >= target_speed:
                self.animation_counter = 0
                if active_set['right']:
                    self.current_frame_index = (self.current_frame_index + 1) % len(active_set['right'])
            if self.direction_right:
                self.image = active_set['right'][self.current_frame_index]
            else:
                self.image = active_set['left'][self.current_frame_index]
        else:
            self.animation_counter = 0
            self.current_frame_index = 0
            if self.direction_right:
                self.image = active_set['stand_right']
            else:
                self.image = active_set['stand_left']

    def update_walking_into_spaceship(self):
        """엔딩: 플레이어가 화면 밖으로 걸어나가면 스테이지 클리어"""
        self.x += self.speed
        self.y = SPACESHIP_WALK_Y 
        self.is_moving = True
        self.direction_right = True
        
        active_set = self.images.all_animations['in']
        self.animation_counter += 1
        if self.animation_counter >= ANIMATION_SPEED:
            self.animation_counter = 0
            self.current_frame_index = (self.current_frame_index + 1) % len(active_set['right'])
        self.image = active_set['right'][self.current_frame_index]
        
        # [수정됨] 화면 완전히 밖으로 나가면(SCREEN_WIDTH 이상) 바로 클리어 처리
        if self.x >= SCREEN_WIDTH:
            self.is_walking_into_spaceship = False
            # self.start_flying_animation()  <-- 삭제 (비행 안 함)
            self.stage.stage_clear = True    # <-- 바로 클리어 신호 보냄

    def start_walking_into_spaceship(self):
        self.is_walking_into_spaceship = True
        self.x = 0
        self.y = 500
        self.direction_right = True
        self.current_frame_index = 0
        self.animation_counter = 0

    def start_flying_animation(self):
        # 사용 안 함
        self.is_flying_animation_active = True
        self.fly_animation_start_time = pygame.time.get_ticks()

    def handle_map_boundaries(self):
        current_map = self.stage.map_manager.current_map
        player_width = self.image.get_width()
        if current_map == "outside1":
            if self.x < 0: self.x = 0
            elif self.x > SCREEN_WIDTH - player_width:
                self.stage.map_manager.current_map = "outside2"
                self.x = 5
                self.reset_animation()
        elif current_map == "inside":
            if self.x < 0:
                self.stage.map_manager.current_map = "outside1"
                self.x = OUTSIDE_DOOR_AREA.centerx - (player_width // 2)
                self.reset_animation()
            elif self.x > SCREEN_WIDTH - player_width: self.x = SCREEN_WIDTH - player_width
        elif current_map == "outside2":
            if self.x < 0:
                self.stage.map_manager.current_map = "outside1"
                self.x = SCREEN_WIDTH - player_width - 5
                self.reset_animation()
            elif self.x > SCREEN_WIDTH - player_width: self.x = SCREEN_WIDTH - player_width

    def reset_animation(self):
        self.current_frame_index = 0
        self.animation_counter = 0

    def update_fade(self):
        if self.is_fading_out:
            self.alpha -= FADE_SPEED
            if self.alpha <= 0:
                self.alpha = 0
                self.is_fading_out = False
                self.stage.go_to_stage1 = True

    def draw(self):
        if self.is_flying_animation_active: return
        if self.alpha < 255:
            temp_image = self.image.copy()
            temp_image.set_alpha(self.alpha)
            self.stage.screen.blit(temp_image, (self.x, self.y))
        else:
            self.stage.screen.blit(self.image, (self.x, self.y))