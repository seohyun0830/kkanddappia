from . import images

class Cmap:
    def __init__(self, window, pix):
        self.windowWidth = window.get_width()
        self.windowHeight = window.get_height()
        
        self.pix = pix
        # 맵 크기 계산
        self.col = (self.windowWidth + pix - 10) // pix + 1
        self.row = (self.windowHeight + pix - 10) // pix
        
        # 0: 땅(블록 있음), 1: 빈공간(블록 없음)
        self.underMap = [[0] * self.col for _ in range(self.row)]
        
        # 0: 없음, 1:광석, 2:흙, 3:석탄, 4:종이, 5:사다리, 6:돌, -1:지하수
        self.itemMap = [[0] * self.col for _ in range(self.row)]

    def f_defaultItemMap(self, MODE):
        # 데이터 관리를 쉽게 하기 위해 좌표 리스트로 정리
        
        # 1. 광석 (ID: 1)
        ores = [
            (0,3), (0,9), (0,10), (0,17),
            (1,0), (1,13),
            (2,4), (2,6), (2,16),
            (3,11),
            (4,7), (4,16), (4,19),
            (5,14),
            (6,3), (6,10), (6,17),
            (8,8), (8,9), (8,10), (8,14),
            (9,0), (9,4),
            (10,0),
            (11,8), (11,9), (11,13), (11,18),
            (12,12), (12,13)
        ]
        
        # 2. 흙 (ID: 2)
        soils = [
            (1,8),
            (4,10),
            (6,8),
            (7,5), (7,16),
            (10,6), (10,12),
            (12,5)
        ]
        
        # 3. 석탄/화석 (ID: 3)
        coals = [(0,19), (4,2), (5,4)]
        
        if MODE == 2:
        # 4. 종이 (ID: 4)
            papers = [(4,5), (1,15), (11,3)]

        # 6. 돌 (ID: 6)
        stones = [(1,9), (1,3), (1,18), (2,2), (6,13), (5,18), (8,2), (9,8), (9,10), (10,15), (12,7)]
        
        # -1. 지하수 (ID: -1)
        waters = [(2,3), (5,19) ,(9,9)]

        # 리스트를 순회하며 맵에 적용 (일괄 처리)
        self._apply_items(ores, 1)
        self._apply_items(soils, 2)
        self._apply_items(coals, 3)
        if MODE == 2:
            self._apply_items(papers, 4)
        self._apply_items(stones, 6)
        self._apply_items(waters, -1)

    # 내부 헬퍼 함수: 리스트의 좌표들을 itemMap에 적용
    def _apply_items(self, coords, item_id):
        for y, x in coords:
            # 인덱스 에러 방지
            if 0 <= y < self.row and 0 <= x < self.col:
                self.itemMap[y][x] = item_id

    def f_drawItemMap(self, window): 
        for i in range(self.row):
            for j in range(self.col):
                item_id = self.itemMap[i][j]
                if item_id > 0:
                    # 아이템 이미지 그리기 (ID-1 인덱스 사용)
                    window.blit(images.items[item_id - 1], (j * self.pix, i * self.pix))

    def f_drawMap(self, window, direction, p_x, p_y, blockMotion):
        # ★ 최적화 핵심: 루프 밖에서 '파괴 중인 블록 좌표'를 미리 계산
        target_x, target_y = -1, -1
        
        # 블록을 캐는 중(motion > 0)일 때만 타겟 계산
        if blockMotion > 0:
            if direction == 0:   target_x, target_y = p_x - 1, p_y # 왼
            elif direction == 1: target_x, target_y = p_x + 1, p_y # 오
            elif direction in [2, 3]: target_x, target_y = p_x, p_y + 1 # 아
        
        # 맵 그리기 루프
        for i in range(self.row):
            for j in range(self.col):
                # 이미 파괴된 블록(1)이면 그리지 않고 스킵
                if self.underMap[i][j] > 0:
                    continue
                
                # 그릴 위치
                pos = (j * self.pix, i * self.pix)
                
                # ★ 단순 비교: 현재 그리는 블록이 타겟 블록인가?
                
                if (self.itemMap[i][j] == 2):                                   # 흙
                    if j == target_x and i == target_y:
                        # 파괴 애니메이션 블록 그리기
                        window.blit(images.blocks[blockMotion], pos)
                    else:
                        # 일반 블록 그리기
                        window.blit(images.soilBlocks[(j + i) % 4], pos)
                elif (self.itemMap[i][j] == 6 or self.itemMap[i][j] == 3):      # 돌, 화석
                    if j == target_x and i == target_y:
                        # 파괴 애니메이션 블록 그리기
                        window.blit(images.blocks[blockMotion], pos)
                    else:
                        # 일반 블록 그리기
                        window.blit(images.rockBlocks[(j + i) * j % 5], pos)
                elif (self.itemMap[i][j] == 4):      # 종이
                    if j == target_x and i == target_y:
                        # 파괴 애니메이션 블록 그리기
                        window.blit(images.blocks[blockMotion], pos)
                    else:
                        # 일반 블록 그리기
                        window.blit(images.specialBlocks[(j + i) % 3], pos)
                
                else:                                                           # 일반
                    if j == target_x and i == target_y:
                        # 파괴 애니메이션 블록 그리기
                        window.blit(images.blocks[blockMotion], pos)
                    else:
                        # 일반 블록 그리기
                        window.blit(images.blocks[0], pos)
        # 탈출구(빛) 그리기
        window.blit(images.enter, ((self.col - 3) * self.pix, 0))