import pygame
from . import inven
from . import player
from . import map
from . import images
from . import sounds
from . import guide

# flag 인자
# 0: 처음 시작 (+가이드) 1: 재시작(리셋) 2: 다시 돌아왔을 때(저장된 상태)
def f_stage1(window, MODE, Try, MapInfo, ItemMapInfo, InvenInfo, InvenCnt, timer):
    # --- [초기화] ---
    fps = pygame.time.Clock()
    pix = 60

    # 객체 생성
    Map = map.Cmap(window, pix)
    col, row = Map.col, Map.row # 자주 쓰는 변수는 미리 꺼내두기

    Player = player.Cplayer(col, row, pix)
    Inven = inven.Cinven(pix, row, col)

    # 초기 맵 설정
    # (Player의 초기 blockX, blockY를 사용하여 설정)
    Map.underMap[Player.blockY][Player.blockX] = 1
    if (Try == 0):
        Map.f_defaultItemMap(MODE)
    else:
        Map.underMap = MapInfo
        Map.itemMap = ItemMapInfo
        Inven.invenList = InvenInfo
        Inven.invenCnt = InvenCnt
    Inven.f_blockCount()

    # 변수 초기화
    isLadder = False
    isDragging = False
    upX, upY = -1, -1
    flag = False
    isTab = False
    
    # 최적화를 위한 이전 좌표 기록 변수
    prev_bx, prev_by = -1, -1
    play = True
    while play:
        deltaTime = fps.tick(50)

        if (timer.get_remianing_time() <= 0):
            return 3, None, None, None, None

        # --- [1. 이벤트 처리] ---
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                play = False
                return 0, None, None, None, None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flag = True

            if event.type == pygame.KEYUP:
                Player.f_setDefault()
                flag = False

            # 마우스 클릭 (드래그 시작)
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickX, clickY = event.pos
                isDragging = True
                if (isTab):
                    isLadder = Inven.f_isLadder(clickX, clickY) # 사다리인지 확인
                    print(isLadder  )
                if (isLadder): 
                    Inven.invenCnt[4] -= 1
                    if (Inven.invenCnt[4] <= 0):
                        Inven.invenList.remove(5)
                upX, upY = -1, -1 # 초기화

            # 마우스 떼기 (드래그 끝)
            if event.type == pygame.MOUSEBUTTONUP:
                upX, upY = event.pos
                isDragging = False

        # --- [2. 게임 로직 업데이트] ---
        keys = pygame.key.get_pressed()

        # 중력 및 물리 적용
        Player.f_gravity(Map.underMap, Map.itemMap)
        
        # 실패 조건 체크
        if Player.blockY >= Player.row - 1: return 1, None, None, None, None # 마그마
        if Map.itemMap[Player.blockY][Player.blockX] == -1: return 2, None, None, None, None # 지하수

        # 플레이어 블록 좌표 갱신 (자주 쓰이니 변수에 저장)
        # Player 클래스 내부에서 realX 업데이트 시 blockX도 같이 업데이트하면 더 좋습니다.
        Player.blockX = (Player.realX + 30) // pix
        Player.blockY = (Player.realY) // pix
        
        bx, by = Player.blockX, Player.blockY # 지역 변수로 캐싱

        # 키 입력 이동
        if keys[pygame.K_LEFT]:  Player.f_left(Map.underMap, Map.itemMap)
        if keys[pygame.K_RIGHT]: Player.f_right(Map.underMap, Map.itemMap)
        if keys[pygame.K_DOWN]:  Player.f_down(Map.underMap)
        if keys[pygame.K_UP]:
            if bx == col - 3 and by == 0: return -1, Map.underMap, Map.itemMap, Inven.invenList, Inven.invenCnt  # 탈출 성공
            if Map.itemMap[by][bx] == 5 or Map.itemMap[by + 1][bx] == 5: Player.f_up(Map.itemMap) # 사다리 타기
            elif Map.itemMap[by - 1][bx] != 6 and Map.underMap[by - 1][bx] == 1:
                Player.f_jump() # 점프
            print(bx)
            print("up:", Map.itemMap[by - 1][bx], Map.underMap[by - 1][bx])
                

        # ★ 최적화: 플레이어 위치가 변했을 때만 아이템 획득 시도
        if (bx != prev_bx) or (by != prev_by):
            Inven.f_getItem(Map.itemMap, bx, by)
            prev_bx, prev_by = bx, by # 현재 위치 기억

        # 사다리 설치 로직
        if upX != -1 and upY != -1 and isLadder:
            Inven.f_putLadder(Map.underMap, Map.itemMap, upX, upY)
            upX, upY = -1, -1 # 처리 후 초기화
            isLadder = False

        # --- [3. 렌더링 (그리기)] ---
        window.blit(images.background, (0,0)) # 배경

        Map.f_drawItemMap(window) # 아이템
        Map.f_drawMap(window, Player.direction, bx, by, Player.blockMotion)
        
        # 맵 그리기 (인자가 많으니 순서 주의)
        
        Player.f_drawPlayer(window) # 플레이어

        # 인벤토리 및 드래그 UI (가장 위에 그려야 하므로 마지막에 배치)
        if keys[pygame.K_TAB]:
            isTab = True
            Inven.f_inven(window)
            Inven.f_invenInfo(window)
        else:
            isTab = False
            
            # 드래그 중인 사다리 그리기 (인벤토리가 켜져 있을 때만 보이게 할지 결정 필요)
            # 만약 인벤토리 밖에서도 드래그가 보여야 한다면 탭 키 밖으로 빼세요.
        if isDragging and isLadder:
            mouseX, mouseY = pygame.mouse.get_pos() # 필요할 때만 get_pos 호출
            Inven.f_ladder(mouseX, mouseY, window)
        
        
        if (Try == 0):
            guide.f_guide(window, flag, isTab, Inven.invenList, isDragging)

        timerText = timer.get_time_text()
        window.blit(timerText, (10, 10))
        pygame.display.update()