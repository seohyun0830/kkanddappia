#maze.py
import random
from constants import WALL, PATH, IRON_GATE, BROKEN

def initialize_grid(size):
    grid = [[WALL] * size for _ in range(size)]
    generate_maze_dfs(grid, 0, 0, size)
    final_grid = [[PATH if grid[r][c] != WALL else WALL for c in range(size)] for r in range(size)]
    final_grid[0][0] = PATH
    final_grid[size - 1][size - 1] = PATH
    return final_grid

def generate_maze_dfs(grid, r, c, size):
    grid[r][c] = PATH
    directions = [(0,1),(0,-1),(1,0),(-1,0)]
    random.shuffle(directions)
    for dr, dc in directions:
        nr, nc = r + dr * 2, c + dc * 2
        if 0 <= nr < size and 0 <= nc < size and grid[nr][nc] == WALL:
            grid[r + dr][c + dc] = PATH
            generate_maze_dfs(grid, nr, nc, size)

def place_iron_gates(maze_data, num_gates=5):
    grid_size = len(maze_data)
    path_positions = [(r, c) for r in range(grid_size) for c in range(grid_size)
                      if maze_data[r][c] == PATH and (r, c) not in [(0, 0), (grid_size - 1, grid_size - 1)]]
    gates = []
    for _ in range(num_gates):
        if not path_positions: break
        r, c = random.choice(path_positions)
        path_positions.remove((r, c))
        maze_data[r][c] = IRON_GATE
        gates.append([r, c, False])  # False=닫힘
    return gates

def place_broken_tiles(maze_data, num_tiles=5):
    grid_size = len(maze_data)
    path_positions = [(r, c) for r in range(grid_size) for c in range(grid_size)
                      if maze_data[r][c] == PATH and (r, c) not in [(0, 0), (grid_size - 1, grid_size - 1)]]
    broken_tiles = []
    for _ in range(num_tiles):
        if not path_positions: break
        r, c = random.choice(path_positions)
        path_positions.remove((r, c))
        maze_data[r][c] = BROKEN
        broken_tiles.append([r, c, True])  # True=단선 존재
    return broken_tiles
