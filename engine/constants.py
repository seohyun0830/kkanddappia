#화면 설정
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

#미로 관련
GRID_SIZE = 35          # 미로 크기
TILE_SIZE = 20          # 타일 크기 
GRID_OFFSET_X = (SCREEN_WIDTH - GRID_SIZE * TILE_SIZE) // 2
GRID_OFFSET_Y = (SCREEN_HEIGHT - GRID_SIZE * TILE_SIZE) // 2

#타일ID
WALL = 1
PATH = 0
IRON_GATE = 12          # 철문
BROKEN = 13            # 단선 타일

#이동 관련
MOVE_COOLDOWN = 3       # Stage3 기본 이동 딜레이
back_MOVE_COOLDOWN = 3  # Stage4→3(back) 스테이지 이동 딜레이

#폰트
FONT_NAME = '둥근모꼴regular'
BASE_FONT_SIZE = 30
TIMER_FONT_SIZE = 50
PSI_FONT_SIZE = 35      # 압력 psi 텍스트 크기

#도착지점 색깔
COLOR_FINISH_ACTIVE = (0, 255, 0)   # 클리어 조건 달성
COLOR_FINISH_INACTIVE = (255, 0, 0) # 아직 클리어 불가

#타이머
TOTAL_GAME_TIME_SECONDS = 5 * 60  # Stage3 전체 제한시간: 5분

# -------------------------------------------------------------
# 압력 관련 (Stage3)
# -------------------------------------------------------------
# 압력 글씨 깜빡임
PULSATE_MAX_OFFSET = 10
PULSATE_SPEED = 0.005

# 미세 변화 (0.2초마다)
PRESSURE_UPDATE_INTERVAL = 200
MIN_RANDOM_CHANGE = 1
MAX_RANDOM_CHANGE = 3

# 급격 변화 (3~5초)
MIN_SPIKE_INTERVAL = 3000
MAX_SPIKE_INTERVAL = 5000
MIN_SPIKE_CHANGE = 10
MAX_SPIKE_CHANGE = 30

#FPS
FPS = 40

#철문,단선 생성 주기
GATE_TOGGLE_INTERVAL = 120
BROKEN_TOGGLE_INTERVAL = 100
last_broken_stage = 0

#HP관련
MAX_HP = 100
start_HP = 100
HP_BAR_W = 200
HP_BAR_H = 20
HP_BAR_X = SCREEN_WIDTH - HP_BAR_W - 20
HP_BAR_Y = 750   # HP 바 y 좌표
