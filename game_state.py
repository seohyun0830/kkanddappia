#game_state.py
from constants import *

def iron_gate_is_open(r, c, iron_gates):
    return any(g[0]==r and g[1]==c and g[2] for g in iron_gates)

def broken_exists(r, c, broken_tiles):
    return any(b[0]==r and b[1]==c and b[2] for b in broken_tiles)

def try_move_player(maze_data, player_pos, dr, dc, iron_gates, broken_tiles):
    r, c = player_pos
    nr, nc = r + dr, c + dc
    if not (0 <= nr < len(maze_data) and 0 <= nc < len(maze_data)): return player_pos
    tile = maze_data[nr][nc]
    if tile == PATH or (tile == IRON_GATE and iron_gate_is_open(nr, nc, iron_gates)) or tile == BROKEN:
        return (nr, nc)
    return player_pos
