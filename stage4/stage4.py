import pygame
import os
import random
import math

pygame.init()

screen_width=1200
screen_height=800
screen=pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("Kkanttappia")

clock = pygame.time.Clock()
 
current_path = os.path.dirname(__file__)    #현재 파일 위치 반환
image_path = os.path.join(current_path,"images")    # images 폴더 위치 반환

background = pygame.image.load(os.path.join(image_path,"background_color.png"))
gameover = pygame.image.load(os.path.join(image_path, "gameover.png")) 
spaceship = pygame.image.load(os.path.join(image_path,"spaceship.png"))
warning_img1 = pygame.image.load(os.path.join(image_path, "warning1.png")) 
warning_img2 = pygame.image.load(os.path.join(image_path, "warning2.png")) 
alien = pygame.image.load(os.path.join(image_path,"alien.png"))
bubble = pygame.image.load(os.path.join(image_path,"bubble.png"))

alien = pygame.transform.scale(alien, (100, 100))
alien_radius = 100 / 2 * 0.8
alien_x_pos = 0 
alien_y_pos = 0
alien_appeared = False # 외계인이 한 번만 나타나게 할 변수

bubble = pygame.transform.scale(bubble, (120, 120)) # 우주선보다 살짝 크게
is_shield_active = False # 쉴드가 활성화됐는지 알려주는 변수
shield_start_time = 0 # 쉴드가 언제 시작됐는지 기록할 변수

spaceship = pygame.transform.scale(spaceship, (80, 80))
spaceship_size = spaceship.get_rect().size
spaceship_width = spaceship_size[0]
spaceship_height = spaceship_size[1]
spaceship_radius = spaceship_width / 2 *0.7
spaceship_x_pos = (screen_width-spaceship_width)/2
spaceship_y_pos =(screen_height-spaceship_height)/2

spaceship_to_x = 0  
spaceship_to_y = 0 
spaceship_speed = 7

############운석들 만들기#############
# 운석 이미지 불러오기
meteor_images=[
    pygame.image.load(os.path.join(image_path,"meteor.png")),   #오른쪽 위
    pygame.image.load(os.path.join(image_path,"meteor2.png")),  #왼쪽 위
    pygame.image.load(os.path.join(image_path,"meteor3.png")),  #오른쪽 아래
    pygame.image.load(os.path.join(image_path,"meteor4.png"))]  #왼쪽 아래
meteor_size = 70

meteor_radius = meteor_size / 2 *0.8 #충돌 판정할 때 원 거리 공식 이용해서..
for i in range(len(meteor_images)):
    meteor_images[i] = pygame.transform.scale(meteor_images[i], (meteor_size, meteor_size)) # 운석 램덤으로 뿌리기 . . . <----10개?

#운석 생성
def create_meteor(current_time):
    img_idx = random.randint(0, 3)  # 이미지 중에 랜덤 불러와서
    if current_time < 10:
        speed = random.randint(2, 5) # 5초 미만일 때는 느리다가
    else:
        speed = random.randint(5, 7) # 5초 이상이면 빠르게
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


#1200x800
meteors=[]
start_ticks = pygame.time.get_ticks()


is_defect_event = False     #결함 체크할 변수

