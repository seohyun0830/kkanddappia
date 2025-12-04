import pygame
import os

#(670,580)

def kkanddappia_land(screen, bk2_img, person_img, person2_img, talk_img, font):
    clock = pygame.time.Clock()
    
    for i in range(6):
        pygame.event.pump() 
        screen.blit(bk2_img, (0, 0))
        if i%2==0:
            screen.blit(person_img, (680 + i * 5, 570 + i * 7))
            pygame.display.update()
            pygame.time.delay(500)
        else:
            screen.blit(bk2_img, (0, 0))
            screen.blit(person2_img, (680 + i * 5, 570 + i * 7))
            pygame.display.update()
            pygame.time.delay(500)
   
    screen.blit(bk2_img, (0, 0))

    screen.blit(person2_img, (720, 630))
    pygame.display.update()
    
    pygame.time.delay(1000)

    captured_screen = screen.copy()
    
    texts = [
        "여기가... 깐따삐아인가?",
        "휴... 나 살았다!"
    ]
    dialog_rect = talk_img.get_rect(midbottom=(900, 650))
   
    text_idx = 0
    char_idx = 0
    last_time = 0
    typing_speed = 50
    typing_finished = False

    while True:
        dt = clock.tick(60)
        current_time = pygame.time.get_ticks()
        if text_idx >= len(texts):
            break
        
        current_full_text = texts[text_idx]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
            
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if typing_finished:
                        text_idx += 1
                        char_idx = 0
                        typing_finished = False
                    else:
                        char_idx = len(current_full_text)
                        typing_finished = True

        if not typing_finished:
            if current_time - last_time > typing_speed:
                char_idx += 1
                last_time = current_time
            
            if char_idx >= len(current_full_text):
                char_idx = len(current_full_text)
                typing_finished = True
        screen.blit(captured_screen, (0, 0))
   
        screen.blit(talk_img, dialog_rect)
    
        display_text = current_full_text[:char_idx]
        text_surface = font.render(display_text, True, (0, 0, 0)) 
      
        screen.blit(text_surface, (dialog_rect.x + 45, dialog_rect.y + 45))
    
        pygame.display.update()

    screen.blit(captured_screen, (0, 0))
    pygame.display.update()
    pygame.time.delay(1000)

def final_ending(screen, bk3, bk4, talk_img, font,mode):
    clock = pygame.time.Clock()
    
    fade_surface = pygame.Surface((1200, 800))
    fade_surface.fill((0, 0, 0))
    
    fade_duration = 1000 

    start_ticks = pygame.time.get_ticks()
    while True:
        pygame.event.pump()
        clock.tick(60)
        elapsed = pygame.time.get_ticks() - start_ticks
        if elapsed >= fade_duration: break
        progress = elapsed / fade_duration
        alpha = int(255 * (1.0 - progress))
        
        screen.blit(bk3, (0, 0))
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()

    screen.blit(bk3, (0, 0))
    pygame.display.update()
    pygame.time.delay(1500) 

    start_ticks = pygame.time.get_ticks()
    while True:
        pygame.event.pump()
        clock.tick(60)
        elapsed = pygame.time.get_ticks() - start_ticks
        if elapsed >= fade_duration: break
        progress = elapsed / fade_duration
        alpha = int(255 * progress)
        
        screen.blit(bk3, (0, 0))
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()

    start_ticks = pygame.time.get_ticks()
    while True:
        pygame.event.pump()
        clock.tick(60)
        elapsed = pygame.time.get_ticks() - start_ticks
        if elapsed >= fade_duration: break
        progress = elapsed / fade_duration
        alpha = int(255 * (1.0 - progress))
        
        screen.blit(bk4, (0, 0))
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()

    screen.blit(bk4, (0, 0))
    talk_img=pygame.transform.scale(talk_img,(650,250))
    talk_rect = talk_img.get_rect(topleft=(500, 350)) 
    screen.blit(talk_img, talk_rect)
    pygame.display.update()

    captured_screen = screen.copy()

    if mode=="easy":
        texts = [
            "할머니 덕분에 깐따삐아에 도착할 수 있었어..",
            "할머니 감사합니다!"]
    else:
        texts = [
            "할머니가 하시려뎐 말씀이 뭐였을까?",
            "할머니 보고 싶다.."]
    text_idx = 0
    char_idx = 0
    last_time = 0
    typing_speed = 50
    typing_finished = False

    while True:
        dt = clock.tick(60)
        current_time = pygame.time.get_ticks()

        if text_idx >= len(texts):
            break
        
        current_full_text = texts[text_idx]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if typing_finished:
                        text_idx += 1
                        char_idx = 0
                        typing_finished = False
                    else:
                        char_idx = len(current_full_text)
                        typing_finished = True

        if not typing_finished:
            if current_time - last_time > typing_speed:
                char_idx += 1
                last_time = current_time
            
            if char_idx >= len(current_full_text):
                char_idx = len(current_full_text)
                typing_finished = True

        screen.blit(captured_screen, (0, 0)) 
        display_text = current_full_text[:char_idx]
        text_surface = font.render(display_text, True, (0, 0, 0)) 
        
        screen.blit(text_surface, (talk_rect.x + 40, talk_rect.y + 50))
        

        pygame.display.update()

    screen.blit(bk4, (0, 0))
    pygame.display.update()
    pygame.time.delay(2000)

#############################################
#깐따삐아 도착
def default_ending(screen, kkanttapia_img, sounds):
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
    pygame.time.delay(1500)
    


def blackhole_ending(screen, background, blackhole_img, spaceship_img, spaceship_pos, bh_pos, size_info, sounds):
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

    