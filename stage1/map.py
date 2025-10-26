import images

class Cmap:
    def __init__(self, window, pix):
        self.windowWidth = window.get_width()
        self.windowHeight = window.get_height()
        self.col = (self.windowWidth + pix - 10) // pix
        self.row = (self.windowHeight + pix - 10) // pix
        self.underMap = [[0]* self.col for _ in range(self.row)]

    def f_drawMap(self,window, underMap, d, c_x, c_y, b, pix):
        window.blit(images.background, (0,0))
        for i in range(self.row):
            for j in range(self.col):
                if (underMap[i][j] == 1):
                    continue
                if (d == 0 and j == c_x - 1 and i == c_y):
                    window.blit(images.blocks[b], ((j) * pix, i * pix))
                elif (d == 1 and j == c_x + 1 and i == c_y):
                    window.blit(images.blocks[b], ((j) * pix, i * pix))
                elif ((d == 2 or d == 3) and j == c_x and i == c_y + 1):
                    window.blit(images.blocks[b], ((j) * pix, i * pix))
                else: 
                    window.blit(images.blocks[0], (j * pix, i * pix))

    def f_updateMap(self, c_x, c_y, value):
        self.underMap[c_y][c_x] = value
