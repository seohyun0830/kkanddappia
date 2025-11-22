import pygame
from .images import *

def f_easy(window):
    clock = pygame.time.Clock()
    pygame.event.clear()
    
    font = pygame.font.Font("DungGeunMO.ttf", 40)
    texts = ["내가 너에게 마지막으로 전할 말이 있다...", "책상 위를 잘 보거라...", "네? 책상 위요??", "나는 이제 떠날 때가 되었구나..."]
    
    # 변수 초기화
    display_text = ""
    char_index = 0
    idx = 0
    
    # ★ '타이핑이 끝났는지' 확인하는 변수 (True면 클릭 대기 상태)
    typing_finished = False 

    last_time = pygame.time.get_ticks()
    typing_speed = 50 # (18은 너무 빠를 수 있어 조금 늦췄습니다)

    f_fade_in(window, grandma)

    play = True
    while play:
        clock.tick(60)
        
        if idx >= len(texts):
            f_fade_out(window, grandma)
            sfx_siren.play()
            return 8

        # 현재 출력해야 할 전체 문장
        current_full_text = texts[idx]

        # --- [1. 이벤트 처리] ---
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                return -1
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ★★★ 핵심 로직 ★★★
                if typing_finished:
                    # 1. 타이핑이 끝난 상태라면 -> 다음 문장으로!
                    idx += 1
                    char_index = 0      # 글자 수 초기화
                    typing_finished = False # 다시 타이핑 상태로 변경
                else:
                    # 2. (선택사항) 타이핑 중인데 클릭하면? -> 즉시 완성 (스킵 기능)
                    char_index = len(current_full_text)
        
        # --- [2. 타이핑 로직] ---
        current_time = pygame.time.get_ticks()
        
        # 타이핑이 아직 안 끝났다면 글자 수 증가
        if not typing_finished:
            if current_time - last_time > typing_speed:
                char_index += 1
                last_time = current_time
                sfx_type.play()
            
            # 문장 끝까지 다 썼는지 확인
            if char_index >= len(current_full_text):
                char_index = len(current_full_text) # 인덱스 초과 방지
                typing_finished = True # ★ 다 썼다! 이제 클릭을 기다리자.

        # 보여줄 글자 자르기
        display_text = current_full_text[:char_index]
        
        # --- [3. 그리기] ---
        window.blit(grandma, (0,0))
        window.blit(talking,(100,250))
        
        text_grandma = font.render(display_text, True, (0, 100, 100))
        text_player = font.render(display_text, True, (50, 50, 50))
        
        # 텍스트 렌더링
        if (idx == 0 or idx == 1 or idx == 3):
            window.blit(text_grandma, (200, 600))
        else:
            window.blit(text_player, (200, 600))
        pygame.display.update()

def f_hard(window):
    clock = pygame.time.Clock()
    pygame.event.clear()
    
    font = pygame.font.Font("DungGeunMO.ttf", 40)
    texts = ["내가 너에게 마지막으로 전할 말이 있다...", "비상상황 발생!!"]
    
    # 변수 초기화
    display_text = ""
    char_index = 0
    idx = 0
    
    # ★ '타이핑이 끝났는지' 확인하는 변수 (True면 클릭 대기 상태)
    typing_finished = False 

    last_time = pygame.time.get_ticks()
    typing_speed = 50 # (18은 너무 빠를 수 있어 조금 늦췄습니다)

    f_fade_in(window, grandma)

    play = True
    while play:
        clock.tick(60)
        
        # --- [안전장치] ---
        # 인덱스가 리스트 범위를 넘어가면 종료 (대화 끝)
        if idx >= len(texts):
            f_fade_out(window, grandma)

            return 8

        # 현재 출력해야 할 전체 문장
        current_full_text = texts[idx]

        # --- [1. 이벤트 처리] ---
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                return -1
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ★★★ 핵심 로직 ★★★
                if typing_finished:
                    # 1. 타이핑이 끝난 상태라면 -> 다음 문장으로!
                    idx += 1
                    char_index = 0      # 글자 수 초기화
                    typing_finished = False # 다시 타이핑 상태로 변경
                    if (idx == 1):
                        sfx_siren.play()
                else:
                    # 2. (선택사항) 타이핑 중인데 클릭하면? -> 즉시 완성 (스킵 기능)
                    char_index = len(current_full_text)
        
        # --- [2. 타이핑 로직] ---
        current_time = pygame.time.get_ticks()
        
        # 타이핑이 아직 안 끝났다면 글자 수 증가
        if not typing_finished:
            if current_time - last_time > typing_speed:
                char_index += 1
                last_time = current_time
                if (idx < 1):
                    sfx_type.play()

            
            # 문장 끝까지 다 썼는지 확인
            if char_index >= len(current_full_text):
                char_index = len(current_full_text) # 인덱스 초과 방지
                typing_finished = True # ★ 다 썼다! 이제 클릭을 기다리자.

        # 보여줄 글자 자르기
        display_text = current_full_text[:char_index]
        
        # --- [3. 그리기] ---
        window.blit(grandma, (0,0))
        window.blit(talking,(100,250))
        
        # 텍스트 렌더링
        text_grandma = font.render(display_text, True, (0, 100, 100))
        text_emergency = font.render(display_text, True, (255,0,0))
        # 텍스트 렌더링
        if (idx == 0):
            window.blit(text_grandma, (200, 600))
        else:
            window.blit(text_emergency, (200,600))
        pygame.display.update()

