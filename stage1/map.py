from . import images

class Cmap:
    def __init__(self, window, pix):
        self.windowWidth = window.get_width()
        self.windowHeight = window.get_height()
        self.col = (self.windowWidth + pix - 10) // pix
        self.row = (self.windowHeight + pix - 10) // pix
        self.pix = pix
        self.underMap = [[0]* self.col for _ in range(self.row)]
        self.itemMap = [[0]* self.col for _ in range(self.row)]

    def f_defaultItemMap(self):
        # 광석
        self.itemMap[0][3] = 1
        self.itemMap[0][9] = 1
        self.itemMap[0][10] = 1
        self.itemMap[0][17] = 1
        self.itemMap[1][0] = 1
        self.itemMap[1][13] = 1
        self.itemMap[2][4] = 1
        self.itemMap[2][6] = 1
        self.itemMap[2][16] = 1
        self.itemMap[3][11] = 1
        self.itemMap[4][7] = 1
        self.itemMap[4][16] = 1
        self.itemMap[4][19] = 1
        self.itemMap[5][14] = 1
        self.itemMap[6][3] = 1
        self.itemMap[6][10] = 1
        self.itemMap[6][17] = 1
        self.itemMap[8][8] = 1
        self.itemMap[8][9] = 1
        self.itemMap[8][10] = 1
        self.itemMap[8][14] = 1
        self.itemMap[9][0] = 1
        self.itemMap[9][4] = 1
        self.itemMap[10][0] = 1
        self.itemMap[11][8] = 1
        self.itemMap[11][9] = 1
        self.itemMap[11][13] = 1
        self.itemMap[11][18] = 1
        self.itemMap[12][12] = 1
        self.itemMap[12][13] = 1
        # 흙
        self.itemMap[1][8] = 2
        self.itemMap[4][10] = 2
        self.itemMap[6][8] = 2
        self.itemMap[7][5] = 2
        self.itemMap[7][16] = 2
        self.itemMap[10][6] = 2
        self.itemMap[10][12] = 2
        self.itemMap[12][5] = 2
        # 석탄
        self.itemMap[0][19] = 3
        self.itemMap[5][4] = 3
        # 돌
        self.itemMap[1][9] = 5
        self.itemMap[5][18] = 5
        self.itemMap[9][8] = 5
        self.itemMap[9][10] = 5
        self.itemMap[12][7] = 5
        # 사다리
        self.itemMap[3][18] = 4
        # 지하수
        self.itemMap[9][9] = -1
    # 이 코드만 쓰고 제출하자
    def f_putLadder(self, invenList, invenRow, invenCol):
        pass

    def f_drawItemMap(self, widow):
        for i in range(self.row):
            for j in range(self.col):
                if (self.itemMap[i][j] == 0):
                    continue
                elif (self.itemMap[i][j] > 0):                
                    widow.blit(images.items[self.itemMap[i][j] - 1], (j * self.pix, i * self.pix))

    def f_drawMap(self,window, d, c_x, c_y, b):
        for i in range(self.row):
            for j in range(self.col):
                if (self.underMap[i][j] > 0):
                    continue
                if (d == 0 and j == c_x - 1 and i == c_y):
                    window.blit(images.blocks[b], ((j) * self.pix, i * self.pix))
                elif (d == 1 and j == c_x + 1 and i == c_y):
                    window.blit(images.blocks[b], ((j) * self.pix, i * self.pix))
                elif ((d == 2 or d == 3) and j == c_x and i == c_y + 1):
                    window.blit(images.blocks[b], ((j) * self.pix, i * self.pix))
                else: 
                    window.blit(images.blocks[0], (j * self.pix, i * self.pix))
        window.blit(images.enter, ((self.col - 2) * self.pix, 0))