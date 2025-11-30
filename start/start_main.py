import pygame
from button.images import btn_background
from .images import background, background2, sfx_click, planet
from button.isClicked import f_isClicked

def f_start(window):
    # --- [초기화 & 리소스 로드] ---
    clock = pygame.time.Clock()
    pygame.event.clear() # 이전 입력 청소

    # 1. 폰트 설정
    font_btn = pygame.font.Font('DungGeunMO.ttf', 100)
    font_title = pygame.font.Font('DungGeunMO.ttf', 200)
    
    # 볼드체용 폰트 객체 별도 생성 (그림자 효과용)
    font_title_shadow = pygame.font.Font('DungGeunMO.ttf', 200)
    font_title_shadow.set_bold(True)

    # 2. ★★★ 텍스트 미리 렌더링 (최적화 핵심) ★★★
    # (루프 밖에서 이미지를 다 만들어둡니다)
    txt_start_white = font_btn.render("START", False, (255, 255, 255))
    txt_start_black = font_btn.render("START", False, (0, 0, 0))
    
    txt_title_white = font_title.render("깐따삐아!", False, (255, 255, 255))
    txt_title_black = font_title_shadow.render("깐따삐아!", False, (0, 0, 0))

    # 버튼 좌표
    btn_x, btn_y = 800, 600

    play = True
    while play:
        clock.tick(60) # FPS 60 고정

        # 3. 마우스 위치 및 호버 상태 확인 (한 번만 계산)
        xPos, yPos = pygame.mouse.get_pos()
        is_hover = f_isClicked(btn_x, btn_y, xPos, yPos)

        # 4. 이벤트 처리
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_hover: # 미리 계산된 호버 상태 사용
                    sfx_click.play()
                    return 1 # START

        # 5. 그리기
        window.blit(background, (0,0))
        window.blit(planet, (-70,-180))
        window.blit(btn_background, (btn_x, btn_y))
        
        # 호버 상태에 따라 미리 만들어둔 텍스트 이미지 선택
        if is_hover:
            window.blit(txt_start_black, (850, 600))
        else:
            window.blit(txt_start_white, (850, 600))

        # 타이틀 그리기 (그림자 -> 본체 순서)
        window.blit(txt_title_black, (155, 210))
        window.blit(txt_title_white, (150, 200))

        pygame.display.update()

def f_modeSelect(window):
    # --- [초기화] ---
    clock = pygame.time.Clock()
    pygame.event.clear()

    font_btn = pygame.font.Font('DungGeunMO.ttf', 100)

    # 텍스트 미리 렌더링
    txt_easy_white = font_btn.render("EASY", False, (255, 255, 255))
    txt_easy_black = font_btn.render("EASY", False, (0, 0, 0))
    
    txt_hard_white = font_btn.render("HARD", False, (255, 255, 255))
    txt_hard_black = font_btn.render("HARD", False, (0, 0, 0))

    # 버튼 좌표 정의
    easy_x, easy_y = 120, 400
    hard_x, hard_y = 720, 400

    play = True
    while play:
        clock.tick(60)

        xPos, yPos = pygame.mouse.get_pos()
        
        # 호버 상태 확인
        is_hover_easy = f_isClicked(easy_x, easy_y, xPos, yPos)
        is_hover_hard = f_isClicked(hard_x, hard_y, xPos, yPos)

        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                return 0
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_hover_easy:
                    sfx_click.play()
                    return 1 # EASY 모드 리턴
                elif is_hover_hard:
                    sfx_click.play()
                    return 2 # HARD 모드 리턴

        # 그리기
        window.blit(background2, (0,0))
        window.blit(planet, (600,350))
        # Easy 버튼
        window.blit(btn_background, (easy_x, easy_y))
        if is_hover_easy:
            window.blit(txt_easy_black, (200, 400))
        else:
            window.blit(txt_easy_white, (200, 400))

        # Hard 버튼
        window.blit(btn_background, (hard_x, hard_y))
        if is_hover_hard:
            window.blit(txt_hard_black, (800, 400))
        else:
            window.blit(txt_hard_white, (800, 400))

        pygame.display.update()