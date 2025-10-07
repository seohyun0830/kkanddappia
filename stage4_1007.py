import pygame
import os
import random
import math

pygame.init()

screen_width=1200
screen_height=800
screen=pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("Kkanttapia")

clock = pygame.time.Clock()

# 운석이 올 때... 몇분 동안할 건가?
#----> 3분? 지루하지 않나.....
# 충돌했으면 어떻게 띄울 건지....
# --> Game over. . ..? -> 다음에 리셋
# 일단 조작.. 움직여야돼...
# ------->방향키 
# 10개씩 운석이 오나?
# 그럼 좌표를 10개에 다 담아놔야되고..
# 화면에서 벗어나면? 새로 추가해야돼

clock = pygame.time.Clock()

current_path = os.path.dirname(__file__)    #현재 파일 위치 반환
image_path = os.path.join(current_path,"images")    # images 폴더 위치 반환

background = pygame.image.load(os.path.join(image_path,"background_color.png"))
gameover = pygame.image.load(os.path.join(image_path, "gameover.png")) # Game Over 이미지 로드
spaceship = pygame.image.load(os.path.join(image_path,"spaceship.png"))
spaceship = pygame.transform.scale(spaceship, (80, 80))
spaceship_size = spaceship.get_rect().size
spaceship_width = spaceship_size[0]
spaceship_height = spaceship_size[1]
spaceship_radius = spaceship_width / 2 
spaceship_x_pos = (screen_width-spaceship_width)/2
spaceship_y_pos =(screen_height-spaceship_height)/2

spaceship_to_x = 0  # x축 이동
spaceship_to_y = 0  # y축 이동
spaceship_speed = 7

############운석들 만들기#############
# 운석 이미지 불러오기
meteor_images=[
    pygame.image.load(os.path.join(image_path,"meteor.png")),   #오른쪽 위
    pygame.image.load(os.path.join(image_path,"meteor2.png")),  #왼쪽 위
    pygame.image.load(os.path.join(image_path,"meteor3.png")),  #오른쪽 아래
    pygame.image.load(os.path.join(image_path,"meteor4.png"))]  #왼쪽 아래
meteor_size = 70
meteor_radius = meteor_size / 2 # 원형 충돌 판정을 위한 반지름
for i in range(len(meteor_images)):
    meteor_images[i] = pygame.transform.scale(meteor_images[i], (meteor_size, meteor_size))# 운석 램덤으로 뿌리기 . . . <----10개?

def create_meteor(current_time):
    img_idx = random.randint(0, 3)
    if current_time < 10:
        speed = random.randint(2, 5) # 5초 미만일 때는 느린 속도
    else:
        speed = random.randint(5, 7) # 5초 이상이면 빠른 속도 (7 포함)
    if img_idx == 0:  # 오른쪽 위
        pos_x = random.randint(screen_width, screen_width + 200)
        pos_y = random.randint(-200, 0)
        to_x = -speed
        to_y = speed
    elif img_idx == 1:  # 왼쪽 위
        pos_x = random.randint(-200, 0)
        pos_y = random.randint(-200, 0)
        to_x = speed
        to_y = speed
    elif img_idx == 2:  # 오른쪽 아래
        pos_x = random.randint(screen_width, screen_width + 200)
        pos_y = random.randint(screen_height, screen_height + 200)
        to_x = -speed
        to_y = -speed
    else:  # 왼쪽 아래
        pos_x = random.randint(-200, 0)
        pos_y = random.randint(screen_height, screen_height + 200)
        to_x = speed
        to_y = -speed
        
    return {
        "pos_x": pos_x, "pos_y": pos_y,
        "img_idx": img_idx,
        "to_x": to_x, "to_y": to_y
    }



# for 문으로 뿌려야되겠지????
# 하ㅏㅏㅏㅏㅏㅏㅏ 어렵다

# 초기 운석 뿌리기
# 근데 인덱스에 따라서 x, y 이동방향이 달라야되는디?
# 그럼 인덱스 받고 방향 고르면 될 거 같은데 아닌ㄱ?
# 4종류... 대각선 왼쪽위
# 초기 스피드도 정해야됨

#1200x800
meteors=[]
start_ticks = pygame.time.get_ticks()

running = True
while running:
    dt=clock.tick(60)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False 

        if event.type ==pygame.KEYDOWN:
            if event.key ==pygame.K_LEFT:
                spaceship_to_x = -spaceship_speed
            elif event.key==pygame.K_RIGHT:
                spaceship_to_x = spaceship_speed
            elif event.key==pygame.K_DOWN:
                spaceship_to_y = spaceship_speed
            elif event.key==pygame.K_UP:
                spaceship_to_y = -spaceship_speed

        if event.type==pygame.KEYUP:
            if event.key ==pygame.K_LEFT and spaceship_to_x < 0:
                spaceship_to_x = 0
            elif event.key == pygame.K_RIGHT and spaceship_to_x > 0:
                spaceship_to_x = 0
            elif event.key == pygame.K_DOWN and spaceship_to_y > 0:
                spaceship_to_y = 0
            elif event.key == pygame.K_UP and spaceship_to_y < 0:
                spaceship_to_y = 0            

    # 경과 시간 계산 (초 단위)
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

    # 시간에 따라 최대 운석 수 조절
    if elapsed_time < 5:
        max_meteors = 3
    else:
        max_meteors = 10
    
    # 현재 운석 수가 최대치보다 적으면 새로 생성
    if len(meteors) < max_meteors:
        meteors.append(create_meteor(elapsed_time)) # 경과 시간을 넘겨줌

    spaceship_x_pos+=spaceship_to_x
    spaceship_y_pos+=spaceship_to_y    

    if spaceship_x_pos < 0:
        spaceship_x_pos = 0
    elif spaceship_x_pos > screen_width - spaceship_width:
        spaceship_x_pos = screen_width - spaceship_width
    if spaceship_y_pos < 0: 
        spaceship_y_pos = 0
    elif spaceship_y_pos > screen_height - spaceship_height: 
        spaceship_y_pos = screen_height - spaceship_height

    screen.blit(background,(0,0))   #배경 그리기
    screen.blit(spaceship,(spaceship_x_pos,spaceship_y_pos))

   
    for meteor in meteors[:]:
        meteor["pos_x"] += meteor["to_x"]
        meteor["pos_y"] += meteor["to_y"]

        # 화면 밖으로 나갔는지 확인하고 제거
        if meteor["pos_x"] < -200 or meteor["pos_x"] > screen_width + 200 or meteor["pos_y"] < -200 or meteor["pos_y"] > screen_height + 200:
            meteors.remove(meteor)
            continue # 제거된 운석은 아래 충돌 처리를 할 필요가 없음

        screen.blit(meteor_images[meteor["img_idx"]], (meteor["pos_x"], meteor["pos_y"]))

        # 충돌 판정
        spaceship_center_x = spaceship_x_pos + spaceship_radius
        spaceship_center_y = spaceship_y_pos + spaceship_radius
        meteor_center_x = meteor["pos_x"] + meteor_radius
        meteor_center_y = meteor["pos_y"] + meteor_radius
        distance = math.sqrt((spaceship_center_x - meteor_center_x)**2 + (spaceship_center_y - meteor_center_y)**2)
        
        if distance < spaceship_radius + meteor_radius:
            game_over_rect = gameover.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(gameover, game_over_rect)
            
            pygame.display.update()
            pygame.time.delay(2000)
            
            running = False
            break

    pygame.display.update()



pygame.time.delay(2000)
pygame.quit()



