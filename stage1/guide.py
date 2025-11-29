import pygame
from .images import *

def f_guide(window, flag, isTab):
    skipFont = pygame.font.Font("DungGeunMO.ttf", 20)
    font = pygame.font.Font("DungGeunMO.ttf", 40)
    box = pygame.Surface((1200, 800)) 

    skip = "Click to Skip"
    texts = [
        "방향키를 눌러 이동합니다.", 
        "블록 앞에서 방향키를 3초 이상 눌러 블록을 깹니다.", 
        "TAB 키를 눌러 아이템을 확인합니다.", 
        "사다리를 드래그&드롭하여 설치합니다.", 
        "빛이 있는 곳으로 나갑니다.", 
        "너무 깊이 들어가면 위험하니 조심하시길 바랍니다.",
        ""
    ]
    
    if flag:
        if not f_guide.is_processed:
            f_guide.idx += 1
            f_guide.is_processed = True

    else:
        f_guide.is_processed = False

    if f_guide.idx >= len(texts):
        f_guide.idx = len(texts) - 1
    
    if (texts[f_guide.idx] != ""):
        skip_text = skipFont.render(skip, True, (255, 255, 255))
        skip_rect = skip_text.get_rect(center = (600, 500))
        box.fill((0, 0, 0)) 
        hole_color = (255, 0, 255)
        if (f_guide.idx == 0 or f_guide.idx == 1):
            pygame.draw.rect(box, hole_color, (1020, 0, 120, 60))
            box.set_colorkey(hole_color)
        elif (f_guide.idx == 2 and isTab):
            pygame.draw.rect(box, hole_color, (120, 90, 960, 600)) 
            box.set_colorkey(hole_color)
        elif (f_guide.idx == 4):
            pygame.draw.circle(box, hole_color, (1110,30), 50)
            box.set_colorkey(hole_color)
        elif (f_guide.idx == 5):
            pygame.draw.rect(box, hole_color, (0,750, 1200, 50))
            box.set_colorkey(hole_color)
        box.set_alpha(128)
        window.blit(box, (0,0))
        window.blit(skip_text, skip_rect)
    
    text = font.render(texts[f_guide.idx], True, (255, 255, 255))
    text_rect = text.get_rect(center=(600, 400))
    window.blit(text, text_rect)

f_guide.idx = 0
f_guide.is_processed = False 