def f_story1(window):
    clock = pygame.time.Clock()
    pygame.event.clear()
    
    font = pygame.font.Font("DungGeunMO.ttf", 40)
    texts = ["비상상황 발생!!", "어..? 이게 무슨일이지..?", "모두 깐따삐아행 우주선에 탑승바랍니다."]
    
    # 변수 초기화
    display_text = ""
    char_index = 0
    idx = 0
    
    # ★ '타이핑이 끝났는지' 확인하는 변수 (True면 클릭 대기 상태)
    typing_finished = False 

    last_time = pygame.time.get_ticks()
    typing_speed = 50 # (18은 너무 빠를 수 있어 조금 늦췄습니다)

    f_fade_in(window, bedroom)

    play = True
    while play:
        clock.tick(60)
        
        if idx >= len(texts):
            f_fade_out(window, bedroom)
            return 9

        current_full_text = texts[idx]

        # --- [1. 이벤트 처리] ---
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                return -1
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ★★★ 핵심 로직 ★★★
                if typing_finished:
                    # 1. 타이핑이 끝난 상태라면 -> 다음 문장으로!
                    idx += 1
                    char_index = 0      # 글자 수 초기화
                    typing_finished = False # 다시 타이핑 상태로 변경
                else:
                    # 2. (선택사항) 타이핑 중인데 클릭하면? -> 즉시 완성 (스킵 기능)
                    char_index = len(current_full_text)
        
        # --- [2. 타이핑 로직] ---
        current_time = pygame.time.get_ticks()
        

        # 타이핑이 아직 안 끝났다면 글자 수 증가
        if not typing_finished:
            if current_time - last_time > typing_speed:
                char_index += 1
                last_time = current_time
                sfx_type.play()
            
            # 문장 끝까지 다 썼는지 확인
            if char_index >= len(current_full_text):
                char_index = len(current_full_text) # 인덱스 초과 방지
                typing_finished = True # ★ 다 썼다! 이제 클릭을 기다리자.

        # 보여줄 글자 자르기
        display_text = current_full_text[:char_index]
        
        # --- [3. 그리기] ---
        window.blit(bedroom, (0,0))
        window.blit(talking,(100,250))
        
        text_player = font.render(display_text, True, (50, 50, 50))
        text_emergency = font.render(display_text, True, (255,0,0))
        # 텍스트 렌더링
        if (idx == 0 or idx == 2):
            window.blit(text_emergency, (200,600))
        else:
            window.blit(text_player, (200, 600))

        pygame.display.update()

