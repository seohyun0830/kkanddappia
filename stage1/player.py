from . import images
from . import sounds

class Cplayer:
    def __init__(self, col, row, pix):
        self.row = row
        self.col = col

        self.pix = pix
        self.blockX = (col - 3)
        self.blockY = 0

        self.realX = self.blockX * pix
        self.realY = self.blockY * pix
        self.toX = 0
        self.toY = 0

        self.direction = 0      # 캐릭터 방향 -> 왼: 0, 오: 1, 아: 2
            
        self.motion = 0
        self.motionTime = 0

        self.blockMotion = 0
        self.blockTime = 0

        self.pickMotion = 1

        self.velocityY = 0
        self.gravity = 1
        self.jumpPower = -11
        self.isOnGround = True
    
    def f_setDefault(self):
        self.pickMotion = 1
        self.blockMotion = 0
        self.blockTime = 0
        self.motion = 0
        self.motionTime = 0
        if self.direction == 2: self.direction = 0
        elif self.direction == 3: self.direction = 1

    def f_isRblocked(self, under_map, itemMap):
        if (under_map[self.blockY][self.blockX + 1] == 0 and (self.blockX * self.pix - self.realX) < 1):
            return 1
        if (itemMap[self.blockY][self.blockX + 1] == 6 and (self.blockX * self.pix - self.realX) < 1):
            return 1
        return 0

    def f_isLblocked(self, under_map, itemMap):
        if (under_map[self.blockY][self.blockX - 1] == 0 and (self.realX - self.blockX * self.pix) < 1):
            return 1
        if (itemMap[self.blockY][self.blockX - 1] == 6 and (self.realX - self.blockX * self.pix) < 1):
            return 1
        return 0

    def f_motion(self):         # 움직임
        if self.motionTime > 8:                  
            if self.motion == 1 or self.motion == 3 or self.motion == 0:
                self.motion = 2
            elif self.motion == 2:
                self.motion = 1
            self.motionTime = 0
            sounds.sfx_step.play()

    def f_left(self, under_map, itemMap):
        self.direction = 0
        self.motionTime += 1
        self.f_motion()
        if (self.realX <= 0):
            return
        if (self.f_isLblocked(under_map,itemMap)): # 갈 수 없으면
            self.motion = 3
            self.motionTime = 0
            self.f_breaking(under_map)
            self.toX = 0
        else:   # 갈 수 있으면
            self.blockTime = 0
            self.blockMotion = 0
            self.toX = 3
        self.realX -= self.toX

    def f_right(self, under_map, itemMap):
        self.direction = 1
        self.motionTime += 1
        self.f_motion()
        if (self.realX >= 1200 - self.pix):
            return
        if (self.f_isRblocked(under_map, itemMap)): # 갈 수 없으면
            self.motion = 3
            self.motionTime = 0
            self.f_breaking(under_map)
            self.toX = 0
        else:   # 갈 수 있으면
            self.blockTime = 0
            self.blockMotion = 0
            self.toX = 3
        self.realX += self.toX

    def f_down(self, underMap):        
        if self.direction == 0: self.direction = 2
        elif self.direction == 1: self.direction = 3
        elif self.direction == 4: self.direction = 0
        self.f_breaking(underMap)
        self.isOnGround = False

    def f_jump(self):
        if self.isOnGround:
            sounds.sfx_jump.play()
            self.velocityY = self.jumpPower
            self.isOnGround = False

    def f_gravity(self, under_map, itemMap):
        # 1. 사다리 체크
        if (itemMap[self.blockY][self.blockX] == 5) and self.direction == 4:
            self.isOnGround = True
            self.velocityY = 0
            return 
        
        # 2. 중력 적용
        self.velocityY += self.gravity
        if self.velocityY > 10: self.velocityY = 10
        
        # 3. Y 값 갱신 (물리 적용)
        self.realY += self.velocityY
        
        # 4. ★★★ Y 블록 좌표 "즉시" 갱신 (가장 중요) ★★★
        self.blockY = int(self.realY // self.pix) 

        # --- (플레이어 너비가 self.pix라고 가정) ---
        # "왼쪽"과 "오른쪽" X 블록 좌표 계산
        left_x_block = int((self.realX + 10) // self.pix)
        # (self.pix - 1) -> 0~59픽셀 너비일 때, 59번째 픽셀을 의미
        right_x_block = int((self.realX - 10 + self.pix - 1) // self.pix)

        # 5. ★★★★★ 천장 충돌 검사 (2점 확인) ★★★★★
        if self.velocityY < 0: # 상승 중일 때
            # "머리 위 왼쪽" 또는 "머리 위 오른쪽"이 땅(0)인지 확인
            is_ceil_left = (under_map[self.blockY][left_x_block] == 0 or itemMap[self.blockY][left_x_block] == 6)
            is_ceil_right = (under_map[self.blockY][right_x_block] == 0 or itemMap[self.blockY][right_x_block] == 6)
            
            if is_ceil_left or is_ceil_right:
                self.velocityY = 0 # 상승 중단
                self.realY = (self.blockY * self.pix) + self.pix # 위치 보정
                self.blockY = int(self.realY // self.pix) # Y 블록 좌표 "재"갱신

        # 6. ★★★★★ 바닥 충돌 검사 (2점 확인) ★★★★★
        check_y = self.blockY + 1 # "발"이 닿을 블록 Y
        
        if check_y >= self.row: # 맵 바닥에 닿음
            self.isOnGround = True
            self.velocityY = 0
            self.realY = (self.row - 1) * self.pix 
        
        else:
            # "발 아래 왼쪽" 또는 "발 아래 오른쪽"이 땅(0)인지 확인
            is_ground_left = (under_map[check_y][left_x_block] == 0 or itemMap[check_y][left_x_block] == 6)
            is_ground_right = (under_map[check_y][right_x_block] == 0 or itemMap[check_y][right_x_block] == 6)
            
            # "왼발"이나 "오른발" 중 하나라도 땅(0)에 닿아있다면
            if is_ground_left or is_ground_right:
                self.isOnGround = True # 땅에 닿았음
                self.velocityY = 0
                self.realY = self.blockY * self.pix # 위치 보정
            else:
                self.isOnGround = False # (두 발 모두 공중에 있음)

    def f_up(self, itemMap):
        if (itemMap[self.blockY + 1][self.blockX] == 5) or (itemMap[self.blockY][self.blockX] == 5):
            self.direction = 4
            self.motionTime += 1
            self.f_motion()
            self.realY -= 5 # (20은 너무 빠르니 5 정도로 조절)

    def f_breaking(self,under_map):
        self.blockTime += 1
        if self.blockTime > 30:
            #if self.blockMotion == 3: 
            #    sounds.sfx_break.play()
            self.blockMotion = 0
            self.pickMotion = 1
            self.blockTime = 0
            if (self.direction == 0):
                under_map[self.blockY][self.blockX - 1] = 1
            elif (self.direction == 1):
                under_map[self.blockY][self.blockX + 1] = 1
            elif (self.direction == 2 or self.direction == 3):
                under_map[self.blockY + 1][self.blockX] = 1
        elif self.blockTime > 20:
            if (self.blockMotion == 2):
                sounds.sfx_break.play() 
            self.blockMotion = 3
            self.pickMotion = 0
        elif self.blockTime > 10:
            if (self.blockMotion == 1):
                sounds.sfx_break.play()
            self.blockMotion = 2
            self.pickMotion = 1
        elif self.blockTime > 0:
            if (self.blockMotion == 0):
                sounds.sfx_break.play()
            self.blockMotion = 1
            self.pickMotion = 0

    def f_drawPlayer(self, window):
        window.blit(images.characters[self.direction][self.motion], (self.realX, self.realY))
        if (self.blockMotion != 0):
            window.blit(images.blocks[self.blockMotion], (self.blockX, self.blockY))
        if (self.direction != 4):
            window.blit(images.picks[self.direction][self.pickMotion], (self.realX, self.realY))