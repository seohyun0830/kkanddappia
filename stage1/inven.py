from images import inven, ladder

def f_inven(window, pix, col, row):
    for i in range(1, col // 2 - 1):
            for j in range(1, row // 2 - 2):
                window.blit(inven, (i * pix * 2, j * pix * 2))
                window.blit(ladder, (pix * 2 + 30, pix * 2 + 30))