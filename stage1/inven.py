import pygame
from .images import inven, items

class Cinven:
    def __init__(self, pix, row, col):
        self.invenList = []
        self.invenRow = row // 2 - 2
        self.invenCol = col // 2 - 1
        self.pix = pix
        self.font = pygame.font.Font(None, 50)

    def f_inven(self, window):
        for i in range(1, self.invenCol):
            for j in range(1, self.invenRow):
                window.blit(inven, (i * self.pix * 2, j * self.pix * 2))
                if ((j - 1) * self.invenCol + (i - 1)) < len(self.invenList):
                    window.blit(items[self.invenList[(j - 1) * self.invenCol + (i - 1)] - 1], (i * self.pix * 2 + 30, j * self.pix * 2 + 30))
    
    def f_invenInfo(self, window):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_bX = mouse_x // (self.pix * 2)
        mouse_bY = mouse_y // (self.pix * 2)

        text = self.font.render(f"Nothing", True, (255, 255, 255))
        for i in range(1, self.invenCol):
            for j in range(1, self.invenRow):
                if (mouse_x // self.pix + mouse_y // self.pix * mouse_x // self.pix) <= len(self.invenList):
                    if (mouse_x > i * self.pix and mouse_x < i * self.pix + self.pix and
                        mouse_y > j * self.pix and mouse_y < j * self.pix + self.pix):
                        if items[mouse_x // self.pix + mouse_y // self.pix * mouse_x // self.pix] == 1: # 광물
                            text = self.font.render(f"광물", True, (255, 255, 255))
                        elif items[self.invenList[(j - 1) * self.invenCol + (i - 1)]] == 2: # 흙
                            text = self.font.render(f"흙", True, (255, 255, 255))
                        elif items[self.invenList[(j - 1) * self.invenCol + (i - 1)]] == 3: # 화석
                            text = self.font.render(f"화석", True, (255, 255, 255))
                        elif items[self.invenList[(j - 1) * self.invenCol + (i - 1)]] == 4: # 사다리
                            text = self.font.render(f"사다리", True, (255, 255, 255))
                    window.blit(text, (mouse_x, mouse_y - 30))


    def f_getItem(self, itemMap, realX, realY):
        if (itemMap[realY // 60][realX // 60] > 0 and itemMap[realY // 60][realX //60] <3):
            self.invenList.append(itemMap[realY // 60][realX // 60])
            self.invenList.sort()
            itemMap[realY // 60][realX // 60] = 0
