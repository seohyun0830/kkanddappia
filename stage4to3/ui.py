import pygame

class FuelGauge:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class FuelIndicator:
    def __init__(self, x, y, image, current_val, max_val):
        self.original_image = image
        self.x = x
        self.y = y
        self.max_val = max_val
        self.angle = 0

        # 초기 표시 업데이트
        self.update(current_val)

    def update(self, val):
        # 0~max_val 범위로 제한
        val = max(0, min(val, self.max_val))

        # 0% → +75도, 100% → -75도  (총 150도 회전)
        ratio = val / self.max_val
        self.angle = 75 - (ratio * 150)

    def draw(self, screen):
        rotated = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        rect = rotated.get_rect(center=(self.x, self.y))
        screen.blit(rotated, rect)
