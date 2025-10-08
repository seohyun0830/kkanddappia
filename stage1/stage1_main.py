import os
import sys
import pygame
from fail_magma import *
from images import *

pygame.init()

# 화면 크기
window_width = 1200
window_height = 800
window = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("Kkanddappia!")

# 기본세팅
fps = pygame.time.Clock()                       # fps 설정
pix = 60                                        # 한 칸에 60 픽셀
col = (window_width + pix - 10) // pix           # 총 열r
row = (window_height + pix - 10) // pix          # 총 행
under_map = [[0]* col for _ in range(row)]      # 맵 블록 디자인 (채워짐 = 0, 비워짐 = 1)

# 블록으로 캐릭터 위치
c_x = (col - 2)
c_y = 0
# 실제 캐릭터 위치
r_x = c_x * pix
r_y = c_y * pix

# 초기 시작 위치는 비워져있도록
under_map[c_y][c_x] = 1

# 각 변수별 flag
d = 0       # 캐릭터 방향 -> 왼: 0, 오: 1, 아: 2
m = 0       # 이동 모션
m_time = 0  # 모션 바뀌는 시간 측정
b = 0       # 블록 넘버 (깨지는 모양)
b_time = 0    # 블록 깨지는 시간
p = 0
f = 0       # 실패 조건

#jumping = 0

# 캐릭터 스피드는 아직 안쓰긴 함
character_speed = 1
play = True

while play:
    deltaTime = fps.tick(60)                # fps 설정
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            play = False
        # 키를 뗐을 때
        if event.type == pygame.KEYUP:
            b = 0
            b_time = 0
            m = 0
            m_time = 0
            if d == 2: d = 0
            elif d == 3: d = 1

    # 눌러진 키 값 받아옴
    keys = pygame.key.get_pressed() 

    # 한 프레임에서 움직인 값
    r_to_x = 0
    r_to_y = 0
    
    # 중력 설정 (같은 x 값에서 가장 밑으로 가도록)
    for i in range(c_y + 1, row):
        if (under_map[i][c_x] == 1):
            r_to_y += 5
        else:
            break

    # 왼쪽 키가 눌렸을 때
    if keys[pygame.K_LEFT]:
        c_x = (r_x + pix - 1) // pix    # 블록 기준 위치 설정
        d = 0                           # 방향 설정

        # 이동 모션 설정
        m_time += 1
        if m_time > 8:                  
            if m == 1 or m == 0 or m == 3:
                m = 2
            elif m == 2:
                m = 1
            m_time = 0

        # 범위를 맵 안으로 제한
        if c_x <= 0:
            r_to_x = 0
        # 만약 범위 안에 있고, 왼쪽에 장애물이 없다면 옆으로 이동
        elif r_x >= 0 and under_map[c_y][c_x - 1] == 1:
            r_to_x = -1
        # 아니라면 블록깨기
        else:
            m = 3
            m_time = 0
            b_time += 1
            if b_time > 30:
                under_map[c_y][c_x - 1] = 1
                b = 0
                b_time = 0
            elif b_time > 20:
                b = 3
                p = 0
            elif b_time > 10:
                b = 2
                p = 1
            elif b_time > 0:
                b = 1
                p = 0
    # 오른쪽
    if keys[pygame.K_RIGHT]:
        c_x = (r_x) // pix
        d = 1
        m_time += 1
        if m_time > 8:
            if m == 1 or m == 0 or m == 3:
                m = 2
            elif m == 2:
                m = 1
            m_time = 0
        #
        if c_x >= col - 1:
            r_to_x = 0
        elif c_x < col - 1 and under_map[c_y][c_x + 1] == 1:
           r_to_x = 1
        else:
            m = 3
            b_time += 1
            if b_time > 30:
                under_map[c_y][c_x + 1] = 1
                b_time = 0
                b = 0
            elif b_time > 20:
                b = 3
                p = 0
            elif b_time > 10:
                b = 2
                p = 1
            elif b_time > 0:
                b = 1
        # 점프가 진자 심각함
    
    # 점프는 어케구현해야할까
    # 지금 구현에서는 점프하는게 아니라 그냥 위칸에 옮겨놓으면 중력으로 떨어지는듯
    if keys[pygame.K_UP]:
        if c_y > 0 and under_map[c_y - 1][c_x] == 1:
            jumping = 1
            r_to_y -= 60
        else:
            pass

    # 약간 애매하게 걸쳐있으면 밑에 블록이 이상하게 깨지는듯
    if keys[pygame.K_DOWN]:
        # 맨 아래 땅 파면 마그마 나오면서 종료
        if (c_y + 1 == row):
            func_fail_magma(window)
            
        if d == 0: d = 2
        elif d == 1: d = 3
        if c_y < row and under_map[c_y + 1][c_x] == 1:
           c_to_y = 1
        else:
            b_time += 1
            if b_time > 30:
                under_map[c_y + 1][c_x] = 1
                b_time = 0
                b = 0
            elif b_time > 20:
                b = 3
                p = 0
            elif b_time > 10:
                b = 2
                p = 1
            elif b_time > 0:
                b = 1
                p = 0
    r_x += r_to_x * character_speed
    r_y += r_to_y
    c_y = r_y // pix
    #c_y += c_to_y

    # draw map
    window.blit(background, (0,0))
    for i in range(row):
        for j in range(col):
            if (under_map[i][j] == 1):
                continue
            if (d == 0 and j == c_x - 1 and i == c_y):
                window.blit(blocks[b], ((j) * pix, i * pix))
            elif (d == 1 and j == c_x + 1 and i == c_y):
                window.blit(blocks[b], ((j) * pix, i * pix))
            elif ((d == 2 or d == 3) and j == c_x and i == c_y + 1):
                window.blit(blocks[b], ((j) * pix, i * pix))
            
            else: window.blit(blocks[0], (j * pix, i * pix))
    
    #window.blit(characters[d][m], (r_x, (c_y) * 60))
    window.blit(characters[d][m], (r_x, r_y))

    if b != 0:
        window.blit(picks[d][p],(r_x, (c_y) * 60))

    # tab 키 누르면 인벤토리 뜨도록
    if keys[pygame.K_TAB]:
        for i in range(1, col // 2 - 1):
            for j in range(1, row // 2 - 2):
                window.blit(inven, (i * pix * 2, j * pix * 2))


    pygame.display.update()

'''
    아직 해야할 일
    1. 점프가 일단 이상함
    2. 탭 누르면 인벤토리 -> 일단 했어 근데 인벤 몇개 정도 하는게 나을까
    4. 용암설정 -> 이것도 일단 했는데 모션 넣고싶어
    5. 맵에 광물, 석유 넣기
    6. 지하수 설정
    7. 맵을 확장할까
    8. 그 픽셀 안에서 좀 애매하게 있으면 아래로 땅이 이상하게 파져
    9. 인벤에서 마우스 올려놓으면 정보 뜨게 하는 것도 ㄱㅊ을거같은데?
    10. 땅 하나 남으면 무너지도록 구현
    11. 그럼 두더지는 그냥 마이너스 요소로 하고싶네
    12. 출입구 표시도 해야됨
    
    버그
    1. 왜 x가 안되냐
    2. 다시하기는 왜 한번밖에 안되는거지
    '''