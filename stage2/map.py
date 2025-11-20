import pygame
from setting import *
import images

class MapManager:
    def __init__(self):
        self.current_map = "outside1"
        self.dropped_items = []
        
        self.bg_keys = {
            "outside1": "outside1",
            "inside": "inside",
            "outside2": "outside2"
        }

    def draw_background(self, screen):
        bg_key = self.bg_keys.get(self.current_map, "outside1")
        bg_image = images.backgrounds.get(bg_key)
        if bg_image:
            screen.blit(bg_image, (0, 0))

    def draw_items(self, screen):
        if self.current_map == "outside1":
            for item in self.dropped_items:
                item_draw = images.item_images.get(item['item_name'])
                if item_draw:
                    screen.blit(item_draw, item['rect'])

    def check_map_transition(self, player):
        """플레이어 위치에 따른 맵 이동 처리"""
        player_width = PLAYER_SIZE[0]

        # 1. Outside1 (맨 왼쪽 맵)
        if self.current_map == "outside1":
            # 왼쪽: 갈 곳 없음 -> 벽 (0으로 막음)
            if player.x < 0:
                player.x = 0
            # 오른쪽: Outside2로 이동
            elif player.x > SCREEN_WIDTH - player_width:
                self.current_map = "outside2"
                player.x = 5 

        # 2. Inside (건물 안)
        elif self.current_map == "inside":
            # 왼쪽: Outside1로 나감 (여기가 안 되던 부분!)
            if player.x < 0:
                self.current_map = "outside1"
                player.x = SCREEN_WIDTH - player_width - 10 # Outside1의 오른쪽 끝에서 등장
            # 오른쪽: 갈 곳 없음 -> 벽
            elif player.x > SCREEN_WIDTH - player_width:
                player.x = SCREEN_WIDTH - player_width

        # 3. Outside2 (오른쪽 맵)
        elif self.current_map == "outside2":
            # 왼쪽: Outside1로 돌아감 (여기가 안 되던 부분!)
            if player.x < 0:
                self.current_map = "outside1"
                player.x = SCREEN_WIDTH - player_width - 10
            # 오른쪽: 갈 곳 없음 -> 벽
            elif player.x > SCREEN_WIDTH - player_width:
                player.x = SCREEN_WIDTH - player_width

    def add_dropped_item(self, name, x, y):
        self.dropped_items.append({
            'item_name': name,
            'rect': pygame.Rect(x, y, ITEM_SIZE, ITEM_SIZE)
        })

    def check_item_pickup(self, player, inventory_list):
        if self.current_map != "outside1":
            return

        player_rect = pygame.Rect(player.x, player.y, PLAYER_SIZE[0], PLAYER_SIZE[1])
        
        for i in range(len(self.dropped_items) - 1, -1, -1):
            item = self.dropped_items[i]
            if player_rect.colliderect(item['rect']):
                inventory_list.append(item['item_name'])
                self.dropped_items.pop(i)