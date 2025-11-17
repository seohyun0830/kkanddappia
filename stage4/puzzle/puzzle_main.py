import pygame
import os
from puzzle.images import *


pygame.init()
pygame.mixer.init()

#audio_path = os.path.join(os.path.dirname(__file__), "..", "audios", "while_puzzle.mp3")

puzzle_audio_path = os.path.join(os.path.dirname(__file__), "..", "audios", "while_puzzle.wav")
puzzle_sound = pygame.mixer.Sound(puzzle_audio_path)

wrong_clicked_audio_path = os.path.join(os.path.dirname(__file__), "..", "audios", "wrong_clicked.mp3")
wrong_clicked_sound = pygame.mixer.Sound(wrong_clicked_audio_path)
correct_ans_audio_path = os.path.join(os.path.dirname(__file__), "..", "audios", "correct_ans.mp3")
correct_ans_sound = pygame.mixer.Sound(correct_ans_audio_path)

puzzle_success_audio_path = os.path.join(os.path.dirname(__file__), "..", "audios", "puzzle_success.mp3")
puzzle_success_sound = pygame.mixer.Sound(puzzle_success_audio_path)
def f_puzzle(window):
    total_time = 60 * 1000 
    start_ticks = pygame.time.get_ticks() 
    font_path = os.path.join(os.path.dirname(__file__), "..", "font", "DungGeunMo.ttf")
    font = pygame.font.Font(font_path, 50)
    remaining_time_sec = 60
    play = True

    ans = [[(425, 240), (445, 255)], [(340,255), (365, 280)], [(185, 375), (195, 390)], [(325,430), (365, 445)], [(390, 460), (415, 475)], [(135, 540), (245, 565)]]
    delay = 0
    res =[0, 0, 0, 0, 0, 0]
    puzzle_sound.play(loops=-1)
    while play:
        mouseX, mouseY = pygame.mouse.get_pos()
        clicked = False

        if (remaining_time_sec <= 0):
            play = False
            puzzle_sound.stop()
            return -1                                   # fail

        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                play = False
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickedX, clickedY = mouseX, mouseY
                clicked = True
        flag = 1
        if (clicked):
            for i in range(len(ans)):
                if (ans[i][0][0] <= clickedX <= ans[i][1][0]) and (ans[i][0][1] <= clickedY <= ans[i][1][1]):
                    res[i] = 1
                    flag = 1
                    correct_ans_sound.play()
                    break
                elif (ans[i][0][0] <= clickedX - 500 <= ans[i][1][0]) and (ans[i][0][1] <= clickedY <= ans[i][1][1]):
                    res[i] = 1
                    flag = 1
                    correct_ans_sound.play()
                    break
                elif (clickedX > 100 and clickedX < 590 and clickedY >= 150 and clickedY <= 550):
                    flag = 0
                    
                elif (clickedX > 600 and clickedX < 1090 and clickedY >= 150 and clickedY <= 550):
                    flag = 0
                    
            if (flag == 0):
                wrong_clicked_sound.play()
                delay += 5

        window.blit(puzzle1, (100,150))
        window.blit(puzzle2, (600,150))
        window.blit(outline3, (90,90))

        for i in range(len(res)):
            if (res[i] == 1):
                
                window.blit(checks[i], (100,150))
                window.blit(checks[i], (600,150))

        current_ticks = pygame.time.get_ticks()                 # 현재 틱 수
        elapsed_time = current_ticks - start_ticks               # 경과 시간 계산

        remaining_time_ms = total_time - elapsed_time      # 남은 시간 계산

        remaining_time_sec = remaining_time_ms // 1000 - delay     # 남은 시간을 초 단위로 변환
    

        timer_text = font.render(f"{remaining_time_sec}", False, (0, 0, 0))
        window.blit(timer_text, (110, 100))
        
        default_text = font.render(f"고장난 곳을 찾아주세요!", False, (0,0,0))
        window.blit(default_text, (300, 110))

        for i in range(sum(res)):
            window.blit(found, (1050 - i * 40, 655))
        for i in range(6 - sum(res)):
            window.blit(notFound, (1050 - i * 40 - 40 * sum(res), 655))
        if (sum(res) == 6):
            play = False
        
        pygame.display.update()
    
    font = pygame.font.Font(font_path, 150)

    text = font.render(f"SUCCESS!!", False, (230, 255, 0))
    shadow = font.render(f"SUCCESS!!", False, (0, 0, 0))
    puzzle_success_sound.play()
    puzzle_sound.stop()
    for i in range(3):

        window.blit(shadow, (305, 305))
        window.blit(text, (300, 300))
        pygame.display.update()
        pygame.time.delay(800)
    

    return 1                                          # success

if __name__ == "__main__":
    # 화면 크기
    window_width = 1200
    window_height = 800         
    window = pygame.display.set_mode((window_width,window_height))
    pygame.display.set_caption("Kkanddappia!")

    f_puzzle(window)