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
warning_img1 = pygame.image.load(os.path.join(image_path, "warning1.png")) 
warning_img2 = pygame.image.load(os.path.join(image_path, "warning2.png")) 
alien = pygame.image.load(os.path.join(image_path,"alien.png"))
bubble = pygame.image.load(os.path.join(image_path,"bubble.png"))
blackhole =pygame.image.load(os.path.join(image_path,"blackhole.png"))
success=pygame.image.load(os.path.join(image_path,"success.png"))
meteor_collision=pygame.image.load(os.path.join(image_path,"meteor_collision.png"))
meteor_collision=pygame.transform.scale(meteor_collision,(1200,800))
kkanttapia=pygame.image.load(os.path.join(image_path,"kkanttapia.png"))


alien = pygame.transform.scale(alien, (100, 100))
alien_radius = 100 / 2 * 0.8
alien_x_pos = 0 
alien_y_pos = 0
alien_appeared = False # 외계인이 한 번만 나타나게 할 변수

bubble = pygame.transform.scale(bubble, (120, 120)) # 우주선보다 살짝 크게
is_shield_active = False # 쉴드가 활성화됐는지 알려주는 변수
shield_start_time = 0 # 쉴드가 언제 시작됐는지 기록할 변수

blackhole= pygame.transform.scale(blackhole, (100, 100)) # 블랙홀 크기 조절
blackhole_radius = 100 / 2 * 0.4 # 충돌 판정 범위 (살짝 작게)
blackhole_x_pos = 0
blackhole_y_pos = 0
blackhole_appeared = False # 블랙홀 등장 스위치

keyborad_rotation=0 #키보드 회전 변수
next_rotation=25.0
left_life=4
is_invincible = False 
invincible_start_time = 0 

############운석들 만들기#############
# 운석 이미지 불러오기
meteor_images=[
    pygame.image.load(os.path.join(image_path,"meteor.png")),   #오른쪽 위
    pygame.image.load(os.path.join(image_path,"meteor2.png")),  #왼쪽 위
    pygame.image.load(os.path.join(image_path,"meteor3.png")),  #오른쪽 아래
    pygame.image.load(os.path.join(image_path,"meteor4.png"))]  #왼쪽 아래
meteor_size = 70
meteor_radius = meteor_size / 2 *0.8    #충돌 판정할 때 원 거리 공식 이용해서..
for i in range(len(meteor_images)):
    meteor_images[i] = pygame.transform.scale(meteor_images[i], (meteor_size, meteor_size)) # 운석 램덤으로 뿌리기 . . . <----10개?

#  우주선 이미지 불러오기
spaceship_images=[
    pygame.image.load(os.path.join(image_path,"spaceship_0.png")),   
    pygame.image.load(os.path.join(image_path,"spaceship_90.png")),  
    pygame.image.load(os.path.join(image_path,"spaceship_180.png")), 
    pygame.image.load(os.path.join(image_path,"spaceship_270.png"))] 

for i in range(len(spaceship_images)):
    spaceship_images[i] = pygame.transform.scale(spaceship_images[i], (80, 80))

#일단 기본 우주선 모양으로 . . .
spaceship_size = spaceship_images[0].get_rect().size
spaceship_width = spaceship_size[0]
spaceship_height = spaceship_size[1]
spaceship_radius = spaceship_width / 2 *0.7
spaceship_x_pos = (screen_width-spaceship_width)/2
spaceship_y_pos =(screen_height-spaceship_height)/2
spaceship_to_x = 0  
spaceship_to_y = 0 
spaceship_speed = 7

life_images=[
    pygame.image.load(os.path.join(image_path,"life1.png")),   
    pygame.image.load(os.path.join(image_path,"life2.png")),  
    pygame.image.load(os.path.join(image_path,"life3.png")), 
    pygame.image.load(os.path.join(image_path,"life4.png"))] 
for i in range(len(life_images)):
    life_images[i] = pygame.transform.scale(life_images[i], (200, 40))

move_success_images=[
    pygame.image.load(os.path.join(image_path,"move_success1.png")),   
    pygame.image.load(os.path.join(image_path,"move_success2.png")),  
    pygame.image.load(os.path.join(image_path,"move_success3.png")),
    pygame.image.load(os.path.join(image_path,"move_success4.png"))] 


#운석 생성
def create_meteor(current_time):
    img_idx = random.randint(0, 3)  # 이미지 중에 랜덤 불러와서
    if current_time < 10:  
        speed = random.randint(2, 5) # 5초 미만일 때는 느리다가
    else:
        speed = random.randint(1, 3) # 5초 이상이면 빠르게
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
was_defect_paused = False 
pause_start_ticks = 0     
total_paused_ms = 0       
font_path = os.path.join(current_path, "font")
game_font = pygame.font.Font(os.path.join(font_path, "DungGeunMo.ttf"), 40)
TOTAL_GAME_TIME = 100 
TIMER_COLOR = (200, 200, 200) 

