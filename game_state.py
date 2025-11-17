import pygame
import constants

#철문
def iron_gate_is_open(r, c, iron_gates):
    for g in iron_gates:
        if g[0]==r and g[1]==c:
            return not g[2] #닫혀있지 않으면 지나갈수있음
    return True #닫힘

#단선생길때
def broken_exists(r, c, broken_tiles):
    return any(b[0]==r and b[1]==c and b[2] for b in broken_tiles)

#플레이어 움직임
def try_move_player(maze_data, player_pos, dr, dc, iron_gates, broken_tile):

    r, c = player_pos
    nr, nc = r + dr, c + dc
    if not (0 <= nr < len(maze_data) and 0 <= nc < len(maze_data)): return player_pos
    tile = maze_data[nr][nc]

    if tile == constants.PATH or tile == constants.BROKEN:
        return (nr, nc)
    if tile == constants.IRON_GATE:
        if iron_gate_is_open(nr, nc, iron_gates):
            return (nr, nc)
        else:
            return player_pos 
    
    return player_pos

#타임오버
def show_end_timeover(SCREEN):
    img=pygame.image.load("images/timeover.png")
    scale = min(constants.SCREEN_WIDTH / img.get_width(), constants.SCREEN_HEIGHT / img.get_height())
    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    pos=img.get_rect(center=(constants.SCREEN_WIDTH//2,constants.SCREEN_HEIGHT//2))

    running=True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False

        SCREEN.fill((0,0,0))
        SCREEN.blit(img,pos)
        pygame.display.update()

#성공
def show_end_screen(SCREEN):
    img1 = pygame.image.load("images/ending_image1.png")
    img2 = pygame.image.load("images/ending_image2.jpg")
    scale = min(constants.SCREEN_WIDTH / img1.get_width(), constants.SCREEN_HEIGHT / img1.get_height())
    s1 = pygame.transform.scale(img1, (int(img1.get_width() * scale), int(img1.get_height() * scale)))
    s2 = pygame.transform.scale(img2, (int(img2.get_width() * scale), int(img2.get_height() * scale)))
    pos = ((constants.SCREEN_WIDTH - s1.get_width()) // 2, (constants.SCREEN_HEIGHT - s1.get_height()) // 2)
    clickable = s1.get_rect(topleft=pos)
    current = s1
    swapped = False
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN and clickable.collidepoint(e.pos) and not swapped:
                current = s2
                swapped = True
            SCREEN.fill((0, 0, 0))
            SCREEN.blit(current, pos)
            pygame.display.update()


