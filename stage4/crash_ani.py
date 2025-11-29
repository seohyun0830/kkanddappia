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

def restart_ani(screen, bk_img, person_images,sperson_img):
    cnt = 0
    i=0
    while cnt < 4: 
        for img in person_images:
            
            screen.blit(bk_img, (0, 0))
            screen.blit(img, (810+i , 650))
            i+=2
            pygame.display.update()
            pygame.time.delay(300) 
            
        cnt += 1
    screen.blit(bk_img, (0, 0))
    screen.blit(sperson_img, (810+i , 650))
    pygame.display.update()
    pygame.time.delay(1000) # 끝나고 잠시 대기

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




def restart_talk(screen, dialog_img):
    clock = pygame.time.Clock()
    
    # 1. 현재 화면 캡처 (배경용)
    captured_screen = screen.copy()

    current_path = os.path.dirname(__file__)
    font_path = os.path.join(current_path, "font", "DungGeunMo.ttf")
    
    font = pygame.font.Font(font_path, 30)

    texts = [
        "으으... 허리가...",
        "잠깐, 여긴... 아까 그 출발지잖아? 하, 중력 한번 살벌하네.",
        "다 분해됐잖아. 그치만 부품은 다 여기 있군?",
        "다시 붙여서 뜬다. 이번엔 진짜 간다."
    ]
    
    idx = 0             # 문장 인덱스
    char_index = 0      # 글자 인덱스
    last_time = 0       # 타이머
    typing_speed = 50   # 타자 속도
    typing_finished = False # 타이핑 완료 여부

    dialog_rect = dialog_img.get_rect(center=(1200 // 2, 800 -600))

    while True:
        dt = clock.tick(60)
  
        if idx >= len(texts):
            return "reset"

        current_full_text = texts[idx]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if typing_finished:
                    idx += 1
                    char_index = 0
                    typing_finished = False
                else:
                    char_index = len(current_full_text)
                    typing_finished = True

        current_time = pygame.time.get_ticks()

        if not typing_finished:
            if current_time - last_time > typing_speed:
                char_index += 1
                last_time = current_time
            
            if char_index >= len(current_full_text):
                char_index = len(current_full_text)
                typing_finished = True 

        display_text = current_full_text[:char_index]

        screen.blit(captured_screen, (0, 0))
    
        screen.blit(dialog_img, dialog_rect)
        
        text_surface = font.render(display_text, True, (0, 0, 0)) 
        
        text_rect = text_surface.get_rect()

        text_rect.centery = dialog_rect.centery

        text_rect.x = dialog_rect.x + 40 
        screen.blit(text_surface, text_rect)
        
   

        pygame.display.update()