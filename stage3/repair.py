# stage3/repair.py
import pygame
from engine import constants, sound
from stage3.broken import is_broken_at, clear_broken_tile


class RepairSystem:
    REPAIR_TIME = 2000   # 2초

    def __init__(self):
        self.repairing = False
        self.repair_start_time = 0
        self.target_tile = None  # [r, c, True]

    def start(self, player_row, player_col, broken_tiles):
        for tile in broken_tiles:
            r, c, is_broken = tile
            if r == player_row and c == player_col and is_broken:
                self.repairing = True
                self.repair_start_time = pygame.time.get_ticks()
                self.target_tile = tile
                return True

        return False

    def update(self, maze_data):
        if not self.repairing or self.target_tile is None:
            return False  # 수리 없음

        now = pygame.time.get_ticks()
        elapsed = now - self.repair_start_time

        # 수리 완료
        if elapsed >= self.REPAIR_TIME:
            clear_broken_tile(maze_data, self.target_tile)
            sound.repair_bgm.play()
            self.repairing = False
            self.target_tile = None
            return True

        return False  # 아직 수리중

    def draw_progress(self, screen, player_row, player_col):
        if not self.repairing or self.target_tile is None:
            return

        now = pygame.time.get_ticks()
        elapsed = now - self.repair_start_time
        progress = max(0, min(1, elapsed / self.REPAIR_TIME))

        bar_width = 40
        bar_height = 6

        # 플레이어 타일 위치 계산
        px = (constants.GRID_OFFSET_X +
              player_col * constants.TILE_SIZE +
              constants.TILE_SIZE // 2)

        py = (constants.GRID_OFFSET_Y +
              player_row * constants.TILE_SIZE - 10)

        # 배경
        pygame.draw.rect(screen, (50, 50, 50),
                         (px - bar_width // 2, py, bar_width, bar_height))

        # 진행도 (초록색)
        pygame.draw.rect(screen, (0, 255, 0),
                         (px - bar_width // 2, py, int(bar_width * progress), bar_height))

    def cancel(self):
        self.repairing = False
        self.target_tile = None
