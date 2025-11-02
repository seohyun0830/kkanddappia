from . import images
from . import fails

class Cplayer:
    def __init__(self, col, row, pix):
        self.row = row
        self.col = col

        self.pix = pix
        self.blockX = (col - 2)
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
    
    def f_setDefault(self):
        self.pickMotion = 1
        self.blockMotion = 0
        self.blockTime = 0
        self.motion = 0
        self.motionTime = 0
        if self.direction == 2: self.direction = 0
        elif self.direction == 3: self.direction = 1

    def f_isRblocked(self, under_map):
        if (under_map[self.blockY][self.blockX + 1] == 0 and (self.blockX * self.pix - self.realX) < 1):
            return 1
        return 0

    def f_isLblocked(self, under_map, itemMap):
        if (under_map[self.blockY][self.blockX - 1] == 0 and (self.realX - self.blockX * self.pix) < 1):
            return 1
        if (itemMap[self.blockY][self.blockX - 1] == 5 and (self.realX - self.blockX * self.pix) < 1):
            return 1
        return 0

    def f_gravity(self, under_map, itemMap):
        for i in range(self.blockY + 1, self.row):
            if (under_map[i][self.blockX] == 1):
                if (itemMap[i][self.blockX] == 5):
                    continue
                self.realY += 5
            else:
                break
        self.blockY = (self.realY) // self.pix

    def f_motion(self):         # 움직임
        if self.motionTime > 8:                  
            if self.motion == 1 or self.motion == 0 or self.motion == 3:
                self.motion = 2
            elif self.motion == 2:
                self.motion = 1
            self.motionTime = 0

    def f_left(self, under_map, itemMap):
        self.direction = 0
        self.motionTime += 1
        self.f_motion()
        if (self.f_isLblocked(under_map,itemMap)): # 갈 수 없으면
            self.motion = 3
            self.motionTime = 0
            self.f_breaking(under_map)
            self.toX = 0
        else:   # 갈 수 있으면
            self.blockTime = 0
            self.blockMotion = 0
            self.toX = 1
        self.realX -= self.toX

    def f_right(self, under_map):
        self.direction = 1
        self.motionTime += 1
        self.f_motion()
        if (self.f_isRblocked(under_map)): # 갈 수 없으면
            self.motion = 3
            self.motionTime = 0
            self.f_breaking(under_map)
            self.toX = 0
        else:   # 갈 수 있으면
            self.blockTime = 0
            self.blockMotion = 0
            self.toX = 1
        self.realX += self.toX

    def f_down(self, underMap):        
        if self.direction == 0: self.direction = 2
        elif self.direction == 1: self.direction = 3
        self.f_breaking(underMap)

    def f_up(self, under_map, itemMap):
        if (self.blockY > 0 and (under_map[self.blockY - 1][self.blockX] == 1 and itemMap[self.blockY - 1][self.blockX] != 5)):
            self.toY = -60
        self.realY += self.toY
        self.toY = 0

    def f_breaking(self,under_map):
        self.blockTime += 1
        if self.blockTime > 30:
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
            self.blockMotion = 3
            self.pickMotion = 0
        elif self.blockTime > 10:
            self.blockMotion = 2
            self.pickMotion = 1
        elif self.blockTime > 0:
            self.blockMotion = 1
            self.pickMotion = 0

    def f_drawPlayer(self, window):
        window.blit(images.characters[self.direction][self.motion], (self.realX, self.realY))
        if (self.blockMotion != 0):
            window.blit(images.blocks[self.blockMotion], (self.blockX, self.blockY))
        window.blit(images.picks[self.direction][self.pickMotion], (self.realX, self.realY))
