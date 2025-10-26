class Cblock:
    def __init__(self, bX, bY):
        self.blockMotion = 0
        self.blockTime = 0

        self.pickMotion = 0

        self.X = bX
        self.Y = bY

    def f_breaking(self,under_map):
        self.blockTime += 1
        if self.blockTime > 30:
            under_map[self.Y][self.X] = 1
            self.blockMotion = 0
        elif self.blockTime > 20:
            self.blockMotion = 3
            self.pickMotion = 0
        elif self.blockTime > 10:
            self.blockMotion = 2
            self.pickMotion = 1
        elif self.blockTime > 0:
            self.blockMotion = 1
            self.pickMotion = 0