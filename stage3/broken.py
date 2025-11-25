"""
1. 단선 생성
-랜덤 통로에 단선 생성
-압력 높을 때 발생
-생성 후 maze_data[r][c]=BROKEN
2. 이미 존재하는 단선인지 검사
3. broken 목록 관리 
-[r,c,is_broken]형태

"""
import random
from engine import constants, sound

#단선이 존재하는지 확인
def is_broken_at(r, c, broken_tiles):
    return any(b[0] == r and b[1] == c and b[2] for b in broken_tiles)

#통로 랜덤위치에 단선 생성
def generate_broken_tile(maze_data, broken_tiles):
    candidates = []
    size = len(maze_data)

    # PATH 중에서 이미 단선 아닌 곳만 후보
    for r in range(size):
        for c in range(size):
            if maze_data[r][c] == constants.PATH:
                # 이미 단선인지 체크
                if not is_broken_at(r, c, broken_tiles):
                    candidates.append((r, c))

    if not candidates:
        return None  # 생성할 곳 없음

    # 후보 중 랜덤
    r, c = random.choice(candidates)

    # 생성
    maze_data[r][c] = constants.BROKEN
    broken_tiles.append([r, c, True])

    # 사운드
    sound.broken_sound.play()

    return (r, c)

#단선 수리 후 일반 통로(PATH)로 되돌림
def clear_broken_tile(maze_data, tile):
    r, c = tile[0], tile[1]
    maze_data[r][c] = constants.PATH
    tile[2] = False
