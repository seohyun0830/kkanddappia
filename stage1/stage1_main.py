import pygame
from . import inven
from . import player
from . import map
from . import images


def f_stage1(window):
    # 기본세팅
    fps = pygame.time.Clock()
    pix = 60                                        # 한 칸에 60 픽셀

    # 클래스 가져오기
    Map = map.Cmap(window, pix)
    col = Map.col
    row = Map.row

    Player = player.Cplayer(col, row, pix)
    bX, bY = Player.blockX, Player.blockY

    Inven = inven.Cinven(pix, row, col)

    Map.underMap[bY][bX] = 1
    Map.f_defaultItemMap()

    play = True
    while play:
        deltaTime = fps.tick(120)                # fps 설정
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                play = False
            # 키를 뗐을 때
            if event.type == pygame.KEYUP:
                Player.f_setDefault()

        # 눌러진 키 값 받아옴
        keys = pygame.key.get_pressed() 
        
        # 중력 설정 (같은 x 값에서 가장 밑으로 가도록)
        Player.f_gravity(Map.underMap, Map.itemMap)
        if (Player.blockY >= Player.row - 1):
            return 1
            
        # 왼쪽 키가 눌렸을 때
        if keys[pygame.K_LEFT]:
            Player.blockX = (Player.realX) // pix
            Player.f_left(Map.underMap, Map.itemMap)
        # 오른쪽
        if keys[pygame.K_RIGHT]:
            Player.blockX = (Player.realX) // pix
            Player.f_right(Map.underMap)

        # 지금 구현에서는 점프하는게 아니라 그냥 위칸에 옮겨놓으면 중력으로 떨어짐
        if keys[pygame.K_UP]:
            Player.f_up(Map.underMap,Map.itemMap)

        # 약간 애매하게 걸쳐있으면 밑에 블록이 이상하게 깨지는듯
        if keys[pygame.K_DOWN]:
            Player.f_down(Map.underMap)
        
        Inven.f_getItem(Map.itemMap, Player.realX, Player.realY)
        
        window.blit(images.background, (0,0))
        Map.f_drawItemMap(window)
        Map.f_drawMap(window, Player.direction, Player.blockX, Player.blockY, Player.blockMotion)

        Player.f_drawPlayer(window)

        # tab 키 누르면 인벤토리 뜨도록
        if keys[pygame.K_TAB]:
            Inven.f_inven(window)
            Inven.f_invenInfo(window)
            
        pygame.display.update()

'''
버그 고치고, 광물 배치하기, 인벤구현, 지하수 터지는 실패


    아직 해야할 일
    6. 지하수 설정
    9. 인벤에서 마우스 올려놓으면 정보 뜨게 하는 것도 ㄱㅊ을거같은데?
    10. 땅 하나 남으면 무너지도록 구현
    12. 출입구 표시도 해야됨
    13. 사다리

    버그
    1. 점프
    2. blockX 설정
    2. 다시하기는 왜 한번밖에 안되는거지
    '''