#메인 게임 루프
running = True
while running:
    dt=clock.tick(60)

    current_ticks = pygame.time.get_ticks() # 현재 실제 시간
    real_elapsed_time = (current_ticks - start_ticks) / 1000.0
    

    # 진짜 게임 시간을 기준으로 결함 이벤트 체크
    if 15 <= real_elapsed_time < 20: 
        is_defect_event = True
        if not was_defect_paused: # 방금 멈추기 시작했다면
            pause_start_ticks = current_ticks # 멈춘 순간의 실제 시간 기록
            was_defect_paused = True
    else: 
        if was_defect_paused: #방금 멈춤이 끝났다면
            total_paused_ms += (current_ticks - pause_start_ticks) #멈춰있던 시간을 총합에 더함
            spaceship_to_x=0
            spaceship_to_y=0
        is_defect_event = False
        was_defect_paused = False
    # 진짜 게임 시간 = (현재시간 - 시작시간 - 총 멈췄던 시간)
    game_elapsed_ms = current_ticks - start_ticks - total_paused_ms
    game_elapsed_time = game_elapsed_ms / 1000.0 # 초 단위

    remaining_seconds = max(0, TOTAL_GAME_TIME - game_elapsed_time)  #남은 시간
    minutes = int(remaining_seconds // 60)
    seconds = int(remaining_seconds % 60)
    timer_text_str = f"{minutes:02}:{seconds:02}"

    if remaining_seconds <= 0 and running:
        kkanttapia_rect = kkanttapia.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(kkanttapia, kkanttapia_rect) 
        pygame.display.update()
        pygame.time.delay(3000) 
        running = False 

    if game_elapsed_time >= next_rotation:
        keyborad_rotation = (keyborad_rotation + 1) % 4 # 4가지 로테이션
        next_rotation += 25.0 
        spaceship_to_y=0
        spaceship_to_x=0

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False 
        if not is_defect_event: #결함 없을 때 키보드 먹도록..(운석 충돌 때문에 일단 이렇게 둠)
            if event.type ==pygame.KEYDOWN:
                if keyborad_rotation==0:
                    if event.key ==pygame.K_LEFT: spaceship_to_x = -spaceship_speed
                    elif event.key==pygame.K_RIGHT: spaceship_to_x = spaceship_speed
                    elif event.key==pygame.K_DOWN: spaceship_to_y = spaceship_speed
                    elif event.key==pygame.K_UP: spaceship_to_y = -spaceship_speed
                elif keyborad_rotation==1:
                    if event.key ==pygame.K_LEFT: spaceship_to_y = -spaceship_speed
                    elif event.key==pygame.K_RIGHT: spaceship_to_y = spaceship_speed
                    elif event.key==pygame.K_DOWN: spaceship_to_x = -spaceship_speed
                    elif event.key==pygame.K_UP: spaceship_to_x = spaceship_speed
                elif keyborad_rotation==2:
                    if event.key ==pygame.K_LEFT: spaceship_to_x = spaceship_speed
                    elif event.key==pygame.K_RIGHT: spaceship_to_x = -spaceship_speed
                    elif event.key==pygame.K_DOWN: spaceship_to_y = -spaceship_speed
                    elif event.key==pygame.K_UP: spaceship_to_y = spaceship_speed
                else:
                    if event.key ==pygame.K_LEFT: spaceship_to_y = spaceship_speed
                    elif event.key==pygame.K_RIGHT: spaceship_to_y = -spaceship_speed
                    elif event.key==pygame.K_DOWN: spaceship_to_x = spaceship_speed
                    elif event.key==pygame.K_UP: spaceship_to_x = -spaceship_speed
                
            if event.type==pygame.KEYUP:
                if keyborad_rotation==0: # 기본
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: spaceship_to_x = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN: spaceship_to_y = 0
                elif keyborad_rotation==1: # 90도
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN: spaceship_to_x = 0
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: spaceship_to_y = 0
                elif keyborad_rotation==2: # 180도
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: spaceship_to_x = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN: spaceship_to_y = 0
                else: # 270도
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN: spaceship_to_x = 0
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: spaceship_to_y = 0


    if not is_defect_event: #이것도 결함 아닐 때
        #무적 시간 끝났나
        if is_invincible and game_elapsed_time - invincible_start_time > 2: # 2초간 무적
            is_invincible = False
        # 운석 생성
        if game_elapsed_time < 5: #5초 이하일 때는 3개만 만들고
            max_meteors = 3 
        else: max_meteors = 10 #이후에는 10개씩

        if game_elapsed_time > 30 and not alien_appeared:    #30초 넘으면 외계인 나오게
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
                shield_start_time = game_elapsed_time # 쉴드 시작 시간 기록
                alien_x_pos = -2000 #외계인 날려버리기..
                alien_y_pos = -2000
        if game_elapsed_time >= 40 and game_elapsed_time<=48 and not blackhole_appeared:   #블랙홀 생성
            blackhole_appeared = True 
            # 안전하게 화면 가장자리 근처 랜덤 위치에 생성 (플레이어 피할 시간 주기)
            side = random.choice(['top', 'bottom', 'left', 'right'])
            blackhole_width = blackhole.get_width() # 100
            blackhole_height = blackhole.get_height() # 100
            margin = 50 # 화면 가장자리에서 얼마나 떨어뜨릴지

            if side == 'top':
                blackhole_x_pos = random.randint(margin, screen_width - blackhole_width - margin)
                blackhole_y_pos = margin # 위쪽 가장자리 근처
            elif side == 'bottom':
                blackhole_x_pos = random.randint(margin, screen_width - blackhole_width - margin)
                blackhole_y_pos = screen_height - blackhole_height - margin # 아래쪽 가장자리 근처
            elif side == 'left':
                blackhole_x_pos = margin # 왼쪽 가장자리 근처
                blackhole_y_pos = random.randint(margin, screen_height - blackhole_height - margin)
            else: # right
                blackhole_x_pos = screen_width - blackhole_width - margin # 오른쪽 가장자리 근처
                blackhole_y_pos = random.randint(margin, screen_height - blackhole_height - margin)

        if is_shield_active:
        # 쉴드 시작 후 5초가 지났으면 쉴드 해제
            if game_elapsed_time - shield_start_time > 5:
                is_shield_active = False

        if blackhole_appeared:
            bh_center_x = blackhole_x_pos + blackhole_radius
            bh_center_y = blackhole_y_pos + blackhole_radius
            sp_center_x = spaceship_x_pos + spaceship_radius
            sp_center_y = spaceship_y_pos + spaceship_radius
            distance = math.sqrt((sp_center_x - bh_center_x)**2 + (sp_center_y - bh_center_y)**2)

            if distance < spaceship_radius + blackhole_radius and running:

                animation_start_time = pygame.time.get_ticks()
                animation_duration = 1500 # 1.5초
                
                start_x, start_y = spaceship_x_pos, spaceship_y_pos
                start_width, start_height = spaceship_width, spaceship_height
                fade_surface = pygame.Surface((screen_width, screen_height))
                fade_surface.fill((0, 0, 0)) 
                
                animating = True
                while animating:
                    elapsed = pygame.time.get_ticks() - animation_start_time
                    progress = min(1.0, elapsed / animation_duration) # 0.0 ~ 1.0
                    ease_progress = progress * progress 
            
                    current_width = int(start_width * (1.0 - ease_progress))
                    current_height = int(start_height * (1.0 - ease_progress))
                    if current_width < 1: current_width = 1
                    if current_height < 1: current_height = 1
                    current_x = start_x + (bh_center_x - (start_x + spaceship_radius)) * ease_progress
                    current_y = start_y + (bh_center_y - (start_y + spaceship_radius)) * ease_progress
                    
                    current_ship_image = spaceship_images[keyborad_rotation]
                    scaled_ship = pygame.transform.scale(current_ship_image, (current_width, current_height))
                    
                    screen.blit(background,(0,0))
                    for meteor in meteors:
                        screen.blit(meteor_images[meteor["img_idx"]], (meteor["pos_x"], meteor["pos_y"]))
                    if alien_appeared:
                        screen.blit(alien, (alien_x_pos, alien_y_pos))
                    screen.blit(blackhole, (blackhole_x_pos, blackhole_y_pos))
                    
                    scaled_rect = scaled_ship.get_rect(center = (current_x + start_width/2, current_y + start_height/2))
                    screen.blit(scaled_ship, scaled_rect)
                    
                    alpha = int(ease_progress * 255) 
                    fade_surface.set_alpha(alpha)
                    screen.blit(fade_surface, (0, 0)) 
                    
                    pygame.display.update()
                    clock.tick(60)
                    
                    if progress >= 1.0:
                        animating = False
            
                white_fade_surface = pygame.Surface((screen_width, screen_height))
                white_fade_surface.fill((255, 255, 255))
                
                fade_in_start_time = pygame.time.get_ticks()
                fade_in_duration = 1000 
                
                fading_in = True
                while fading_in:
                    elapsed = pygame.time.get_ticks() - fade_in_start_time
                    progress = min(1.0, elapsed / fade_in_duration)
                    
                    alpha = int(progress * 255) 
                    white_fade_surface.set_alpha(alpha)
                    
                    screen.fill((0, 0, 0)) 
                    screen.blit(white_fade_surface, (0, 0)) 
                    
                    pygame.display.update()
                    clock.tick(60)
                    
                    if progress >= 1.0:
                        fading_in = False

                
                kkanttapia_rect = kkanttapia.get_rect(center=(screen_width / 2, screen_height / 2))
                screen.blit(kkanttapia, kkanttapia_rect)
                pygame.display.update()
                pygame.time.delay(1500) 

                fade_to_black_start = pygame.time.get_ticks()
                fade_duration = 1000 
                fading_to_black = True
                
                fade_surface = pygame.Surface((screen_width, screen_height))
                fade_surface.fill((0, 0, 0)) 
                
                while fading_to_black:
                    elapsed = pygame.time.get_ticks() - fade_to_black_start
                    progress = min(1.0, elapsed / fade_duration)
                    alpha = int(progress * 255) 
                    
                    screen.blit(kkanttapia, kkanttapia_rect)
                    
                    fade_surface.set_alpha(alpha)
                    screen.blit(fade_surface, (0, 0))
                    
                    pygame.display.update()
                    clock.tick(60)
                    
                    if progress >= 1.0:
                        fading_to_black = False

                move_success_cnt = 0
                
                success_font = pygame.font.Font(os.path.join(font_path, "DungGeunMo.ttf"), 70)
                success_text_surface = success_font.render("깐따삐아에 이주 성공하다!", True, (255, 255, 255))
                
                text_rect = success_text_surface.get_rect(center=(screen_width / 2, screen_height/3 - 100))
                
                while move_success_cnt < 3:
                    for img in move_success_images: 
                        screen.blit(img, (0,0)) 
                        screen.blit(success_text_surface,text_rect)
                        pygame.display.update() 
                        pygame.time.delay(500)
                    
                    move_success_cnt += 1
                

                pygame.time.delay(1500) 
                running = False
        #운석 계속 만들기
        if len(meteors) < max_meteors:
            meteors.append(create_meteor(game_elapsed_time))

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
                    meteors.append(create_meteor(game_elapsed_time)) # 새 운석 생성
            else:
            #쉴드 안켜져있을 때
                #무적 상태면 건너뛰기
                if is_invincible:
                    continue
            # 충돌 판정
                spaceship_center_x = spaceship_x_pos + spaceship_radius
                spaceship_center_y = spaceship_y_pos + spaceship_radius
                meteor_center_x = meteor["pos_x"] + meteor_radius
                meteor_center_y = meteor["pos_y"] + meteor_radius
                distance = math.sqrt((spaceship_center_x - meteor_center_x)**2 + (spaceship_center_y - meteor_center_y)**2)

                if distance < spaceship_radius + meteor_radius: #충돌하면 겜 오버
                    left_life = left_life - 1 
                    meteors.remove(meteor)    # 부딪힌 운석은 일단 제거
                    if left_life==0:
                        collision_rect = meteor_collision.get_rect(center=(screen_width / 2, screen_height / 2))
                        screen.blit(meteor_collision, collision_rect)
                        pygame.display.update() # 화면 업데이트해서 보여주기
                        pygame.time.delay(2000) # 2초 대기

                        game_over_rect = gameover.get_rect(center=(screen_width / 2, screen_height / 2))
                        screen.blit(gameover, game_over_rect)
                        pygame.display.update() # 화면 업데이트해서 보여주기
                        pygame.time.delay(2000) # 2초 대기
                        running = False
                        break
                    else:
                        is_invincible=True
                        invincible_start_time=game_elapsed_time
    if not running:
        break

    screen.blit(background,(0,0))

    if left_life==4:
        screen.blit(life_images[3],(1000,10))
    elif left_life==3:
        screen.blit(life_images[2],(1000,10))
    elif left_life==2:
        screen.blit(life_images[1],(1000,10))
    else:
        screen.blit(life_images[0],(1000,10))

    timer_surface = game_font.render(timer_text_str, True, TIMER_COLOR)
   
    screen.blit(timer_surface, (10, 10))
    for meteor in meteors:
        screen.blit(meteor_images[meteor["img_idx"]], (meteor["pos_x"], meteor["pos_y"]))

    if alien_appeared:
        screen.blit(alien, (alien_x_pos, alien_y_pos))
    if blackhole_appeared:
        screen.blit(blackhole, (blackhole_x_pos, blackhole_y_pos))

    current_spaceship_image = spaceship_images[keyborad_rotation]

    
    if is_invincible:
        if (pygame.time.get_ticks() // 100) % 2 == 0: 
            screen.blit(current_spaceship_image,(spaceship_x_pos,spaceship_y_pos)) 
    else:
        screen.blit(current_spaceship_image,(spaceship_x_pos,spaceship_y_pos))
    
    if is_shield_active:
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