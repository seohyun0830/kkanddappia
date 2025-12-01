import pygame
import os

# --- 화면 설정 ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# --- 색상 ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)

# --- 경로 설정 ---
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(CURRENT_PATH, 'assets')

# --- 플레이어 설정 ---
PLAYER_SPEED = 5
ANIMATION_SPEED = 8 
JUMP_STRENGTH = 15  # 점프 힘
GRAVITY = 1.0       # 중력
GROUND_Y = 630    # 바닥 Y좌표 기준

# --- 우주선 조각 설정 ---
TOTAL_PIECES = 9
PIECE_SIZE = 50

# --- 발사대(Launchpad) 위치 ---
LAUNCHPAD_RECT = pygame.Rect(900, 400, 250, 300)

# --- 하단 UI (주운 조각이 보이는 곳) ---
UI_HEIGHT = 100
UI_RECT = pygame.Rect(0, SCREEN_HEIGHT - UI_HEIGHT, SCREEN_WIDTH, UI_HEIGHT)

# --- 우주선 효과 (Pulsate) ---
PULSATE_SPEED = 0.005
PULSATE_MIN_SCALE = 0.95
PULSATE_MAX_SCALE = 1.05