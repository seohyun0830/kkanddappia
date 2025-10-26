import pygame
import inven
import player
import map

pygame.init()

# 화면 크기
window_width = 1200
window_height = 800
window = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("Kkanddappia!")

# 기본세팅
fps = pygame.time.Clock()                       # fps 설정
pix = 60                                        # 한 칸에 60 픽셀

# 클래스 가져오기
Map = map.Cmap(window, pix)
col = Map.col
row = Map.row

Player = player.Cplayer(col, row, pix)
bX, bY = Player.blockX, Player.blockY

Map.underMap[bY][bX] = 1

play = True
while play:
    deltaTime = fps.tick(60)                # fps 설정
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            play = False
        # 키를 뗐을 때
        if event.type == pygame.KEYUP:
            Player.f_setDefault()

    # 눌러진 키 값 받아옴
    keys = pygame.key.get_pressed() 
    
    # 중력 설정 (같은 x 값에서 가장 밑으로 가도록)
    Player.f_gravity(Map.underMap)

    # 왼쪽 키가 눌렸을 때
    if keys[pygame.K_LEFT]:
        Player.blockX = (Player.realX) // pix
        Player.f_left(Map.underMap)
    # 오른쪽
    if keys[pygame.K_RIGHT]:
        Player.blockX = (Player.realX) // pix
        Player.f_right(Map.underMap)

    # 지금 구현에서는 점프하는게 아니라 그냥 위칸에 옮겨놓으면 중력으로 떨어짐
    if keys[pygame.K_UP]:
        Player.f_up(Map.underMap)

    # 약간 애매하게 걸쳐있으면 밑에 블록이 이상하게 깨지는듯
    if keys[pygame.K_DOWN]:
        Player.f_down(window, Map.underMap)

    Map.f_drawMap(window, Map.underMap, Player.direction, Player.blockX, Player.blockY, Player.blockMotion, pix)

    Player.f_drawPlayer(window)

    # tab 키 누르면 인벤토리 뜨도록
    if keys[pygame.K_TAB]:
        inven.f_inven(window, pix, col, row)

    pygame.display.update()

'''
버그 고치고, 광물 배치하기, 인벤구현, 지하수 터지는 실패


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
    13. 사다리

    버그
    1. 왜 x가 안되냐
    2. 다시하기는 왜 한번밖에 안되는거지
    '''