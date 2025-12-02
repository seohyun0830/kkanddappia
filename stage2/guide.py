import pygame
from .setting import *

# 1. 처음 외부 (기본 조작)
def f_guide1(window, flag, isDragging):
    # 함수 속성 초기화
    if not hasattr(f_guide1, "idx"):
        f_guide1.idx = 0
        f_guide1.is_processed = False

    try:
        skipFont = pygame.font.Font("DungGeunMO.ttf", 20)
        font = pygame.font.Font("DungGeunMO.ttf", 40)
    except:
        skipFont = pygame.font.Font(None, 20)
        font = pygame.font.Font(None, 40)
        
    box = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)) 
    skip = "[SPACE] to Skip"

    texts = [
        "방향키를 눌러 이동합니다.", 
        "오른쪽으로 이동하여 우주선 제작소로 이동합니다.",
        "가방을 눌러 아이템을 확인합니다.",
        "사전을 눌러 아이템 조합 방법을 확인합니다.",
        "나무를 3초 이상 클릭해 목재를 얻습니다.", 
        "땅굴로 들어가 자원을 수집합니다.",
        "건물을 클릭해 연구실로 들어갑니다.",
        "" 
    ]

    if flag:
        if not f_guide1.is_processed:
            f_guide1.idx += 1
            f_guide1.is_processed = True
    else:
        f_guide1.is_processed = False

    if f_guide1.idx >= len(texts):
        f_guide1.idx = len(texts) - 1
    
    # 종료 조건
    if texts[f_guide1.idx] == "":
        return False

    # --- 그리기 ---
    box.fill((0, 0, 0)) 
    hole_color = (255, 0, 255)

    # 하이라이트 박스 그리기
        
    if f_guide1.idx == 2 or f_guide1.idx == 3: 
        # 가방/사전 아이콘 위치 (우측 상단)
        pygame.draw.rect(box, hole_color, (SCREEN_WIDTH - 200, 0, 200, 100))

    elif f_guide1.idx==4:
        pygame.draw.rect(box, hole_color, TREE_AREA)

    elif f_guide1.idx==5:
        pygame.draw.rect(box, hole_color, STAGE1_AREA)
        
    elif f_guide1.idx == 6:
        # 문 위치
        pygame.draw.rect(box, hole_color, OUTSIDE_DOOR_AREA)

    box.set_colorkey(hole_color)
    box.set_alpha(128) 
    window.blit(box, (0,0))

    # 텍스트 출력
    skip_text = skipFont.render(skip, True, WHITE)
    skip_rect = skip_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    window.blit(skip_text, skip_rect)
    
    text = font.render(texts[f_guide1.idx], True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    window.blit(text, text_rect)
    
    return True 

# 2. 연구실 안
def f_guide2(window, flag, isDragging):
    if not hasattr(f_guide2, "idx"):
        f_guide2.idx = 0
        f_guide2.is_processed = False

    try:
        skipFont = pygame.font.Font("DungGeunMO.ttf", 20)
        font = pygame.font.Font("DungGeunMO.ttf", 40)
    except:
        skipFont = pygame.font.Font(None, 20)
        font = pygame.font.Font(None, 40)

    box = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)) 
    skip = "[SPACE] to Skip"
    texts = [
        "책상 위 사전을 선택해 사전을 확인합니다.", 
        "기계를 클릭해 조합실로 입장합니다.",
        "아이템을 드래그 & 드롭한 후 M 버튼을 클릭해 조합합니다.",
        "E 버튼을 눌러 제작 슬롯을 비웁니다.",
        "왼쪽으로 이동하여 연구실을 나갑니다.",
        ""
    ]

    if flag:
        if not f_guide2.is_processed:
            f_guide2.idx += 1
            f_guide2.is_processed = True
    else:
        f_guide2.is_processed = False

    if f_guide2.idx >= len(texts):
        f_guide2.idx = len(texts) - 1
    
    if texts[f_guide2.idx] == "":
        return False

    box.fill((0, 0, 0)) 
    hole_color = (255, 0, 255)
    
    if f_guide2.idx == 0:
        pygame.draw.rect(box, hole_color, DIC_AREA)
    elif f_guide2.idx == 1:
        pygame.draw.rect(box, hole_color, CLICK_AREA)
    elif f_guide2.idx == 2 or f_guide2.idx ==3:
        # 제작창 위치 (make2 이미지 기준)
        pygame.draw.rect(box, hole_color, (MAKE2_IMAGE_X, MAKE2_IMAGE_Y, IMG_SIZE_MAKE2[0], IMG_SIZE_MAKE2[1]))

    box.set_colorkey(hole_color)
    box.set_alpha(128)
    window.blit(box, (0,0))

    skip_text = skipFont.render(skip, True, WHITE)
    skip_rect = skip_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    window.blit(skip_text, skip_rect)
    
    text = font.render(texts[f_guide2.idx], True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    window.blit(text, text_rect)
    
    return True

# 3. 우주선 제작소
def f_guide3(window, flag, isDragging):
    if not hasattr(f_guide3, "idx"):
        f_guide3.idx = 0
        f_guide3.is_processed = False

    try:
        skipFont = pygame.font.Font("DungGeunMO.ttf", 20)
        font = pygame.font.Font("DungGeunMO.ttf", 40)
    except:
        skipFont = pygame.font.Font(None, 20)
        font = pygame.font.Font(None, 40)

    box = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)) 
    skip = "[SPACE] to Skip"
    texts = [
        "오른쪽으로 이동하여 우주선 발사대로 이동합니다.", 
        "드래그 & 드롭해 우주선을 제작합니다.", 
        "왼쪽으로 이동합니다.",
        ""
    ]

    if flag:
        if not f_guide3.is_processed:
            f_guide3.idx += 1
            f_guide3.is_processed = True
    else:
        f_guide3.is_processed = False

    if f_guide3.idx >= len(texts):
        f_guide3.idx = len(texts) - 1
    
    if texts[f_guide3.idx] == "":
        return False

    box.fill((0, 0, 0)) 
    hole_color = (255, 0, 255)
    
    if f_guide3.idx == 1:
        pygame.draw.rect(box, hole_color, SPACESHIP_AREA)

    box.set_colorkey(hole_color)
    box.set_alpha(128)
    window.blit(box, (0,0))

    skip_text = skipFont.render(skip, True, WHITE)
    skip_rect = skip_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    window.blit(skip_text, skip_rect)
    
    text = font.render(texts[f_guide3.idx], True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    window.blit(text, text_rect)
    
    return True