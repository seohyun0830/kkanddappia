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
        
        # 인벤(상단)
        self.inventory_pieces = [] 
        
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
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.map_manager.assembled_count >= TOTAL_PIECES:
                    if LAUNCHPAD_RECT.collidepoint(mouse_pos):
                        self.cutscene_active = True
                        self.player.start_cutscene() 
                        return
                                    
                # 상단에서 드래그
                for i, rect in enumerate(self.inventory_pieces):
                    if rect.collidepoint(mouse_pos):
                        self.is_dragging = True
                        self.drag_index = i
                        self.drag_offset = (rect.x - mouse_pos[0], rect.y - mouse_pos[1])
                        break
            
            elif event.type == pygame.MOUSEMOTION:
                if self.is_dragging and self.drag_index != -1:
                    current_rect = self.inventory_pieces[self.drag_index]
                    current_rect.x = mouse_pos[0] + self.drag_offset[0]
                    current_rect.y = mouse_pos[1] + self.drag_offset[1]
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.is_dragging:
                    dropped_rect = self.inventory_pieces[self.drag_index]
                    
                    if LAUNCHPAD_RECT.colliderect(dropped_rect):
                        self.inventory_pieces.pop(self.drag_index) 
                        self.map_manager.assembled_count += 1 
                        self.rearrange_inventory() 
                    else:
                        self.rearrange_inventory()
                        
                    self.is_dragging = False
                    self.drag_index = -1

    def add_to_inventory(self):
        count = len(self.inventory_pieces)
        x = 20 + (count * (PIECE_SIZE + 10))
        y = 25 
        new_rect = pygame.Rect(x, y, PIECE_SIZE, PIECE_SIZE)
        self.inventory_pieces.append(new_rect)

    def rearrange_inventory(self):
        new_list = []
        for i in range(len(self.inventory_pieces)):
            x = 20 + (i * (PIECE_SIZE + 10))
            y = 25
            rect = pygame.Rect(x, y, PIECE_SIZE, PIECE_SIZE)
            new_list.append(rect)
        self.inventory_pieces = new_list

    def update(self):
        self.player.update()
        
        if not self.cutscene_active:
            collected_num = self.map_manager.check_collection(self.player.rect)
            for _ in range(collected_num):
                self.add_to_inventory()

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
        
        ui_surf = pygame.Surface((SCREEN_WIDTH, UI_HEIGHT))
        ui_surf.fill(BLACK)
        ui_surf.set_alpha(150)
        self.screen.blit(ui_surf, (0, 0)) 
        
        for i, rect in enumerate(self.inventory_pieces):
            self.screen.blit(self.images.broken_piece, rect.topleft)
        
        # 텍스트(넣을까말까)
        '''
        font = pygame.font.Font(None, 30)
        if self.map_manager.assembled_count < TOTAL_PIECES:
            msg = "Move to collect pieces! Drag them to the Launchpad!"
        else:
            msg = "Spaceship Ready! Click to Launch!"
            
        text_surf = font.render(msg, True, WHITE)
        self.screen.blit(text_surf, (SCREEN_WIDTH // 2 - text_surf.get_width() // 2, UI_HEIGHT + 10))
        '''

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    stage = Stage2Back(screen)
    stage.run()
    pygame.quit()