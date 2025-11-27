import pygame
import sys
from setting import *
from images import ImageManager
from sounds import SoundManager

from player import Player
from map import MapManager
from dic import Dictionary
from inven import Inventory
from make import Crafting
from sounds import SoundManager

class Stage2:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        self.images = ImageManager()
        self.sounds = SoundManager()

        self.sounds.play_background_music('background_sound.mp3', volume=0.3)
        
        self.done = False
        self.game_over = False

        self.replay_btn_rect = pygame.Rect(SCREEN_WIDTH-250, SCREEN_HEIGHT - 120, 200, 60)
        self.btn_font = pygame.font.Font(None, 50) 

        self.reset_game_data()
        
        self.inventory = (['fire']*1 + ['water']*1 + ['stone']*15 + 
                         ['spaceship'] * 1 + 
                         ['spaceship-side'] * 4 + 
                         ['spaceship-roof'] * 4 + 
                         ['fuel tank'] * 7)
        
        self.crafting_table = [None] * 9
        self.spaceship_assembly_storage = []
        self.assembled_slot_map = {}
        self.dropped_items = []
        
        self.open_door = False
        self.dic_open = False
        self.is_crafting_open = False
        self.is_spaceship_crafting_open = False
        
        self.is_drag = False
        self.drag_item = None
        self.drag_item_original = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        self.map_manager = MapManager(self)
        self.player = Player(self)
        self.dictionary = Dictionary(self)
        self.inven_ui = Inventory(self)
        self.crafting_ui = Crafting(self)

    def reset_game_data(self):
        self.game_over = False
        
        self.inventory = (['fire']*1 + ['water']*1 + ['stone']*15 + 
                         ['spaceship'] * 1 + 
                         ['spaceship-side'] * 4 + 
                         ['spaceship-roof'] * 4 + 
                         ['fuel tank'] * 7)
        
        self.crafting_table = [None] * 9
        self.spaceship_assembly_storage = []
        self.assembled_slot_map = {}
        self.dropped_items = []
        
        self.open_door = False
        self.dic_open = False
        self.is_crafting_open = False
        self.is_spaceship_crafting_open = False
        
        self.is_drag = False
        self.drag_item = None
        self.drag_item_original = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        
        self.map_manager = MapManager(self)
        self.player = Player(self)
        self.dictionary = Dictionary(self)
        self.inven_ui = Inventory(self)
        self.crafting_ui = Crafting(self)
        
    def run(self):
        while not self.done:
            self.handle_events()
            
            self.update()
            
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(FPS)
            
        return "game_over" if self.game_over else "quit"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            
            if self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    #게임 리셋
                    if self.replay_btn_rect.collidepoint(mouse_pos):
                        self.reset_game_data()
                continue

            if self.game_over or self.player.is_flying_animation_active or self.player.is_walking_into_spaceship:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up(event)

    def handle_mouse_down(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if self.crafting_ui.crafted_item_display:
            self.crafting_ui.confirm_crafting_result()
            return
        
        # 아이콘
        if self.inven_ui.handle_icon_click(mouse_pos):
            return
        
        if EASY_MODE and DIC_ICON_AREA.collidepoint(mouse_pos):
            self.dic_open = not self.dic_open
            if self.dic_open:
                # 사전
                self.open_door = False
                self.is_crafting_open = False
                self.is_spaceship_crafting_open = False
                
                if self.is_drag:
                    self.inventory.append(self.drag_item)
                    self.reset_drag()
            return

        # 사전 넘기기
        if self.dic_open:
            if self.dictionary.handle_click(mouse_pos):
                return
            else:
                self.dic_open = False # 사전 닫기

        elif self.open_door or self.is_spaceship_crafting_open:
            is_handled = False
            if self.open_door:
                if self.inven_ui.is_click_inside_ui(mouse_pos) or self.crafting_ui.is_click_inside_ui(mouse_pos):
                    is_handled = True
            elif self.is_spaceship_crafting_open:
                if self.crafting_ui.is_click_inside_spaceship_ui(mouse_pos):
                    is_handled = True
            
            if not is_handled and not (DIC_ICON_AREA.collidepoint(mouse_pos) or BAG_ICON_AREA.collidepoint(mouse_pos)):
                # 창 닫을 때 드래그 중이던거 복구
                if self.is_drag:
                    self.inventory.append(self.drag_item)
                    self.reset_drag()
                self.close_all_popups()

        elif not self.open_door and not self.dic_open and not self.is_spaceship_crafting_open:
            self.map_manager.handle_click(mouse_pos)

        # 드래그
        if self.open_door or self.is_spaceship_crafting_open:
             if self.inven_ui.handle_drag_start(mouse_pos):
                 pass
             elif self.open_door and self.is_crafting_open:
                 self.crafting_ui.handle_drag_start(mouse_pos)

    def handle_mouse_up(self, event):
        mouse_pos = pygame.mouse.get_pos()

        # 나무 베기 중단
        if self.map_manager.is_tree_pressing:
            self.map_manager.is_tree_pressing = False
            self.map_manager.tree_press_start_time = 0

            if self.sounds.tree_sound:
                    self.sounds.tree_sound.stop()

        if self.is_drag:
            self.handle_drop(mouse_pos)

    def handle_drop(self, mouse_pos):
        dropped = False
        
        # 제작창 드랍
        if self.is_crafting_open:
            if self.crafting_ui.handle_drop_in_crafting(mouse_pos):
                dropped = True

        # 외부 제작창 드랍
        if self.is_spaceship_crafting_open and not dropped:
            if self.crafting_ui.handle_drop_in_spaceship_window(mouse_pos):
                dropped = True

        # 우주선 드랍
        if (self.open_door or self.is_spaceship_crafting_open) and not dropped:
            if self.map_manager.current_map == "outside2":
                 if self.crafting_ui.handle_drop_on_spaceship_area(mouse_pos):
                     dropped = True

        # 드랍 실패
        if not dropped:
            self.inventory.append(self.drag_item)
        
        self.reset_drag()

    def reset_drag(self):
        self.is_drag = False
        self.drag_item = None
        self.drag_item_original = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    def close_all_popups(self):
        self.open_door = False
        self.is_crafting_open = False
        self.is_spaceship_crafting_open = False
        self.dic_open = False

    def update(self):
        self.player.update()
        self.map_manager.update()

    def draw(self):

        if self.game_over:
            if self.images.bomb_ending_image:
                self.screen.blit(self.images.bomb_ending_image, (0,0))
            else:
                self.screen.fill(BLACK)

            mouse_pos = pygame.mouse.get_pos()
            is_hover = self.replay_btn_rect.collidepoint(mouse_pos)
            
            pygame.draw.rect(self.screen, (180, 180, 180), self.replay_btn_rect, border_radius=10)
            pygame.draw.rect(self.screen, BLACK, self.replay_btn_rect, width=3, border_radius=10)
            
            text_color = BLACK if is_hover else WHITE
            
            replay_text = self.btn_font.render("REPLAY", True, text_color)
            text_rect = replay_text.get_rect(center=self.replay_btn_rect.center)
            self.screen.blit(replay_text, text_rect)
            
            return

        self.screen.fill(BLACK)
        
        self.map_manager.draw()

        self.player.draw()

        self.map_manager.draw_dropped_items()

        # 우주선 게이지
        if self.map_manager.current_map == "outside2":
             self.map_manager.draw_spaceship_gauge()
        
        if self.open_door:
            # 인벤토리만
            current_x = INVEN_IMAGE_X if self.is_crafting_open else CENTERED_INV_X
            self.inven_ui.draw(current_x)
            
            if self.is_crafting_open:
                self.crafting_ui.draw_normal_crafting()

        elif self.is_spaceship_crafting_open:
             self.crafting_ui.draw_spaceship_crafting()
        
        elif self.dic_open:
            self.dictionary.draw()

        # 아이콘
        if not self.player.is_flying_animation_active and not self.player.is_walking_into_spaceship:
            self.screen.blit(self.images.icon_bag_image, (BAG_ICON_X, BAG_ICON_Y))
            self.screen.blit(self.images.icon_dic_image, (DIC_ICON_X, DIC_ICON_Y))

        # 드래그 중 아이템
        if self.is_drag and self.drag_item:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            item_img = self.images.item_images.get(self.drag_item)
            if item_img:
                self.screen.blit(item_img, (mouse_x - self.drag_offset_x, mouse_y - self.drag_offset_y))

        self.crafting_ui.draw_result_popup()

        if self.game_over:
            font = pygame.font.Font(None, 74)
            small_font = pygame.font.Font(None, 40)
            game_over_text = font.render("GAME OVER", True, RED)
            sub_text = small_font.render("Press ESC to Quit", True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(sub_text, (SCREEN_WIDTH // 2 - sub_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("KKANDDABBIA! - Stage 2 (Modularized)")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    stage = Stage2(screen)
    stage.run()
    
    pygame.quit()
