import pygame

class Timer:
    def __init__(self):
        self.targetTime = 12 * 60 * 1000 + 1 # 12분 (밀리초 단위)
        self.start_ticks = pygame.time.get_ticks()
        self.font_timer = pygame.font.Font("DungGeunMO.ttf", 40)

    def get_remianing_time(self):
        # 1. 흐른 시간 계산
        elapsed_time = pygame.time.get_ticks() - self.start_ticks
        
        remaining_time = self.targetTime - elapsed_time

        if remaining_time < 0:
            remaining_time = 0

        return remaining_time

    def get_time_text(self):
        remaining_time = self.get_remianing_time()

        if remaining_time < 0:
            remaining_time = 0

        seconds = (remaining_time // 1000) % 60
        minutes = (remaining_time // 1000) // 60
        
        timer_text = self.font_timer.render(f"{minutes:02d}:{seconds:02d}", True, (255, 255, 255))
        return timer_text

    def reset(self):
        self.start_ticks = pygame.time.get_ticks()