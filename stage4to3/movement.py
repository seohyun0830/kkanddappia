def try_move_player(maze, pos, dr, dc, iron_gates, broken_tiles):
    r, c = pos
    nr, nc = r + dr, c + dc
    size = len(maze)

    # 미로 범위 밖 x
    if nr < 0 or nr >= size or nc < 0 or nc >= size:
        return r, c

    # 벽 못감
    if maze[nr][nc] == 1:
        return r, c

    return nr, nc
