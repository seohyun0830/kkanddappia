import pygame
from .images import *
from .setting import *

'''
CLICK_AREA = pygame.Rect(850, 100, 300, 380) 
OUTSIDE_DOOR_AREA = pygame.Rect(400, 400, 400, 300) 
OUTSIDE_MAKE_AREA = pygame.Rect(10, 340, 490, 350)
DIC_AREA = pygame.Rect(250, 480, 250, 100)
MAKE_BUTTON_AREA = pygame.Rect(420, 260, 115, 115)
'''
# flag : 스페이스바를 눌럿는가?
# 처음 외부
def f_guide1(window, flag, isDragging):
    skipFont = pygame.font.Font("DungGeunMO.ttf", 20)
    font = pygame.font.Font("DungGeunMO.ttf", 40)
    box = pygame.Surface((1200, 800)) 

    skip = "[SPACE] to Skip"

    # 문구 설정
    texts = [
        "방향키를 눌러 이동합니다.", 
        "가방을 눌러 아이템을 확인합니다.",
        "사전을 눌러 아이템 조합 방법을 확인합니다." 
        "건물을 클릭해 연구실로 들어갑니다."
    ]
    skip_text = skipFont.render(skip, True, (255, 255, 255))
    skip_rect = skip_text.get_rect(center = (600, 500))
    if flag:
        if not f_guide1.is_processed:
            f_guide1.idx += 1
            f_guide1.is_processed = True

    else:
        f_guide1.is_processed = False

    if f_guide1.idx >= len(texts):
        f_guide1.idx = len(texts) - 1
    
    if (texts[f_guide1.idx] != ""):
        box.fill((0, 0, 0)) 
        hole_color = (255, 0, 255)

        # 각 문구에서 밝게 보일 곳
        if (f_guide1.idx == 0 or f_guide1.idx == 1):
            pygame.draw.rect(box, hole_color, (1020, 0, 120, 60))
        elif (f_guide1.idx == 2):
            pygame.draw.rect(box, hole_color, (120, 90, 960, 600)) 
        elif (f_guide1.idx == 3):
            pass
        box.set_colorkey(hole_color)
        box.set_alpha(128)
        window.blit(box, (0,0))
        window.blit(skip_text, skip_rect)
    
    # 문구 출력 위치
    text = font.render(texts[f_guide1.idx], True, (255, 255, 255))
    text_rect = text.get_rect(center=(600, 400))
    window.blit(text, text_rect)

f_guide1.idx = 0
f_guide1.is_processed = False 

# 연구실 안
def f_guide2(window, flag, isDragging):
    skipFont = pygame.font.Font("DungGeunMO.ttf", 20)
    font = pygame.font.Font("DungGeunMO.ttf", 40)
    box = pygame.Surface((1200, 800)) 

    skip = "[SPACE] to Skip"
    texts = [
        "책상 위 사전을 선택해 사전을 확인합니다.", 
        "기계를 클릭해 조합실로 입장합니다.", 
        "아이템을 드래그 & 드롭한 후 M 버튼을 클릭해 조합합니다.",
        "왼쪽으로 이동하여 연구실을 나갑니다."
        ""
    ]
    skip_text = skipFont.render(skip, True, (255, 255, 255))
    skip_rect = skip_text.get_rect(center = (600, 500))
    if flag:
        if not f_guide2.is_processed:
            f_guide2.idx += 1
            f_guide2.is_processed = True

    else:
        f_guide2.is_processed = False

    if f_guide2.idx >= len(texts):
        f_guide2.idx = len(texts) - 1
    
    if (texts[f_guide2.idx] != ""):
        box.fill((0, 0, 0)) 
        hole_color = (255, 0, 255)
        if (f_guide2.idx == 0 or f_guide2.idx == 1):
            pygame.draw.rect(box, hole_color, (1020, 0, 120, 60))
        elif (f_guide2.idx == 2):
            pygame.draw.rect(box, hole_color, (120, 90, 960, 600)) 
        elif (f_guide2.idx == 3):
            pass
        box.set_colorkey(hole_color)
        box.set_alpha(128)
        window.blit(box, (0,0))
        window.blit(skip_text, skip_rect)
    
    text = font.render(texts[f_guide2.idx], True, (255, 255, 255))
    text_rect = text.get_rect(center=(600, 400))
    window.blit(text, text_rect)

f_guide2.idx = 0
f_guide2.is_processed = False 

# 우주선 제작소
def f_guide3(window, flag, isDragging):
    skipFont = pygame.font.Font("DungGeunMO.ttf", 20)
    font = pygame.font.Font("DungGeunMO.ttf", 40)
    box = pygame.Surface((1200, 800)) 

    skip = "[SPACE] to Skip"
    texts = [
        "오른쪽으로 이동하여 우주선 제작소로 이동합니다.", 
        "드래그 & 드롭해 우주선을 제작합니다.", 
        "왼쪽으로 이동합니다."
        ""
    ]
    skip_text = skipFont.render(skip, True, (255, 255, 255))
    skip_rect = skip_text.get_rect(center = (600, 500))
    if flag:
        if not f_guide3.is_processed:
            f_guide3.idx += 1
            f_guide3.is_processed = True

    else:
        f_guide3.is_processed = False

    if f_guide3.idx >= len(texts):
        f_guide3.idx = len(texts) - 1
    
    if (texts[f_guide3.idx] != ""):
        box.fill((0, 0, 0)) 
        hole_color = (255, 0, 255)
        if (f_guide3.idx == 0):
            pass
        elif (f_guide3.idx == 1):
            pygame.draw.rect(box, hole_color, SPACESHIP_AREA)
        elif (f_guide3.idx == 2):
            pass
        box.set_colorkey(hole_color)
        box.set_alpha(128)
        window.blit(box, (0,0))
        window.blit(skip_text, skip_rect)
    
    text = font.render(texts[f_guide3.idx], True, (255, 255, 255))
    text_rect = text.get_rect(center=(600, 400))
    window.blit(text, text_rect)

f_guide3.idx = 0
f_guide3.is_processed = False 

# 다시 처음
def f_guide4(window, flag, isDragging):
    skipFont = pygame.font.Font("DungGeunMO.ttf", 20)
    font = pygame.font.Font("DungGeunMO.ttf", 40)
    box = pygame.Surface((1200, 800)) 

    skip = "[SPACE] to Skip"
    texts = [
        "나무를 3초 이상 클릭해 목재를 얻습니다.", 
        "땅굴로 들어가 자원을 수집합니다.",
        ""
    ]
    skip_text = skipFont.render(skip, True, (255, 255, 255))
    skip_rect = skip_text.get_rect(center = (600, 500))
    if flag:
        if not f_guide4.is_processed:
            f_guide4.idx += 1
            f_guide4.is_processed = True

    else:
        f_guide4.is_processed = False

    if f_guide4.idx >= len(texts):
        f_guide4.idx = len(texts) - 1
    
    if (texts[f_guide4.idx] != ""):
        box.fill((0, 0, 0)) 
        hole_color = (255, 0, 255)
        if (f_guide4.idx == 0):
            pygame.draw.rect(box, hole_color, TREE_AREA)
        elif (f_guide4.idx == 1):
            pygame.draw.rect(box, hole_color, STAGE1_AREA) 
        box.set_colorkey(hole_color)
        box.set_alpha(128)
        window.blit(box, (0,0))
        window.blit(skip_text, skip_rect)
    
    text = font.render(texts[f_guide4.idx], True, (255, 255, 255))
    text_rect = text.get_rect(center=(600, 400))
    window.blit(text, text_rect)

f_guide4.idx = 0
f_guide4.is_processed = False 
