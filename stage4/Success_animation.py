import pygame
import os
import Blackhole
def draw_success_ui(screen, move_success_images, font_path):
   
    success_font = pygame.font.Font(os.path.join(font_path, "DungGeunMo.ttf"), 70)
    success_text_surface = success_font.render("깐따삐아에 이주 성공하다!", True, (255, 255, 255))
    text_rect = success_text_surface.get_rect(center=(1200 / 2, 800/3 - 100))
    
    move_success_cnt = 0
    while move_success_cnt < 3:
        for img in move_success_images: 
            screen.blit(img, (0,0)) 
            screen.blit(success_text_surface, text_rect)
            pygame.display.update() 
            pygame.time.delay(500)
        move_success_cnt += 1
    pygame.time.delay(1500) 

#############################################
def default_ending(screen, kkanttapia_img, sounds, move_success_images, font_path):
    clock = pygame.time.Clock()
    fade_surface = pygame.Surface((1200, 800))
    fade_surface.fill((0, 0, 0))
    
    fade_start = pygame.time.get_ticks()
    fade_duration = 1000 
    pygame.mixer.music.pause()
            
    while True:
        clock.tick(60)
        elapsed = pygame.time.get_ticks() - fade_start
        if elapsed >= fade_duration:
            break
                    
        progress = elapsed / fade_duration
        alpha = int(progress * 255) 
                
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
               
    pygame.time.delay(1000) 
    sounds['landed'].play()
   
    fade_start = pygame.time.get_ticks()
    fade_duration = 1500 #
            
    while True:
        elapsed = pygame.time.get_ticks() - fade_start
        if elapsed >= fade_duration:
            break
                
        progress = elapsed / fade_duration
        alpha = int(255 - (progress * 255)) 
                
        screen.blit(kkanttapia_img, (0,0))
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
                
        pygame.display.update()
    


def blackhole_ending(screen, background, blackhole_img, spaceship_img, spaceship_pos, bh_pos, size_info, sounds, move_success_images, font_path):
    clock = pygame.time.Clock()
    
    pygame.mixer.music.pause()
    sounds['to_blackhole'].play()

    animation_start_time = pygame.time.get_ticks()
    animation_duration = 1500 
    
    start_x, start_y = spaceship_pos
    bh_x, bh_y = bh_pos
    start_width, start_height = size_info
    
    screen_width, screen_height = screen.get_size()

    bh_center_x = bh_x + 120 / 2
    bh_center_y = bh_y +120/2
    
    spaceship_radius = start_width / 2 * 0.7

    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill((0, 0, 0)) 
    
    animating = True
    while animating:
        pygame.event.pump()
        
        elapsed = pygame.time.get_ticks() - animation_start_time
        progress = min(1.0, elapsed / animation_duration) # 0.0 ~ 1.0
        ease_progress = progress * progress 

        current_width = int(start_width * (1.0 - ease_progress))
        current_height = int(start_height * (1.0 - ease_progress))
        if current_width < 1: current_width = 1
        if current_height < 1: current_height = 1
        
        current_x = start_x + (bh_center_x - (start_x + start_width/2)) * ease_progress
        current_y = start_y + (bh_center_y - (start_y + start_height/2)) * ease_progress

        screen.blit(background, (0,0))
        screen.blit(blackhole_img, (bh_x, bh_y)) 
      
        scaled_ship = pygame.transform.scale(spaceship_img, (current_width, current_height))
        scaled_rect = scaled_ship.get_rect(center = (current_x + current_width/2, current_y + current_height/2))
        screen.blit(scaled_ship, scaled_rect)
        
        alpha = int(ease_progress * 255) 
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0)) 

        pygame.display.update()
        clock.tick(60) 
        
        if progress >= 1.0:
            animating = False

    