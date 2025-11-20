import pygame
import sys
import math

# --- 모듈 불러오기 ---
from setting import *
import images
from player import Player
from map import MapManager
from inven import Inventory
from make import CraftingManager
from dic import Dictionary

# --- 초기화 ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("KKANDDABBIA! - Refactored")
clock = pygame.time.Clock()

# --- 에셋 로드 (가장 먼저!) ---
images.load_all_assets()

# --- 객체 생성 ---
player = Player()
map_mgr = MapManager()
inven = Inventory()
maker = CraftingManager()
dictionary = Dictionary()

# --- 전역 변수 및 상태 ---
game_over = False
done = False

# 드래그 관련
is_drag = False
drag_item_name = None
drag_offset_x = 0
drag_offset_y = 0

# 나무 캐기 관련
is_tree_pressing = False
tree_press_start_time = 0
GATHER_DURATION = 3000
TREE_AREA = pygame.Rect(840, 430, 120, 290) # setting.py로 옮겨도 좋음

# 우주선 관련
pulsate_time_start = pygame.time.get_ticks()
PULSATE_SPEED = 0.003 
PULSATE_MIN_SCALE = 0.9
PULSATE_MAX_SCALE = 1.1
SPACESHIP_AREA = pygame.Rect(900, 600, 280, 100)

# 엔딩(비행) 관련
is_flying = False
fly_start_time = 0

# 페이드 아웃
is_fading_out = False
FADE_SPEED = 5

def handle_drag_start(mouse_pos):
    """드래그 시작 로직 통합"""
    global is_drag, drag_item_name, drag_offset_x, drag_offset_y
    
    # 1. 제작창 슬롯에서 드래그 (제작 중인 재료 회수)
    if maker.is_open:
        item = maker.handle_click_craft_slot(mouse_pos)
        if item:
            is_drag = True
            drag_item_name = item
            # 오프셋은 대략 마우스 중심
            drag_offset_x = ITEM_SIZE // 2
            drag_offset_y = ITEM_SIZE // 2
            return

    # 2. 인벤토리에서 드래그
    # 제작창이 열려있으면 인벤토리가 오른쪽으로 밀려있음 (shift값 계산)
    shift_x = 280 if maker.is_open else 0 # 280은 원본 코드의 위치 차이
    
    item = inven.handle_click_item(mouse_pos, shift_x)
    if item:
        is_drag = True
        drag_item_name = item
        drag_offset_x = ITEM_SIZE // 2
        drag_offset_y = ITEM_SIZE // 2

def handle_drag_end(mouse_pos):
    """드래그 종료(드롭) 로직 통합"""
    global is_drag, drag_item_name
    
    if not is_drag: return

    # 1. 제작창/우주선창에 드롭 시도
    if maker.handle_drop(mouse_pos, drag_item_name, inven):
        # 성공적으로 들어감
        pass
    
    # 2. 외부 맵 우주선에 드롭 (Stage 3 조건)
    elif map_mgr.current_map == "outside2" and SPACESHIP_AREA.collidepoint(mouse_pos):
        if maker.add_spaceship_part(drag_item_name):
             pass # 성공
        else:
            inven.add_item(drag_item_name) # 실패 시 반환
            
    # 3. 실패 (다시 인벤토리로)
    else:
        inven.add_item(drag_item_name)

    is_drag = False
    drag_item_name = None

