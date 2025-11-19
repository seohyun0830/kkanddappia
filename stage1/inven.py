import pygame
from .images import inven, items

class Cinven:
    def __init__(self, pix, row, col):
        # 초기 아이템 (사다리)
        self.invenList = [4]
        
        # 인벤토리 크기 설정
        self.invenRow = row // 2 - 2
        self.invenCol = col // 2 - 1
        self.invenPix = pix * 2
        
        # 사다리 수
        self.ladderCnt = 2

        # 폰트 미리 생성
        self.font = pygame.font.Font("DungGeunMO.ttf", 30)
        
        # 아이템 이름 매핑 (f_invenInfo 최적화용)
        self.item_names = {
            1: "gem", 2: "sand", 3: "fossil", 4: "ladder"
        }

    def f_inven(self, window):
        # 텍스트 미리 생성 (최적화)
        count_text = self.font.render("10", True, (255, 255, 255))
        ladder_text = self.font.render(f"{self.ladderCnt}", True, (255,255,255))
        # ★ 전체 슬롯을 순회 (배경을 다 그리기 위해)
        # (대장님의 기존 range 범위 1 ~ invenCol 유지)
        for i in range(1, self.invenCol):
            for j in range(1, self.invenRow):
                
                # 1. 좌표 계산
                x = i * self.invenPix
                y = j * self.invenPix
                
                # 2. ★ 배경은 무조건 그립니다 ★
                window.blit(inven, (x, y))
                
                # 3. 리스트 인덱스 계산
                # (가로 칸 수: self.invenCol - 1)
                list_index = (j - 1) * (self.invenCol - 1) + (i - 1)
                
                # 4. 아이템이 있으면 그리기
                if list_index < len(self.invenList):
                    item_id = self.invenList[list_index]
                    
                    # 아이템 이미지
                    window.blit(items[item_id - 1], (x + 30, y + 30))
                    
                    # 수량 표시
                    if item_id == 4:
                        window.blit(ladder_text, (x + 70, y + 75))
                    else:
                        window.blit(count_text, (x + 70, y + 75))
                       

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
            if item_id == 4: # 사다리인 경우만 좌표 확인
                col_idx = idx % (self.invenCol - 1)
                row_idx = idx // (self.invenCol - 1)
                
                x = (col_idx + 1) * self.invenPix
                y = (row_idx + 1) * self.invenPix
                
                if x < clickX < x + self.invenPix and y < clickY < y + self.invenPix:
                    return True # 1 대신 True 반환 권장
        return False # 0 대신 False 반환 권장

    def f_ladder(self, mouseX, mouseY, window):
        # 드래그 중인 사다리 이미지 그리기
        window.blit(items[3], (mouseX - 30, mouseY - 30))


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
            itemMap[by][bx] = 4 # 사다리 설치 완료
            # (성공했으니 invenList에서 뺄 필요 없음. f_ladder에서 이미 뺐다고 가정)
            
        # 설치 실패: 땅(0)이거나 뭔가 있음 -> 사다리 돌려받기
        elif underMap[by][bx] == 0 or itemMap[by][bx] != 0:
            if (self.ladderCnt <= 0):
                self.invenList.append(4)
                self.invenList.sort()

            self.ladderCnt += 1
            print(self.ladderCnt)
        

    def f_getItem(self, itemMap, blockX, blockY):
        # 아이템 획득 (1:광석, 2:흙)
        # 범위 체크 (3 미만 -> 1, 2)
        if 0 < itemMap[blockY][blockX] < 3:
            self.invenList.append(itemMap[blockY][blockX])
            self.invenList.sort()
            itemMap[blockY][blockX] = 0 # 맵에서 아이템 제거