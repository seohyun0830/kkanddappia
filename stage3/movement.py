"""
방향키 먹게 하기
미로 범위체크
충돌 처리
단선은 지나갈수있게
"""
from engine import constants
from stage3.broken import is_broken_at


def is_gate_open(r, c, iron_gates):
    for g in iron_gates:
        gr, gc, closed, slide_y = g
        if gr == r and gc == c:
            return not closed  # 닫혀있지 않으면 True
    return True  # 철문 정보 없으면 통과 가능


def try_move_player(maze_data, pos, dr, dc, iron_gates, broken_tiles):
    r, c = pos
    nr, nc = r + dr, c + dc
    size = len(maze_data)

    # 미로 범위 체크
    if not (0 <= nr < size and 0 <= nc < size):
        return pos  # 이동 불가

    tile = maze_data[nr][nc]

    #벽->이동 x
    if tile == constants.WALL:
        return pos

    #단선->이동o
    if tile == constants.BROKEN:
        return (nr, nc)

    #철문->열려있을때만 통과o
    if tile == constants.IRON_GATE:
        if is_gate_open(nr, nc, iron_gates):
            return (nr, nc)
        else:
            return pos

    #일반PATH
    return (nr, nc)