# --- 메인 루프 ---
while not done:
    current_time = pygame.time.get_ticks()
    
    # 1. 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # --- 마우스 클릭 (DOWN) ---
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and not is_flying:
            mouse_pos = pygame.mouse.get_pos()
            
            # ---------------------------------------------------------
            # 1. 아이콘 클릭 처리 (최우선 순위)
            # ---------------------------------------------------------
            
            # (1) 사전 아이콘 및 페이지 넘김
            # handle_click은 아이콘 클릭이나 페이지 클릭 시 True를 반환
            if dictionary.handle_click(mouse_pos):
                if dictionary.is_open: 
                    inven.is_open = False
                    maker.is_open = False
                    maker.is_spaceship_open = False
                continue # 처리했으면 루프 넘김
                
            # (2) 가방 아이콘
            if inven.icon_rect.collidepoint(mouse_pos):
                is_open = inven.toggle()
                if is_open:
                    maker.is_open = False
                    dictionary.is_open = False
                    maker.is_spaceship_open = False
                else:
                    maker.is_open = False
                continue

            # ---------------------------------------------------------
            # 2. [추가된 기능] 창 밖 클릭 시 닫기
            # ---------------------------------------------------------
            # 현재 열려있는 모든 창의 영역(Rect)을 계산합니다.
            active_windows = []
            
            if dictionary.is_open:
                active_windows.append(dictionary.rect)
            
            if inven.is_open:
                # 제작창이 열려있으면 인벤토리가 오른쪽으로 밀림
                shift_x = 280 if maker.is_open else 0
                inv_rect = pygame.Rect(inven.center_x + shift_x, inven.y, inven.image.get_width(), inven.image.get_height())
                active_windows.append(inv_rect)
                
            if maker.is_open:
                mk_rect = pygame.Rect(maker.x, maker.y, maker.bg_image.get_width(), maker.bg_image.get_height())
                active_windows.append(mk_rect)
                
            if maker.is_spaceship_open:
                sp_rect = pygame.Rect(maker.sp_x, maker.sp_y, maker.spaceship_bg.get_width(), maker.spaceship_bg.get_height())
                active_windows.append(sp_rect)
            
            # 창이 하나라도 열려있을 때
            if active_windows:
                # 마우스가 어떤 창의 영역 안에도 없고(Outside) + 아이콘 위도 아니라면
                clicked_inside_window = any(rect.collidepoint(mouse_pos) for rect in active_windows)
                clicked_on_icon = inven.icon_rect.collidepoint(mouse_pos) or dictionary.icon_rect.collidepoint(mouse_pos)
                
                if not clicked_inside_window and not clicked_on_icon:
                    # 모든 창 닫기
                    inven.is_open = False
                    maker.is_open = False
                    maker.is_spaceship_open = False
                    dictionary.is_open = False
                    continue # 닫았으면 맵 클릭 같은 건 하지 말고 넘김

            # ---------------------------------------------------------
            # 3. 열린 창 내부 기능 처리 (버튼, 드래그)
            # ---------------------------------------------------------
            if inven.is_open or maker.is_spaceship_open:
                
                # 제작 버튼 (M)
                if maker.is_open and maker.button_rect.collidepoint(mouse_pos):
                    if not maker.check_recipe(inven):
                        game_over = True
                    continue

                # 드래그 시작 시도
                handle_drag_start(mouse_pos)
                
                # 드래그나 버튼을 눌렀다면 여기서 멈춤 (맵 클릭 방지)
                # (단, 드래그 시작이 안됐다면 아래 맵 클릭으로 넘어갈 수도 있으니 주의, 
                # 하지만 위에서 '창 밖 클릭'을 이미 걸러냈으므로 여기 왔다는 건 '창 안'을 클릭했다는 뜻)
                pass 

            # ---------------------------------------------------------
            # 4. 맵 상호작용 (창이 모두 닫혀있을 때만!)
            # ---------------------------------------------------------
            if not (inven.is_open or maker.is_open or maker.is_spaceship_open or dictionary.is_open):
                
                # [Outside1] 나무 캐기
                if map_mgr.current_map == "outside1" and TREE_AREA.collidepoint(mouse_pos):
                    is_tree_pressing = True
                    tree_press_start_time = current_time
                
                # [Outside1] 문 (Inside로 이동)
                if map_mgr.current_map == "outside1" and pygame.Rect(400, 400, 400, 300).collidepoint(mouse_pos):
                    map_mgr.current_map = "inside"
                    player.x = 100
                    
                # [Inside] 책상 클릭 (제작창 열기)
                if map_mgr.current_map == "inside" and pygame.Rect(850, 100, 300, 380).collidepoint(mouse_pos):
                    inven.is_open = True
                    maker.is_open = True
                    
                # [Outside2] 우주선
                if map_mgr.current_map == "outside2" and SPACESHIP_AREA.collidepoint(mouse_pos):
                    if maker.is_spaceship_complete():
                        player.is_walking_into_spaceship = True
                        player.x = 0 
                        player.y = 500
                    elif 'spaceship' in inven.items:
                        maker.is_spaceship_open = True
                        inven.is_open = True

        # --- 마우스 떼기 (UP) ---
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            
            # 나무 캐기 중단
            if is_tree_pressing:
                is_tree_pressing = False
            
            # 드래그 드롭
            handle_drag_end(mouse_pos)


    # 2. 게임 로직 업데이트
    
    if is_flying:
        # 엔딩 컷신 중
        pass 
    
    elif player.is_walking_into_spaceship:
        player.update()
        player.x += player.speed
        if player.x >= SCREEN_WIDTH - 100: # 충분히 걸어갔으면
            player.is_walking_into_spaceship = False
            is_flying = True
            fly_start_time = current_time
    
    elif game_over:
        pass # 게임 오버 상태

    else:
        # 플레이어 이동
        if not (dictionary.is_open or maker.is_open or maker.is_spaceship_open or is_tree_pressing):
            keys = pygame.key.get_pressed()
            player.move(keys)
            player.update()
        
        # 맵 이동 체크
        map_mgr.check_map_transition(player)
        
        # 아이템 줍기 체크 (충돌)
        map_mgr.check_item_pickup(player, inven.items)
        
        # 나무 캐기 완료 체크
        if is_tree_pressing and (current_time - tree_press_start_time >= GATHER_DURATION):
            map_mgr.add_dropped_item('wood', TREE_AREA.centerx, player.y + 100)
            is_tree_pressing = False


    # 3. 화면 그리기
    screen.fill(BLACK) # 기본 배경

    if is_flying:
        # 엔딩 컷신 그리기
        bg = images.backgrounds.get('2to3') # 배경
        if bg: screen.blit(bg, (0,0))
        
        ship = images.animations.get('fly_spaceship')
        if ship:
            # 간단한 위로 날아가는 효과
            elapsed = current_time - fly_start_time
            fly_y = SCREEN_HEIGHT - (elapsed * 0.5) # 천천히 위로
            screen.blit(ship, ((SCREEN_WIDTH - 250)//2, fly_y))
            
    else:
        # (1) 배경 & 바닥 아이템
        map_mgr.draw_background(screen)
        map_mgr.draw_items(screen)
        
        # (2) 플레이어
        if not player.is_walking_into_spaceship: # 탑승 중일 땐 배경 위, 우주선 뒤 등 레이어 고려 필요
             player.draw(screen)

        # (3) 맵 전용 오브젝트 (Outside2 우주선)
        if map_mgr.current_map == "outside2":
            # 완성된 우주선 깜빡임 효과
            if maker.is_spaceship_complete():
                time_factor = (current_time - pulsate_time_start) * PULSATE_SPEED
                scale = PULSATE_MIN_SCALE + (math.sin(time_factor) + 1) / 2 * (PULSATE_MAX_SCALE - PULSATE_MIN_SCALE)
                
                original_img = images.item_images.get('spaceship_completed')
                if original_img:
                    w = int(original_img.get_width() * scale)
                    h = int(original_img.get_height() * scale)
                    scaled_img = pygame.transform.scale(original_img, (w, h))
                    # 위치 보정 (중심 기준)
                    draw_x = SPACESHIP_AREA.centerx - w // 2
                    draw_y = SPACESHIP_AREA.top - h - 50 # 원본 위치 조정
                    screen.blit(scaled_img, (draw_x, draw_y))
            
            # 진행도 게이지 (항상 표시 or 조립중일때만? 원본은 항상)
            # 게이지 그리기 로직은 복잡하므로 간단히 텍스트로 대체하거나 원본 draw_rect 로직 가져오면 됨
            progress = maker.get_spaceship_progress()
            # ... 게이지 그리기 생략 (필요하면 추가) ...

        # (4) 탑승 애니메이션 중인 플레이어 (우주선보다 앞에 그려야 한다면 순서 조정)
        if player.is_walking_into_spaceship:
             player.draw(screen)

        # (5) UI 창 (Layer 순서: 배경 -> 플레이어 -> 창 -> 아이템)
        shift_x = 280 if maker.is_open else 0
        
        maker.draw(screen) # 제작창/우주선창
        inven.draw(screen, shift_x) # 인벤토리
        dictionary.draw(screen) # 사전

        # (6) 나무 캐기 게이지
        if is_tree_pressing:
            elapsed = current_time - tree_press_start_time
            progress = min(1.0, elapsed / GATHER_DURATION)
            bar_w = 100
            bar_h = 10
            bx = TREE_AREA.centerx - bar_w // 2
            by = TREE_AREA.y - 20
            pygame.draw.rect(screen, (50,50,50), (bx, by, bar_w, bar_h))
            pygame.draw.rect(screen, (0,200,0), (bx, by, bar_w * progress, bar_h))

        # (7) 드래그 중인 아이템 (가장 최상단)
        if is_drag and drag_item_name:
            img = images.item_images.get(drag_item_name)
            if img:
                mx, my = pygame.mouse.get_pos()
                screen.blit(img, (mx - drag_offset_x, my - drag_offset_y))

        # (8) 게임 오버 텍스트
        if game_over:
            screen.fill(BLACK)
            txt = images.fonts['default'].render("GAME OVER", True, RED)
            screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, SCREEN_HEIGHT//2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()