def f_story2(window):
    clock = pygame.time.Clock()
    pygame.event.clear()
    
    font = pygame.font.Font("DungGeunMO.ttf", 40)
    texts = ["깐따삐아행 마지막 우주선 출입문 닫습니다.", "안돼!!!!!!!", "출발합니다.", "(우주선이 출발한다)", "이대로 죽을 순 없어..", "내가 우주선을 만들어서 탈출하겠어!"]
    
    # 변수 초기화
    display_text = ""
    char_index = 0
    idx = 0
    
    # ★ '타이핑이 끝났는지' 확인하는 변수 (True면 클릭 대기 상태)
    typing_finished = False 

    last_time = pygame.time.get_ticks()
    typing_speed = 50 # (18은 너무 빠를 수 있어 조금 늦췄습니다)

    f_fade_in(window, outside)

    play = True
    while play:
        clock.tick(60)
        
        if idx >= len(texts):
            return 11
        if idx == 3:
            sfx_siren.stop()

        current_full_text = texts[idx]

        # --- [1. 이벤트 처리] ---
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                return -1
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ★★★ 핵심 로직 ★★★
                if typing_finished:
                    # 1. 타이핑이 끝난 상태라면 -> 다음 문장으로!
                    idx += 1
                    char_index = 0      # 글자 수 초기화
                    typing_finished = False # 다시 타이핑 상태로 변경
                    if (idx == 3):
                        sfx_arrive.play()
                    elif (idx == 4):
                        sfx_arrive.stop()
                else:
                    # 2. (선택사항) 타이핑 중인데 클릭하면? -> 즉시 완성 (스킵 기능)
                    char_index = len(current_full_text)
        
        # --- [2. 타이핑 로직] ---
        current_time = pygame.time.get_ticks()
        

        # 타이핑이 아직 안 끝났다면 글자 수 증가
        if not typing_finished:
            if current_time - last_time > typing_speed:
                char_index += 1
                last_time = current_time
                sfx_type.play()
            
            # 문장 끝까지 다 썼는지 확인
            if char_index >= len(current_full_text):
                char_index = len(current_full_text) # 인덱스 초과 방지
                typing_finished = True # ★ 다 썼다! 이제 클릭을 기다리자.

        # 보여줄 글자 자르기
        display_text = current_full_text[:char_index]
        
        # --- [3. 그리기] ---
        window.blit(outside, (0,0))
        window.blit(talking,(100,250))
        
        text_player = font.render(display_text, True, (50, 50, 50))
        text_emergency = font.render(display_text, True, (255,0,0))
        # 텍스트 렌더링
        if (idx == 0 or idx == 2):
            window.blit(text_emergency, (200,600))
        else:
            window.blit(text_player, (200, 600))

        pygame.display.update()

def f_fade_in(window, background_img): 
    # 1. 화면 크기와 똑같은 '검은색 막'을 만듭니다.
    fade = pygame.Surface((1200, 800)) 
    fade.fill((0, 0, 0)) # 검은색 채우기
    
    # 2. 투명도를 255(불투명)에서 0(투명)까지 줄여나갑니다.
    # (range의 세 번째 인자가 속도입니다. -2는 느리게, -5는 빠르게)
    for alpha in range(255, -1, -5):
        
        # --- [이벤트 처리] ---
        # (페이드인 중에도 종료 버튼은 먹어야 하므로)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1 

        # --- [그리기 순서] ---
        
        # 1. 뒤에 깔릴 배경을 먼저 그립니다. (이게 있어야 서서히 나타나는 것처럼 보임)
        window.blit(background_img, (0,0)) 
        
        # 2. 그 위에 검은 막(fade)의 투명도를 조절합니다.
        fade.set_alpha(alpha)
        
        # 3. 검은 막을 덮어씌웁니다.
        window.blit(fade, (0, 0))
        
        # 4. 화면 갱신 & 속도 조절
        pygame.display.update()
        pygame.time.delay(10) # 0.03초 대기 (부드럽게)

def f_fade_out(window, last_screen_img):
    # 1. 검은 막 생성
    fade = pygame.Surface((1200, 800))
    fade.fill((0, 0, 0))
    
    # 2. 투명도를 0(투명)에서 255(완전 검정)까지 높여갑니다.
    # (속도를 높이려면 5를 더 큰 숫자로 바꾸세요)
    for alpha in range(0, 256, 5):
        
        # --- [이벤트 처리] (멈춤 방지) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1

        # --- [그리기] ---
        # 1. 사라질 화면(배경)을 밑에 깝니다.
        window.blit(last_screen_img, (0,0))
        
        # 2. 그 위에 검은 막의 투명도를 조절해 덮습니다.
        fade.set_alpha(alpha)
        window.blit(fade, (0, 0))
        
        # 3. 갱신 & 대기
        pygame.display.update()
        pygame.time.delay(10) # 부드러운 연출을 위한 딜레이
