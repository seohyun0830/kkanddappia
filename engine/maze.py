import random
from . import constants  

def initialize_grid(size: int):
    # 전부 벽으로 초기화
    grid = [[constants.WALL] * size for _ in range(size)]

    # (0,0)에서 시작해서 DFS로 통로 뚫기
    generate_maze_dfs(grid, 0, 0, size)

    # 혹시 홀수/짝수 때문에 중간에 남은 벽들이 있더라도
    # DFS로 방문한 곳은 PATH, 나머지는 WALL로 정리
    final_grid = [
        [
            constants.PATH if grid[r][c] != constants.WALL else constants.WALL
            for c in range(size)
        ]
        for r in range(size)
    ]

    # 시작점 / 도착점은 항상 PATH 보장
    final_grid[0][0] = constants.PATH
    final_grid[size - 1][size - 1] = constants.PATH

    return final_grid


def generate_maze_dfs(grid, r, c, size):
    # 깊이우선 탐색 기반 미로 뚫기
    grid[r][c] = constants.PATH

    # 상하좌우 랜덤 순서로 섞기
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(directions)

    for dr, dc in directions:
        nr, nc = r + dr * 2, c + dc * 2  # 2칸 건너 위치
        # 아직 안 뚫린 벽이면 사이를 뚫고 재귀
        if 0 <= nr < size and 0 <= nc < size and grid[nr][nc] == constants.WALL:
            # 중간 벽 한 칸 뚫기
            grid[r + dr][c + dc] = constants.PATH
            generate_maze_dfs(grid, nr, nc, size)


def place_iron_gates(maze_data, num_gates=5):
    size = len(maze_data)
    path_positions = [
        (r, c)
        for r in range(size)
        for c in range(size)
        if maze_data[r][c] == constants.PATH
           and (r, c) not in [(0, 0), (size - 1, size - 1)]
    ]

    gates = []
    for _ in range(num_gates):
        if not path_positions:
            break
        r, c = random.choice(path_positions)
        path_positions.remove((r, c))

        maze_data[r][c] = constants.IRON_GATE
        gates.append([r, c, False])  # [행, 열, 닫힘여부(False면 열림)]

    return gates


def place_broken_tiles(maze_data, num_tiles=5):
    size = len(maze_data)
    path_positions = [
        (r, c)
        for r in range(size)
        for c in range(size)
        if maze_data[r][c] == constants.PATH
           and (r, c) not in [(0, 0), (size - 1, size - 1)]
    ]

    broken_tiles = []
    for _ in range(num_tiles):
        if not path_positions:
            break
        r, c = random.choice(path_positions)
        path_positions.remove((r, c))

        maze_data[r][c] = constants.BROKEN
        broken_tiles.append([r, c, True])  # True = 단선 존재

    return broken_tiles
