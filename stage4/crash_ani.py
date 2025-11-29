import pygame
import random
import os
def zoom_effect(screen, target_image, sounds): 
    clock = pygame.time.Clock()
    pygame.mixer.music.pause()

    
    if 'siren' in sounds:
        sounds['siren'].play(maxtime=7000)
    
    ZOOM_DURATION = 3000  
    START_SCALE = 0.1 
    END_SCALE = 1.0 
    SCREEN_CENTER = (1200 // 2, 800 // 2)
    
    start_ticks = pygame.time.get_ticks()
    ow, oh = target_image.get_size() 
    crash_played = False
    
    while True:
        pygame.event.pump()
        clock.tick(60)
        elapsed = pygame.time.get_ticks() - start_ticks
    
        if elapsed >= 500 and not crash_played:
            if 'external_failure' in sounds:
                sounds['external_failure'].play(maxtime=5000)
            crash_played = True 
        
        elapsed = pygame.time.get_ticks() - start_ticks
        if elapsed >= ZOOM_DURATION:
            break 
        
        progress = elapsed / ZOOM_DURATION
        current_scale = START_SCALE + (progress * (END_SCALE - START_SCALE))
        
        new_width = max(1, int(ow * current_scale))
        new_height = max(1, int(oh * current_scale))
        new_size = (new_width, new_height)
        
        zoomed_img = pygame.transform.scale(target_image, new_size)
        draw_rect = zoomed_img.get_rect(center=SCREEN_CENTER)
        
        screen.fill((0, 0, 0)) 
        screen.blit(zoomed_img, draw_rect)
        pygame.display.update()
    
    final_rect = target_image.get_rect(center=SCREEN_CENTER)
    screen.fill((0, 0, 0))
    screen.blit(target_image, final_rect)
    pygame.display.update()
    
    pygame.time.delay(1500)


def crash_animation(screen, crash_images,sounds):
    clock = pygame.time.Clock()
    pygame.mixer.music.pause()
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
   
    frame_per_image =50
    

    for i, img in enumerate(crash_images):
    
        if i == 6:
            if 'ground_crash' in sounds: 
                sounds['ground_crash'].play()
        elif i == 7 or i == 8:
            if 'burning' in sounds: 
                sounds['burning'].play(maxtime=1000)
        for _ in range(frame_per_image):
            pygame.event.pump() 
            
            shake_x = random.randint(-5, 5)
            shake_y = random.randint(-3, 3)
            
            screen.blit(img, (shake_x, shake_y))
            
            pygame.display.update()
            clock.tick(60) 
    
    last_img = crash_images[-1]
    screen.blit(last_img, (0, 0))
    pygame.display.update()
    pygame.time.delay(1500)




