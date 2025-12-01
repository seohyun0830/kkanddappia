import pygame
import sys
from setting import *
from images import ImageManager
from player import Player
from map import MapManager

class Stage2Back:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        self.images = ImageManager()
        self.player = Player(self.images)
        self.map_manager = MapManager(self.images)
        
        # 인벤토리 (수집한 조각들의 화면상 위치 Rect 리스트)
        self.inventory_pieces = [] 
        
        # 드래그 앤 드롭 관련 변수
        self.is_dragging = False
        self.drag_index = -1 
        self.drag_offset = (0, 0) 
        
        self.done = False
        self.cutscene_active = False

    def run(self):
        while not self.done:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        return "stage3"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.cutscene_active:
                continue
            
            mouse_pos = pygame.mouse.get_pos()
            
            # --- [마우스 클릭] ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1. 우주선 완성 후 발사대 클릭 -> 컷신 시작
                if self.map_manager.assembled_count >= TOTAL_PIECES:
                    if LAUNCHPAD_RECT.collidepoint(mouse_pos):
                        self.cutscene_active = True
                        self.player.start_cutscene() 
                        return
                
                # [변경됨] 바닥 조각 클릭 수집 로직 삭제 (스치면 먹기로 변경됨)
                    
                # 2. 상단 인벤토리 드래그 시작
                for i, rect in enumerate(self.inventory_pieces):
                    if rect.collidepoint(mouse_pos):
                        self.is_dragging = True
                        self.drag_index = i
                        self.drag_offset = (rect.x - mouse_pos[0], rect.y - mouse_pos[1])
                        break
            
            # --- [마우스 이동 (드래그 중)] ---
            elif event.type == pygame.MOUSEMOTION:
                if self.is_dragging and self.drag_index != -1:
                    current_rect = self.inventory_pieces[self.drag_index]
                    current_rect.x = mouse_pos[0] + self.drag_offset[0]
                    current_rect.y = mouse_pos[1] + self.drag_offset[1]
            
            # --- [마우스 뗌 (드롭)] ---
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.is_dragging:
                    dropped_rect = self.inventory_pieces[self.drag_index]
                    
                    # 발사대 영역에 놓았는지 확인
                    if LAUNCHPAD_RECT.colliderect(dropped_rect):
                        self.inventory_pieces.pop(self.drag_index) 
                        self.map_manager.assembled_count += 1 
                        self.rearrange_inventory() 
                    else:
                        self.rearrange_inventory() # 실패 시 복구
                        
                    self.is_dragging = False
                    self.drag_index = -1

    def add_to_inventory(self):
        """수집한 조각을 상단 UI 인벤토리에 추가"""
        count = len(self.inventory_pieces)
        # 상단 UI 바(높이 100)의 중간쯤인 y=25에 배치
        x = 20 + (count * (PIECE_SIZE + 10))
        y = 25 
        new_rect = pygame.Rect(x, y, PIECE_SIZE, PIECE_SIZE)
        self.inventory_pieces.append(new_rect)

    def rearrange_inventory(self):
        """인벤토리 아이템들을 상단에 맞춰 정렬"""
        new_list = []
        for i in range(len(self.inventory_pieces)):
            x = 20 + (i * (PIECE_SIZE + 10))
            y = 25 # 상단 배치
            rect = pygame.Rect(x, y, PIECE_SIZE, PIECE_SIZE)
            new_list.append(rect)
        self.inventory_pieces = new_list

    def update(self):
        self.player.update()
        
        # [핵심] 이동 중에 조각과 닿았는지 체크 (자동 수집)
        if not self.cutscene_active:
            # check_collection이 수집한 개수를 반환함
            collected_num = self.map_manager.check_collection(self.player.rect)
            for _ in range(collected_num):
                self.add_to_inventory()

        # 컷신 종료 체크
        if self.cutscene_active:
            if self.player.x > SCREEN_WIDTH:
                self.done = True

    def draw(self):
        self.map_manager.draw_background(self.screen, self.cutscene_active)
        
        if self.cutscene_active:
            self.player.draw(self.screen)
            return

        self.map_manager.draw_ground_pieces(self.screen)
        self.map_manager.draw_launchpad_info(self.screen)
        self.player.draw(self.screen)
        
        # 상단 UI 배경 (좌표 0, 0)
        ui_surf = pygame.Surface((SCREEN_WIDTH, UI_HEIGHT))
        ui_surf.fill(BLACK)
        ui_surf.set_alpha(150)
        self.screen.blit(ui_surf, (0, 0)) 
        
        # 인벤토리 안의 조각들 그리기
        for i, rect in enumerate(self.inventory_pieces):
            self.screen.blit(self.images.broken_piece, rect.topleft)
            # 드래그 중일 때 하이라이트(테두리)는 삭제됨
        
        # 안내 텍스트
        font = pygame.font.Font(None, 30)
        if self.map_manager.assembled_count < TOTAL_PIECES:
            msg = "Move to collect pieces! Drag them to the Launchpad!"
        else:
            msg = "Spaceship Ready! Click to Launch!"
            
        text_surf = font.render(msg, True, WHITE)
        self.screen.blit(text_surf, (SCREEN_WIDTH // 2 - text_surf.get_width() // 2, UI_HEIGHT + 10))

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    stage = Stage2Back(screen)
    stage.run()
    pygame.quit()