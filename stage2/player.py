import pygame
from setting import *

class Player:
    def __init__(self, stage):
        self.stage = stage
        self.images = stage.images
        
        # 위치 및 이동 관련
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.speed = PLAYER_SPEED
        self.direction_right = True
        self.is_moving = False
        
        # 애니메이션 관련
        self.current_frame_index = 0
        self.animation_counter = 0
        
        self.image = self.images.all_animations['bag']['stand_right']
        
        #투명도
        self.alpha = 255
        self.is_fading_out = False
        
        self.is_walking_into_spaceship = False
        self.is_flying_animation_active = False
        self.fly_animation_start_time = 0

        self.is_sound_playing=False

    def update(self):

        if self.is_flying_animation_active:
            elapsed_time = pygame.time.get_ticks() - self.fly_animation_start_time
            return

        if self.is_walking_into_spaceship:
            self.update_walking_into_spaceship()
            self.update_sound()
            return

        self.handle_input()
        self.update_animation()
        self.handle_map_boundaries()
        self.update_fade()

        self.update_sound()

    def update_sound(self):
        """걷는 소리 켜고 끄기 로직"""
        should_play = self.is_moving or self.is_walking_into_spaceship

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
        
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction_right = False
            self.is_moving = True
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction_right = True
            self.is_moving = True

    def update_animation(self):

        ani_speed=ANIMATION_SPEED

        if self.stage.map_manager.is_tree_pressing:
            active_set = self.images.all_animations['tree']
            ani_speed=TREE_ANIMATION_SPEED
            self.is_moving = True
        elif self.stage.map_manager.current_map == "inside":
            active_set = self.images.all_animations['in']
        else:
            active_set = self.images.all_animations['bag']

        if self.is_moving:
            self.animation_counter += 1

            if self.animation_counter >= ani_speed:
                self.animation_counter = 0
                if active_set['right']:
                    self.current_frame_index = (self.current_frame_index + 1) % len(active_set['right'])
            
            if self.direction_right:
                self.image = active_set['right'][self.current_frame_index]
            else:
                self.image = active_set['left'][self.current_frame_index]
        
        # 멈춰있을 때
        else:
            self.animation_counter = 0
            self.current_frame_index = 0
            if self.direction_right:
                self.image = active_set['stand_right']
            else:
                self.image = active_set['stand_left']

    def update_walking_into_spaceship(self):
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
        
        '''
        if self.x >= SCREEN_WIDTH - self.image.get_width():
            self.is_walking_into_spaceship = False
            self.start_flying_animation()
        '''

    def start_walking_into_spaceship(self):

        self.is_walking_into_spaceship = True
        self.x = 0
        self.y = 500
        self.direction_right = True
        self.current_frame_index = 0
        self.animation_counter = 0

    def start_flying_animation(self):

        self.is_flying_animation_active = True
        self.fly_animation_start_time = pygame.time.get_ticks()

    def handle_map_boundaries(self):

        current_map = self.stage.map_manager.current_map
        player_width = self.image.get_width()
        
        if current_map == "outside1":
            if self.x < 0:
                self.x = 0
            elif self.x > SCREEN_WIDTH - player_width:
                self.stage.map_manager.current_map = "outside2"
                self.x = 5
                self.reset_animation()

        elif current_map == "inside":
            if self.x < 0:
                self.stage.map_manager.current_map = "outside1"
                self.x = SCREEN_WIDTH - player_width - 5
                self.reset_animation()
            elif self.x > SCREEN_WIDTH - player_width:
                self.x = SCREEN_WIDTH - player_width

        elif current_map == "outside2":
            if self.x < 0:
                self.stage.map_manager.current_map = "outside1"
                self.x = SCREEN_WIDTH - player_width - 5
                self.reset_animation()
            elif self.x > SCREEN_WIDTH - player_width:
                self.x = SCREEN_WIDTH - player_width

    def reset_animation(self):
        self.current_frame_index = 0
        self.animation_counter = 0

    def update_fade(self):
        if self.is_fading_out:
            self.alpha -= FADE_SPEED
            if self.alpha <= 0:
                self.alpha = 0
                self.is_fading_out = False

    def draw(self):
        if self.is_flying_animation_active:
            return

        if self.alpha < 255:
            temp_image = self.image.copy()
            temp_image.set_alpha(self.alpha)
            self.stage.screen.blit(temp_image, (self.x, self.y))
        else:
            self.stage.screen.blit(self.image, (self.x, self.y))