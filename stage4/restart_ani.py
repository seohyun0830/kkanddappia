import pygame
import os
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
            screen.blit(captured_screen, (0, 0))
            pygame.display.update()
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