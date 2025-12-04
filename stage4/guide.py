# guide.py
import pygame

def show_guide(screen, background_img, font):

    clock = pygame.time.Clock()

    messages = [
        "w,a,s,d 키로 우주선을 조종하여",
        "사방에서 날아오는 운석을 피해",
        "무사히 깐따삐아에 도착하십시오!",
        "a좌, d우, w상, s하"
    ]
    
    screen_width = screen.get_width()
    
    base_y = 150 

    line_spacing = 50 

    start_ticks = pygame.time.get_ticks()

    while True:
        pygame.event.pump()
        clock.tick(60)

        if pygame.time.get_ticks() - start_ticks > 5000:
            break

        screen.blit(background_img, (0, 0))

        for i, line in enumerate(messages):
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen_width // 2, base_y + (i * line_spacing)))
            screen.blit(text_surface, text_rect)
        
        pygame.display.update()