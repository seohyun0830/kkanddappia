import pygame
from .images import inven, items

class Cinven:
    def __init__(self, pix, row, col):
        # 초기 아이템 (사다리)
        self.invenList = [5]
        
        # 각 아이템 총 갯수
        self.invenCnt = [0,0,0,0,1]

        # 한칸 갯수
        self.blockCount = [1]

        # 인벤토리 크기 설정
        self.invenRow = row // 2 - 1
        self.invenCol = col // 2 - 1
        self.invenPix = pix * 2

        # 폰트 미리 생성
        self.font = pygame.font.Font("DungGeunMO.ttf", 30)
        
        # 아이템 이름 매핑 (f_invenInfo 최적화용)
        self.item_names = {
            1: "gem", 2: "sand", 3: "fossil", 4: "paper", 5: "ladder"
        }

    def f_blockCount(self):
        self.blockCount = []
        temp_cnt = list(self.invenCnt) 
        
        # invenList에 있는 아이템 순서대로 개수를 배정합니다.
        for item_id in self.invenList:
            idx = item_id - 1 # 아이템 인덱스 (0~4)

            if temp_cnt[idx] >= 10:
                self.blockCount.append(10) # 10개 꽉 채움
                temp_cnt[idx] -= 10
            else:
                self.blockCount.append(temp_cnt[idx]) # 남은 거 다 넣음
                temp_cnt[idx] = 0

    def f_inven(self, window):
        self.f_blockCount()
        for i in range(1, self.invenCol):
            for j in range(1, self.invenRow):
                
                # 1. 좌표 계산
                x = i * self.invenPix
                y = j * self.invenPix - 30
                
                # 2. ★ 배경은 무조건 그립니다 ★
                window.blit(inven, (x, y))
                
                # 3. 리스트 인덱스 계산
                # (가로 칸 수: self.invenCol - 1)
                list_index = (j - 1) * (self.invenCol - 1) + (i - 1)
                # 4. 아이템이 있으면 그리기
                if list_index < len(self.invenList):
                    item_id = self.invenList[list_index]
                    window.blit(items[item_id - 1], (x + 30, y + 30))
                    
                    # ★★★ 1:1 매칭된 개수 표시 ★★★
                    # 이제 list_index를 그대로 쓰면 됩니다.
                    count = self.blockCount[list_index]
                    if (count == 0):
                        self.invenList.remove(item_id)
                        self.blockCount.remove(count)
                    # (0개인 경우는 안 그리도록 예외 처리 가능)
                    text = self.font.render(f"x{count}", True, (255, 255, 255))
                    if count == 10:
                        window.blit(text, (x + 60, y + 75))      
                    elif count > 0:
                        window.blit(text, (x + 70, y + 75))      

    def f_invenInfo(self, window):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # 마우스가 인벤토리 영역 안에 있는지 대략적으로 확인 (최적화)
        # (정확한 충돌 체크는 아래 루프에서 수행)
        
        for idx, item_id in enumerate(self.invenList):
            col_idx = idx % (self.invenCol - 1)
            row_idx = idx // (self.invenCol - 1)
            
            x = (col_idx + 1) * self.invenPix
            y = (row_idx + 1) * self.invenPix
            
            # 마우스가 해당 아이템 슬롯 위에 있는지 확인
            if x < mouse_x < x + self.invenPix and y < mouse_y < y + self.invenPix:
                # 딕셔너리에서 이름 가져오기 (match-case 대체)
                name = self.item_names.get(item_id, "Unknown")
                
                text = self.font.render(name, True, (255, 255, 255))
                window.blit(text, (mouse_x, mouse_y - 30))
                return # 하나 찾았으면 더 볼 필요 없으므로 종료

    def f_isLadder(self, clickX, clickY):
        for idx, item_id in enumerate(self.invenList):
            if item_id == 5: # 사다리인 경우만 좌표 확인
                col_idx = idx % (self.invenCol - 1)
                row_idx = idx // (self.invenCol - 1)
                
                x = (col_idx + 1) * self.invenPix
                y = (row_idx + 1) * self.invenPix
                
                if x < clickX < x + self.invenPix and y < clickY < y + self.invenPix:
                    return True # 1 대신 True 반환 권장
        return False # 0 대신 False 반환 권장

    def f_ladder(self, mouseX, mouseY, window):
        # 드래그 중인 사다리 이미지 그리기
        window.blit(items[4], (mouseX - 30, mouseY - 30))


    def f_putLadder(self, underMap, itemMap, upX, upY):
        # 좌표 변환 (픽셀 -> 블록 인덱스)
        bx = upX // 60
        by = upY // 60 # 60은 self.pix 값이겠죠? 매개변수로 받거나 상수 처리 추천
        
        # 범위 체크 (안전장치)
        if not (0 <= by < len(itemMap) and 0 <= bx < len(itemMap[0])):
            return # 맵 밖이면 무시

        # 설치 조건: 빈 공간(1)이고 아이템이 없어야(0) 함
        # (대장님 코드: underMap[..]==1 이 빈공간이라고 가정)
        if underMap[by][bx] == 1 and itemMap[by][bx] == 0:
            itemMap[by][bx] = 5 # 사다리 설치 완료
            # (성공했으니 invenList에서 뺄 필요 없음. f_ladder에서 이미 뺐다고 가정)
            
        # 설치 실패: 땅(0)이거나 뭔가 있음 -> 사다리 돌려받기
        elif underMap[by][bx] == 0 or itemMap[by][bx] != 0:
            if (self.invenCnt[4] <= 0):
                self.invenList.append(5)
                self.invenList.sort()

            self.invenCnt[4] += 1
        

    def f_getItem(self, itemMap, blockX, blockY):
        # 아이템 획득 (1:광석, 2:흙)
        # 범위 체크 (3 미만 -> 1, 2)
        if (len(self.invenList) >= self.invenCol * self.invenRow):
            return
        if 0 < itemMap[blockY][blockX] < 5:
            if (itemMap[blockY][blockX] == 4):
                if (self.invenCnt[3] == 0):
                    self.invenList.append(4)

                self.invenCnt[itemMap[blockY][blockX] - 1] += 1
            else:
                self.invenList.append(itemMap[blockY][blockX])
                self.invenCnt[itemMap[blockY][blockX] - 1] += 10
            self.invenList.sort()
            itemMap[blockY][blockX] = 0 # 맵에서 아이템 제거