#메인 게임 루프
running = True
while running:
    dt=clock.tick(60)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False 
        if not is_defect_event: #결함 없을 때 키보드 먹도록..(운석 충돌 때문에 일단 이렇게 둠)
            if event.type ==pygame.KEYDOWN:
                if event.key ==pygame.K_LEFT: spaceship_to_x = -spaceship_speed
                elif event.key==pygame.K_RIGHT: spaceship_to_x = spaceship_speed
                elif event.key==pygame.K_DOWN: spaceship_to_y = spaceship_speed
                elif event.key==pygame.K_UP: spaceship_to_y = -spaceship_speed
            if event.type==pygame.KEYUP:
                if (event.key ==pygame.K_LEFT and spaceship_to_x < 0) or (event.key == pygame.K_RIGHT and spaceship_to_x > 0): spaceship_to_x = 0
                elif (event.key ==pygame.K_DOWN and spaceship_to_y > 0) or (event.key == pygame.K_UP and spaceship_to_y < 0): spaceship_to_y = 0


    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000   #경과시간

    if 15 <= elapsed_time < 20:     #일단 15~20초 사이에 결함문구 뜨게 하고
        is_defect_event = True  
    else:       #이후에 다시 운석피하기
        is_defect_event = False

    if not is_defect_event: #이것도 결함 아닐 때
        # 운석 생성
        if elapsed_time < 5: #5초 이하일 때는 3개만 만들고
            max_meteors = 3 
        else: max_meteors = 10 #이후에는 10개씩

        if elapsed_time > 30 and not alien_appeared:    #30초 넘으면 외계인 나오게
            alien_appeared = True 

            # 화면 중앙 위쪽에서 등장  (일단은....)
            alien_x_pos = screen_width / 2 - alien.get_width() / 2
            alien_y_pos = 100

        if alien_appeared and not is_shield_active: #쉴드 받기 전
        # 충돌 계산
            alien_center_x = alien_x_pos + alien_radius
            alien_center_y = alien_y_pos + alien_radius
            spaceship_center_x = spaceship_x_pos + spaceship_radius
            spaceship_center_y = spaceship_y_pos + spaceship_radius
            distance = math.sqrt((spaceship_center_x - alien_center_x)**2 + (spaceship_center_y - alien_center_y)**2)
        
            if distance < spaceship_radius + alien_radius:  #우주선랑 외계인이랑 충돌됐다고 판단되면
                is_shield_active = True # 쉴드 활성화
                shield_start_time = elapsed_time # 쉴드 시작 시간 기록
                alien_x_pos = -2000 #외계인 날려버리기..
                alien_y_pos = -2000
       

        if is_shield_active:
        # 쉴드 시작 후 5초가 지났으면 쉴드 해제
            if elapsed_time - shield_start_time > 5:
                is_shield_active = False

        #운석 계속 만들기
        if len(meteors) < max_meteors:
            meteors.append(create_meteor(elapsed_time))

        #우주선 위치 업뎃
        spaceship_x_pos += spaceship_to_x
        spaceship_y_pos += spaceship_to_y 

        # 화면 경계 처리 (우주선이 화면 못 벗어나게)
        if spaceship_x_pos < 0: spaceship_x_pos = 0
        elif spaceship_x_pos > screen_width - spaceship_width: spaceship_x_pos = screen_width - spaceship_width
        if spaceship_y_pos < 0: spaceship_y_pos = 0
        elif spaceship_y_pos > screen_height - spaceship_height: spaceship_y_pos = screen_height - spaceship_height

        # 운석 처리
        for meteor in meteors[:]:
            meteor["pos_x"] += meteor["to_x"]
            meteor["pos_y"] += meteor["to_y"]
            if not (-200 < meteor["pos_x"] < screen_width + 200 and -200 < meteor["pos_y"] < screen_height + 200):  #운석이 완전히 벗어나게
                meteors.remove(meteor)
                continue
            if is_shield_active:
            # 쉴드가 켜져 있을 때 운석과 부딪히면 운석만 파괴
                shield_center_x = spaceship_x_pos + spaceship_radius # 쉴드 중심 우주선과 같도록 설졍..
                shield_center_y = spaceship_y_pos + spaceship_radius
                meteor_center_x = meteor["pos_x"] + meteor_radius
                meteor_center_y = meteor["pos_y"] + meteor_radius
                distance = math.sqrt((shield_center_x - meteor_center_x)**2 + (shield_center_y - meteor_center_y)**2)
                
                if distance < spaceship_radius + meteor_radius: #우주선이랑 충돌했는지
                    meteors.remove(meteor) # 부딪힌 운석 제거
                    meteors.append(create_meteor(elapsed_time)) # 새 운석 생성
            else:
            #쉴드 안켜져있을 때
            # 충돌 판정
                spaceship_center_x = spaceship_x_pos + spaceship_radius
                spaceship_center_y = spaceship_y_pos + spaceship_radius
                meteor_center_x = meteor["pos_x"] + meteor_radius
                meteor_center_y = meteor["pos_y"] + meteor_radius
                distance = math.sqrt((spaceship_center_x - meteor_center_x)**2 + (spaceship_center_y - meteor_center_y)**2)

                if distance < spaceship_radius + meteor_radius: #충돌하면 겜 오버
                    game_over_rect = gameover.get_rect(center=(screen_width / 2, screen_height / 2))
                    screen.blit(gameover, game_over_rect)
                    pygame.display.update()
                    pygame.time.delay(2000)
                    running = False
                    break
    if not running:
        break

    screen.blit(background,(0,0))
    screen.blit(spaceship,(spaceship_x_pos,spaceship_y_pos))
    for meteor in meteors:
        screen.blit(meteor_images[meteor["img_idx"]], (meteor["pos_x"], meteor["pos_y"]))

    if alien_appeared:
        screen.blit(alien, (alien_x_pos, alien_y_pos))

    if is_shield_active:
        # 버블 이미지의 중심을 우주선의 중심과 맞춤
        bubble_rect = bubble.get_rect(center = (spaceship_x_pos + spaceship_width/2, spaceship_y_pos + spaceship_height/2))
        screen.blit(bubble, bubble_rect)
    if is_defect_event: #결함이벤트 발생하면
        flicker_value = (pygame.time.get_ticks() // 200) % 2    #짝수 초일 때
        if flicker_value == 0:
            screen.blit(warning_img1, (0,0))
        else:   #홀수 초일 때
            screen.blit(warning_img2, (0,0))
    pygame.display.update()

pygame.quit()