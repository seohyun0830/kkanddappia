import pygame
from stage1.images import *
from .images import btn_background, sfx_click

def f_isClicked(btnX, btnY, xPos, yPos):
    if xPos > btnX and xPos < btnX + 360 and yPos > btnY and yPos < btnY + 108:
        return 1

def f_isFail(window, reson):
    pygame.event.clear()

    font = pygame.font.Font('DungGeunMO.ttf', 90)
    text_hover = font.render("RESTART", False, (0, 0, 0))     # 검은색 (마우스 올렸을 때)
    text_normal = font.render("RESTART", False, (255, 255, 255)) # 흰색 (평소)

    fps = pygame.time.Clock()
    play = True
    
    # 버튼 위치 변수화 (유지보수 용이)
    btn_x, btn_y = 800, 600
    time = 0

    while play:
        fps.tick(60)
        
        # 2. 마우스 위치 및 충돌 확인을 "이벤트 처리 전"에 합니다.
        xPos, yPos = pygame.mouse.get_pos()
        is_hover = f_isClicked(btn_x, btn_y, xPos, yPos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            
            if event.type == pygame.MOUSEBUTTONDOWN:  
                # 3. 미리 계산해둔 hover 상태를 확인합니다.
                if is_hover:
                    sfx_click.play()
                    return True # (메인 루프의 1스테이지 코드가 11번이라면 11로, 10이면 10으로 맞추세요)

        # 4. 그리기
        time += 1
        idx = time // 40
        if (idx >= len(reson)):
            idx = len(reson) - 1
        window.blit(reson[idx], (0,0))
        window.blit(btn_background, (btn_x, btn_y))
        
        # hover 상태에 따라 다른 텍스트 이미지 그리기
        if is_hover:
            window.blit(text_hover, (btn_x + 20, btn_y))
        else:
            window.blit(text_normal, (btn_x + 20, btn_y))

        pygame.display.update()