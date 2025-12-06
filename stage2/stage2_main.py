import pygame
import sys
from .setting import *
from .images import ImageManager
from .sounds import SoundManager

from .player import Player
from .map import MapManager
from .dic import Dictionary
from .inven import Inventory
from .make import Crafting
from .sounds import SoundManager

from .guide import f_guide1, f_guide2, f_guide3

class Stage2:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        self.images = ImageManager()
        self.sounds = SoundManager()
        
        self.is_easy_mode = True
        self.done = False
        self.game_over = False
        self.go_to_stage1 = False
        self.stage_clear = False
        
        self.game_reset=False
        
        # 가이드 넘김용 스페이스바 상태 변수
        self.guide_space_pressed = False

        # 모은 쪽지 개수 (사전 해금용)
        self.collected_notes_count = 0

        #폭발 애니메이션
        self.bomb_animation_index = 0
        self.bomb_animation_timer = 0
        
        # 리플레이 버튼
        btn_width = 200
        btn_height = 60
        margin_right = 30
        margin_bottom = 30
        
        self.replay_btn_rect = pygame.Rect(
            SCREEN_WIDTH - btn_width - margin_right, 
            SCREEN_HEIGHT - btn_height - margin_bottom, 
            btn_width, 
            btn_height
        )
        
        try:
            self.btn_font = pygame.font.Font('DungGeunMO.ttf', 50)
        except:
            self.btn_font = pygame.font.Font(None, 50)

        self.reset_game_data()

    def reset_game_data(self, imported_items=None):
        """게임을 처음 상태로 되돌림 (REPLAY용)"""
        self.game_over = False
        self.go_to_stage1 = False

        self.collected_notes_count = 0 # 쪽지 초기화

        self.bomb_animation_index = 0
        self.bomb_animation_timer = 0
        
        if self.sounds.bomb_sound: self.sounds.bomb_sound.stop()
        if self.sounds.tree_sound: self.sounds.tree_sound.stop()
        if self.sounds.walk_sound: self.sounds.walk_sound.stop()
        
        # 기본 아이템 (불, 물 + 테스트용 부품들)
        base_items = ['fire', 'water'] + \
                     ['spaceship-side'] * 4 + \
                     ['spaceship-roof'] * 4 + \
                     ['fuel tank'] * 15 + \
                     ['steel'] * 2 + \
                     ['axe'] + \
                     ['ladder']*10

        if imported_items is not None:
            self.inventory = base_items + imported_items
        else:
            self.inventory = base_items

        self.collected_notes_count=self.inventory.count('paper')
        
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

    def update_resources(self, imported_items):
        """Stage 1에서 돌아올 때 자원만 갱신"""
        self.go_to_stage1 = False 
        self.game_over = False
        
        if self.sounds.bomb_sound: self.sounds.bomb_sound.stop()
        if self.sounds.tree_sound: self.sounds.tree_sound.stop()
        if self.sounds.walk_sound: self.sounds.walk_sound.stop()
        
        stage1_resource_names = ['stone', 'soil', 'fossil', 'ladder']
        
        new_inventory = []
        for item in self.inventory:
            if item not in stage1_resource_names:
                new_inventory.append(item)

        if imported_items:
            new_inventory.extend(imported_items)
             
        self.inventory = new_inventory

        self.collected_notes_count = self.inventory.count('paper')
        
        self.player.x = PLAYER_START_X
        self.player.y = PLAYER_START_Y
        self.player.alpha = 255
        self.player.is_fading_out = False
        self.player.is_walking_into_spaceship = False
        self.player.is_flying_animation_active = False
        
        self.map_manager.current_map = "outside1"
        self.map_manager.is_tree_pressing = False
        
        self.open_door = False
        self.dic_open = False
        self.is_crafting_open = False
        self.is_spaceship_crafting_open = False
        self.crafting_ui.crafted_item_display = None

    def run(self, timer=None):
        """메인 게임 루프 실행"""
        self.done = False
        self.go_to_stage1 = False
        self.game_over = False
        self.game_reset=False
        
        # 플레이어 위치 복구
        self.player.x = PLAYER_START_X
        self.player.y = PLAYER_START_Y
        self.player.alpha = 255
        self.player.is_fading_out = False
        self.player.is_walking_into_spaceship = False
        self.player.is_flying_animation_active = False
        
        self.map_manager.current_map = "outside1"
        self.map_manager.is_tree_pressing = False
        
        self.open_door = False
        self.dic_open = False
        self.is_crafting_open = False
        self.is_spaceship_crafting_open = False
        self.crafting_ui.crafted_item_display = None
        
        self.sounds.play_background_music('background_sound.mp3', volume=0.3)

        while not self.done:
            # Stage 1 이동 신호
            if self.go_to_stage1:
                #self.sounds.stop_background_music()
                return "stage1"
            
            if self.game_reset:
                self.sounds.stop_background_music()
                return "reset"
        

            # 타이머 종료 체크
            if timer and timer.get_remianing_time() <= 0: # 오타 수정: remianing -> remaining
                self.sounds.stop_background_music()
                return "timeOUT"

            self.handle_events()
            self.update()
            if self.stage_clear:
                self.sounds.stop_background_music()
                            
                            # 연료통 개수 세기
                fuel_count = self.inventory.count('fuel-tank')
                            
                            # 튜플 형태로 (다음 스테이지, 연료 개수) 반환
                return ("stage3", fuel_count)
            self.draw(timer)
            
            # 가이드용 키 입력 플래그 리셋
            self.guide_space_pressed = False
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        self.sounds.stop_background_music()
        return "game_over" if self.game_over else "quit"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            
            if self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.replay_btn_rect.collidepoint(mouse_pos):
                        self.game_reset=True
                continue 

            # 가이드 스킵 키
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.guide_space_pressed = True

            if self.player.is_flying_animation_active or self.player.is_walking_into_spaceship:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up(event)

    def handle_mouse_down(self, event):
        mouse_pos = pygame.mouse.get_pos()
        
        # 0. 팝업 닫기
        if self.crafting_ui.crafted_item_display:
            self.crafting_ui.confirm_crafting_result()
            return
        
        # 1. 아이콘 클릭
        if self.inven_ui.handle_icon_click(mouse_pos):
            return

        # 2. 사전 아이콘
        if DIC_ICON_AREA.collidepoint(mouse_pos):
            self.dic_open = not self.dic_open
            if self.dic_open:
                self.open_door = False
                self.is_crafting_open = False
                self.is_spaceship_crafting_open = False
                if self.is_drag:
                    self.inventory.append(self.drag_item)
                    self.reset_drag()
            return

        # 3. 사전 페이지 넘김
        if self.dic_open:
            if self.dictionary.handle_click(mouse_pos):
                return
            else:
                self.dic_open = False 

        # 4. UI 창 닫기
        elif self.open_door or self.is_spaceship_crafting_open:
            is_handled = False
            if self.open_door:
                if self.inven_ui.is_click_inside_ui(mouse_pos) or self.crafting_ui.is_click_inside_ui(mouse_pos):
                    is_handled = True
            elif self.is_spaceship_crafting_open:
                if self.crafting_ui.is_click_inside_spaceship_ui(mouse_pos):
                    is_handled = True
            
            is_on_dic_icon = DIC_ICON_AREA.collidepoint(mouse_pos)
            
            if not is_handled and not (is_on_dic_icon or BAG_ICON_AREA.collidepoint(mouse_pos)):
                if self.is_drag:
                    if self.drag_item not in ['fire', 'water', 'axe', 'hammer']:
                        self.inventory.append(self.drag_item)
                    self.reset_drag()
                self.close_all_popups()

        # 5. 맵 상호작용
        elif not self.open_door and not self.dic_open and not self.is_spaceship_crafting_open:
            self.map_manager.handle_click(mouse_pos)

        # 6. 드래그 시작
        if self.open_door or self.is_spaceship_crafting_open:
             if self.inven_ui.handle_drag_start(mouse_pos):
                 pass
             elif self.open_door and self.is_crafting_open:
                 self.crafting_ui.handle_drag_start(mouse_pos)

    def handle_mouse_up(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.map_manager.is_tree_pressing:
            self.map_manager.is_tree_pressing = False  
            self.map_manager.tree_press_start_time = 0
            if self.sounds.tree_sound:
                self.sounds.tree_sound.stop()
        if self.is_drag:
            self.handle_drop(mouse_pos)

    def handle_drop(self, mouse_pos):
        dropped = False
        if self.is_crafting_open:
            if self.crafting_ui.handle_drop_in_crafting(mouse_pos):
                dropped = True
        if self.is_spaceship_crafting_open and not dropped:
            if self.crafting_ui.handle_drop_in_spaceship_window(mouse_pos):
                dropped = True
        if (self.open_door or self.is_spaceship_crafting_open) and not dropped:
            if self.map_manager.current_map == "outside2":
                 if self.crafting_ui.handle_drop_on_spaceship_area(mouse_pos):
                     dropped = True
        if not dropped:
            if self.drag_item not in ['fire', 'water']:
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
        if self.game_over:
            return 
        self.player.update()
        self.map_manager.update()
        
        self.map_manager.check_item_pickup(self.player.rect)

    def draw(self, timer=None):
        # 1. 게임 오버 화면
        if self.game_over:
            self.bomb_animation_timer += 1
            
            if self.bomb_animation_index < len(self.images.bomb_frames) - 1:
                self.bomb_animation_timer += 1
                if self.bomb_animation_timer >= 20: # 속도 (클수록 느림)
                    self.bomb_animation_index += 1
                    self.bomb_animation_timer = 0
            
            # 현재 프레임 그리기
            if self.images.bomb_frames:
                current_frame = self.images.bomb_frames[self.bomb_animation_index]
                self.screen.blit(current_frame, (0, 0))
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

        # --- 일반 게임 화면 ---
        self.screen.fill(BLACK)
        self.map_manager.draw(timer) # 맵 매니저가 타이머도 그림
        self.player.draw()
        self.map_manager.draw_dropped_items()

        # 우주선 게이지
        if self.map_manager.current_map == "outside2" and \
           not self.player.is_walking_into_spaceship and \
           not self.player.is_flying_animation_active:
             self.map_manager.draw_spaceship_gauge()
        
        # UI
        if self.open_door:
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

        # 드래그 중인 아이템
        if self.is_drag and self.drag_item:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            item_img = self.images.item_images.get(self.drag_item)
            if item_img:
                self.screen.blit(item_img, (mouse_x - self.drag_offset_x, mouse_y - self.drag_offset_y))

        self.crafting_ui.draw_result_popup()

        # 가이드 그리기
        if self.map_manager.current_map == "outside1":
            f_guide1(self.screen, self.guide_space_pressed, self.is_drag)
        elif self.map_manager.current_map == "inside":
            f_guide2(self.screen, self.guide_space_pressed, self.is_drag)
        elif self.map_manager.current_map == "outside2":
            f_guide3(self.screen, self.guide_space_pressed, self.is_drag)

# --- 테스트 실행용 코드 ---
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("KKANDDABBIA! - Stage 2")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    stage = Stage2(screen)
    # 테스트 시에는 타이머 없이 실행
    stage.run(None)
    pygame.quit()

'''

class Stage2:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        self.images = ImageManager()
        self.sounds = SoundManager()
        
        self.is_easy_mode = True
        self.done = False
        
        btn_width = 200
        btn_height = 60
        margin_right = 30
        margin_bottom = 30
        
        self.replay_btn_rect = pygame.Rect(
            SCREEN_WIDTH - btn_width - margin_right, 
            SCREEN_HEIGHT - btn_height - margin_bottom, 
            btn_width, 
            btn_height
        )
        self.btn_font = pygame.font.Font(None, 50) 

        self.reset_game_data()

    def reset_game_data(self, imported_items=None):

        self.game_over = False
        
        if self.sounds.bomb_sound: self.sounds.bomb_sound.stop()
        if self.sounds.tree_sound: self.sounds.tree_sound.stop()
        if self.sounds.walk_sound: self.sounds.walk_sound.stop()

        base_items = (['fire']*1 + ['water']*1 +
                         ['spaceship-side'] * 4 + 
                         ['spaceship-roof'] * 4 + 
                         ['fuel tank'] * 7)
        
        if imported_items is not None:
            self.inventory=base_items+imported_items
        else:
            self.inventory=base_items
        
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
        
        # 상태 복구
        self.done = False
        self.go_to_stage1 = False
        self.game_over = False
        
        # 플레이어 위치 및 투명도 원상복구
        self.player.x = PLAYER_START_X
        self.player.y = PLAYER_START_Y
        self.player.alpha = 255
        self.player.is_fading_out = False
        self.player.is_walking_into_spaceship = False
        self.player.is_flying_animation_active = False
        
        # 맵 상태 복구 (첫 맵으로)
        self.map_manager.current_map = "outside1"
        self.map_manager.is_tree_pressing = False
        
        # 열려있는 창 닫기
        self.open_door = False
        self.dic_open = False
        self.is_crafting_open = False
        self.is_spaceship_crafting_open = False
        self.crafting_ui.crafted_item_display = None
        
        self.sounds.play_background_music('background_sound.mp3', volume=0.3)

        while not self.done:
            if self.go_to_stage1:
                self.sounds.stop_background_music()
                return "stage1"

            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        
        self.sounds.stop_background_music()
        return "game_over" if self.game_over else "quit"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            
            if self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.replay_btn_rect.collidepoint(mouse_pos):
                        self.reset_game_data()
                continue 

            if self.player.is_flying_animation_active or self.player.is_walking_into_spaceship:
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
        
        if self.inven_ui.handle_icon_click(mouse_pos):
            return

        if self.is_easy_mode and DIC_ICON_AREA.collidepoint(mouse_pos):
            self.dic_open = not self.dic_open
            if self.dic_open:
                self.open_door = False
                self.is_crafting_open = False
                self.is_spaceship_crafting_open = False
                if self.is_drag:
                    self.inventory.append(self.drag_item)
                    self.reset_drag()
            return

        if self.dic_open:
            if self.dictionary.handle_click(mouse_pos):
                return
            else:
                self.dic_open = False 

        elif self.open_door or self.is_spaceship_crafting_open:
            is_handled = False
            if self.open_door:
                if self.inven_ui.is_click_inside_ui(mouse_pos) or self.crafting_ui.is_click_inside_ui(mouse_pos):
                    is_handled = True
            elif self.is_spaceship_crafting_open:
                if self.crafting_ui.is_click_inside_spaceship_ui(mouse_pos):
                    is_handled = True
            
            is_on_dic_icon = self.is_easy_mode and DIC_ICON_AREA.collidepoint(mouse_pos)
            
            if not is_handled and not (is_on_dic_icon or BAG_ICON_AREA.collidepoint(mouse_pos)):
                if self.is_drag:
                    self.inventory.append(self.drag_item)
                    self.reset_drag()
                self.close_all_popups()

        elif not self.open_door and not self.dic_open and not self.is_spaceship_crafting_open:
            self.map_manager.handle_click(mouse_pos)

        if self.open_door or self.is_spaceship_crafting_open:
             if self.inven_ui.handle_drag_start(mouse_pos):
                 pass
             elif self.open_door and self.is_crafting_open:
                 self.crafting_ui.handle_drag_start(mouse_pos)

    def handle_mouse_up(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.map_manager.is_tree_pressing:
            self.map_manager.is_tree_pressing = False  
            self.map_manager.tree_press_start_time = 0
            if self.sounds.tree_sound:
                self.sounds.tree_sound.stop()
        if self.is_drag:
            self.handle_drop(mouse_pos)

    def handle_drop(self, mouse_pos):
        dropped = False
        if self.is_crafting_open:
            if self.crafting_ui.handle_drop_in_crafting(mouse_pos):
                dropped = True
        if self.is_spaceship_crafting_open and not dropped:
            if self.crafting_ui.handle_drop_in_spaceship_window(mouse_pos):
                dropped = True
        if (self.open_door or self.is_spaceship_crafting_open) and not dropped:
            if self.map_manager.current_map == "outside2":
                 if self.crafting_ui.handle_drop_on_spaceship_area(mouse_pos):
                     dropped = True
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
        if self.game_over:
            return 
        self.player.update()
        self.map_manager.update()

    def draw(self):
        if self.game_over:
            if self.images.bomb_ending_image:
                self.screen.blit(self.images.bomb_ending_image, (0, 0))
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

            small_font = pygame.font.Font(None, 30)
            sub_text = small_font.render("Press ESC to Quit", True, WHITE)
            sub_text_rect = sub_text.get_rect(center=(self.replay_btn_rect.centerx, self.replay_btn_rect.top - 30))
            self.screen.blit(sub_text, sub_text_rect)
            return 

        self.screen.fill(BLACK)
        self.map_manager.draw()
        self.player.draw()
        self.map_manager.draw_dropped_items()

        if self.map_manager.current_map == "outside2" and \
           not self.player.is_walking_into_spaceship and \
           not self.player.is_flying_animation_active:
             self.map_manager.draw_spaceship_gauge()
        
        if self.open_door:
            current_x = INVEN_IMAGE_X if self.is_crafting_open else CENTERED_INV_X
            self.inven_ui.draw(current_x)
            if self.is_crafting_open:
                self.crafting_ui.draw_normal_crafting()
        elif self.is_spaceship_crafting_open:
             self.crafting_ui.draw_spaceship_crafting()
        elif self.dic_open:
            self.dictionary.draw()

        if not self.player.is_flying_animation_active and not self.player.is_walking_into_spaceship:
            self.screen.blit(self.images.icon_bag_image, (BAG_ICON_X, BAG_ICON_Y))
            if self.is_easy_mode:
                self.screen.blit(self.images.icon_dic_image, (DIC_ICON_X, DIC_ICON_Y))

        if self.is_drag and self.drag_item:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            item_img = self.images.item_images.get(self.drag_item)
            if item_img:
                self.screen.blit(item_img, (mouse_x - self.drag_offset_x, mouse_y - self.drag_offset_y))

        self.crafting_ui.draw_result_popup()

# --- 테스트 실행용 코드 (단독 실행 시) ---
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("KKANDDABBIA! - Stage 2 (Modularized)")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    stage = Stage2(screen)
    stage.run()
    
    pygame.quit()

'''

'''
#제발되거라제발

class Stage2:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        self.images = ImageManager()
        self.sounds = SoundManager()

        self.sounds.play_background_music('background_sound.mp3', volume=0.3)
        
        self.done = False
        self.game_over = False
        self.go_to_stage1=False

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
        self.go_to_stage1
        
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

            if self.go_to_stage1:
                self.sounds.stop_background_music()
                return "stage1"

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
'''