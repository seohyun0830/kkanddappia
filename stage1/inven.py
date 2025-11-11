import pygame
from .images import inven, items

class Cinven:
    def __init__(self, pix, row, col):
        self.invenList = [4]
        self.invenRow = row // 2 - 2
        self.invenCol = col // 2 - 1
        self.invenPix = pix * 2
        self.font = pygame.font.Font(None, 30)

    def f_inven(self, window):
        for i in range(1, self.invenCol):
            for j in range(1, self.invenRow):
                window.blit(inven, (i * self.invenPix, j * self.invenPix))
                if ((j - 1) * self.invenCol + (i - 1)) < len(self.invenList):
                    window.blit(items[self.invenList[(j - 1) * self.invenCol + (i - 1)] - 1], (i * self.invenPix + 30, j * self.invenPix + 30))
    
    def f_invenInfo(self, window):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        text = self.font.render(f"Nothing", True, (255, 255, 255))
        for i in range(1, self.invenCol):
            for j in range(1, self.invenRow):
                if ((i - 1) + (j - 1) * self.invenCol) < len(self.invenList):
                    if (mouse_x > i * self.invenPix and mouse_x < (i + 1) * self.invenPix
                         and mouse_y > j * self.invenPix and mouse_y < (j + 1) * self.invenPix):
                        match self.invenList[(i - 1) + (j - 1) * self.invenCol]:
                            case 1:
                                text = self.font.render(f"gem", True, (255,255,255))
                            case 2:
                                text = self.font.render(f"sand", True, (255, 255, 255))
                            case 3:
                                text = self.font.render(f"fossil", True, (255, 255, 255))
                            case 4:
                                text = self.font.render(f"ladder", True, (255, 255, 255))
                        window.blit(text, (mouse_x, mouse_y - 30))

    def f_isLadder(self, clickX, clickY):
        for i in range(1, self.invenCol):
            for j in range(1, self.invenRow):
                if ((i - 1) + (j - 1) * self.invenCol) < len(self.invenList):
                    if (clickX > i * self.invenPix and clickX < (i + 1) * self.invenPix
                         and clickY > j * self.invenPix and clickY < (j + 1) * self.invenPix):
                        if (self.invenList[(i - 1) + (j - 1) * self.invenCol] == 4):
                            return 1
        return 0
    
    def f_ladder(self, mouseX, mouseY, window):
        window.blit(items[3], (mouseX - 30, mouseY - 30))
        for i in range(len(self.invenList)):
            if (self.invenList[i] == 4):
                del self.invenList[i]

    def f_putLadder(self, underMap, itemMap, upX, upY):
        if (underMap[upY // 60][upX // 60] == 1 and itemMap[upY // 60][upX // 60] == 0):
            itemMap[upY // 60][upX // 60] = 4
        elif (underMap[upY // 60][upX // 60] == 0):
            self.invenList.append(4)
            self.invenList.sort()

    def f_getItem(self, itemMap, realX, realY):
        if (itemMap[realY // 60][realX // 60] > 0 and itemMap[realY // 60][realX //60] <3):
            self.invenList.append(itemMap[realY // 60][realX // 60])
            self.invenList.sort()
            itemMap[realY // 60][realX // 60] = 0