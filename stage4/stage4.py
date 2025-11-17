import pygame
import os
import random
import math
import ui
import meteor_util
from puzzle import puzzle_main
pygame.init()
pygame.mixer.init()

screen_width=1200
screen_height=800
screen=pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("Kkanttappia")

clock = pygame.time.Clock()
 
current_path = os.path.dirname(__file__)    #현재 파일 위치 반환
image_path = os.path.join(current_path,"images")    # images 폴더 위치 반환
audio_path=os.path.join(current_path,"audios")    

rotate_sound=pygame.mixer.Sound(os.path.join(audio_path,"rotate.mp3"))
background_music=pygame.mixer.music.load(os.path.join(audio_path, "cosmic_zoo.mp3"))
defect_sound=pygame.mixer.Sound(os.path.join(audio_path,"machine_call.mp3"))
collision_sound=pygame.mixer.Sound(os.path.join(audio_path,"collision.mp3"))
bubble_collision_sound=pygame.mixer.Sound(os.path.join(audio_path,"bubble_collision.mp3"))
to_blackhole_sound=pygame.mixer.Sound(os.path.join(audio_path,"to_blackhole.mp3"))
landed_sound=pygame.mixer.Sound(os.path.join(audio_path,"landed.mp3"))
alien_sound=pygame.mixer.Sound(os.path.join(audio_path,"contact_alien.mp3"))
explosion_sound=pygame.mixer.Sound(os.path.join(audio_path,"explosion.mp3"))


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

#네비게이션
navigation_screen=pygame.image.load(os.path.join(image_path,"navigation_screen.png"))
navi=pygame.image.load(os.path.join(image_path,"spaceship_navi.png"))
navigation_movement=ui.navigation(navi)

fuelgauge=pygame.image.load(os.path.join(image_path, "fuelgauge.png")) #일단 눈대중으로.. 각도 맞춰놓긴 햇는데 계산해야할 듯
fuel_gauge=ui.fuelgauge(0,660,fuelgauge)

left_fuel=80   #일단 80
last_fuel_drop_time = 0 # 마지막으로 연료 깎인 시간

fuelindicator_img=pygame.image.load(os.path.join(image_path, "fuel_indicator.png")) 
fuel_Indicator=ui.fuel_indicator(78,760,fuelindicator_img,left_fuel,100)

alien = pygame.transform.scale(alien, (60, 100))
alien_radius = 100 / 2 * 0.8
alien_x_pos = 0 
alien_y_pos = 0
alien_appeared = False # 외계인이 한 번만 나타나게 할 변수

bubble = pygame.transform.scale(bubble, (120, 120)) # 우주선보다 살짝 크게
is_shield_active = False # 쉴드가 활성화됐는지 알려주는 변수
shield_start_time = 0 # 쉴드가 언제 시작됐는지 기록할 변수

blackhole= pygame.transform.scale(blackhole, (120, 120)) # 블랙홀 크기 조절
blackhole_radius = 120 / 2 * 0.4 # 충돌 판정 범위 (살짝 작게)
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

meteor_util.Meteor.images=meteor_images

meteors=[]
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

#1200x800

start_ticks = pygame.time.get_ticks()


is_defect_event = False     #결함 체크할 변수
was_defect_paused = False 
pause_start_ticks = 0     
total_paused_ms = 0       
font_path = os.path.join(current_path, "font")
game_font = pygame.font.Font(os.path.join(font_path, "DungGeunMo.ttf"), 40)
fuel_font = pygame.font.Font(os.path.join(font_path, "DungGeunMo.ttf"), 30)
TOTAL_GAME_TIME = 100 
TIMER_COLOR = (200, 200, 200) 
pygame.mixer.music.play(-1)

#메인 게임 루프
running = True
while running:
    dt=clock.tick(60)

    current_ticks = pygame.time.get_ticks() # 현재 실제 시간
    real_elapsed_time = (current_ticks - start_ticks) / 1000.0
    game_elapsed_ms = current_ticks - start_ticks - total_paused_ms
    game_elapsed_time = game_elapsed_ms / 1000.0 # 초 단위
    if not is_defect_event and game_elapsed_time - last_fuel_drop_time > 2:
        if left_fuel > 0:
            left_fuel -= 1
        last_fuel_drop_time = game_elapsed_time

    if 20 <= game_elapsed_time < 20.1 and not is_defect_event:  #결함 발생
        is_defect_event = True
        pygame.mixer.music.pause()
        defect_sound.play(loops=-1)
        spaceship_to_x = 0
        spaceship_to_y = 0
        if not was_defect_paused:
           pause_start_ticks = current_ticks
        was_defect_paused = True

    remaining_seconds = max(0, TOTAL_GAME_TIME - game_elapsed_time)  #남은 시간
    minutes = int(remaining_seconds // 60)
    seconds = int(remaining_seconds % 60)
    timer_text_str = f"{minutes:02}:{seconds:02}"
    
 
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False 
        if is_defect_event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB: 
                    screen.blit(warning_img2, (0,0))
                    pygame.display.update()
                    defect_sound.stop()
                    puzzle_start_tick = pygame.time.get_ticks()
                    result = puzzle_main.f_puzzle(screen) 
                    
                    if result!=1:
                       running=False

                    # 정지 시간 보정
                    puzzle_end_tick = pygame.time.get_ticks()
                    total_paused_ms += (puzzle_end_tick - pause_start_ticks)
                    game_elapsed_ms = current_ticks - start_ticks - total_paused_ms
                    game_elapsed_time = game_elapsed_ms / 1000.0 # 초 단위
                    is_defect_event = False
                    was_defect_paused = False
                    
                    remaining_seconds = max(0, TOTAL_GAME_TIME - game_elapsed_time)  #남은 시간

                # 1초 대기 후 게임 다시
                    pygame.time.delay(1000)
                    pygame.mixer.music.unpause()
        else: #결함 없을 때 키보드 먹도록..(운석 충돌 때문에 일단 이렇게 둠)
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

    remaining_seconds = max(0, TOTAL_GAME_TIME - game_elapsed_time)  #남은 시간

    if not is_defect_event: #이것도 결함 아닐 때
        if game_elapsed_time >= next_rotation:
            keyborad_rotation = (keyborad_rotation + 1) % 4 # 4가지 로테이션
            rotate_sound.play()
            next_rotation += 25.0 
            spaceship_to_y=0
            spaceship_to_x=0
        if remaining_seconds>=84:
            navigation_movement.update(1)
        elif remaining_seconds>=68:
            navigation_movement.update(2)
        elif remaining_seconds>=52:
                navigation_movement.update(3)
        elif remaining_seconds>=36:
            navigation_movement.update(4)
        elif remaining_seconds>=20:
                navigation_movement.update(5)
        elif remaining_seconds>=0:
                navigation_movement.update(6)

        
        navigation_movement.draw(screen)    #왜 근데 여기에 넣는데 안그려지는 거지?
        #무적 시간 끝났나
        if is_invincible and game_elapsed_time - invincible_start_time > 2: # 2초간 무적
            is_invincible = False
        
        # 운석 생성
        if game_elapsed_time < 5: #5초 이하일 때는 3개만 만들고
            max_meteors = 3 
        else: max_meteors = 10 #이후에는 10개씩

        if game_elapsed_time > 30 and game_elapsed_time<38 and not alien_appeared:    #30초 넘으면 외계인 나오게
            alien_appeared = True 

            # 화면 중앙 위쪽에서 등장  (일단은....)
            alien_x_pos = screen_width / 2 - alien.get_width() / 2
            alien_y_pos = 100
        if game_elapsed_time >35:    #30초 넘으면 외계인 나오게
            alien_appeared = False 

        if alien_appeared and not is_shield_active: #쉴드 받기 전
        # 충돌 계산
            alien_center_x = alien_x_pos + alien_radius
            alien_center_y = alien_y_pos + alien_radius
            spaceship_center_x = spaceship_x_pos + spaceship_radius
            spaceship_center_y = spaceship_y_pos + spaceship_radius
            distance = math.sqrt((spaceship_center_x - alien_center_x)**2 + (spaceship_center_y - alien_center_y)**2)
        
            if distance < spaceship_radius + alien_radius:  #우주선랑 외계인이랑 충돌됐다고 판단되면
                alien_sound.play()
                is_shield_active = True # 쉴드 활성화
                shield_start_time = game_elapsed_time # 쉴드 시작 시간 기록
                alien_x_pos = -2000 #외계인 날려버리기..
                alien_y_pos = -2000
        #
        # navigation_movement.draw(screen)
        ####################
        if game_elapsed_time >= 45 and game_elapsed_time<=55 and not blackhole_appeared:  #블랙홀 생성
            blackhole_appeared = True 
            
            margin_top = 100    
            margin_bottom = 250 
            margin_left = 200    
            margin_right = 250    
            
            blackhole_width = blackhole.get_width() # 120
            blackhole_height = blackhole.get_height() # 120

            safe_x_min = margin_left
            safe_x_max = screen_width - margin_right - blackhole_width
            safe_y_min = margin_top
            safe_y_max = screen_height - margin_bottom - blackhole_height

            side = random.choice(['top', 'bottom', 'left', 'right'])

            if side == 'top':
                blackhole_x_pos = random.randint(safe_x_min, safe_x_max)
                blackhole_y_pos = safe_y_min 
            elif side == 'bottom':
                blackhole_x_pos = random.randint(safe_x_min, safe_x_max)
                blackhole_y_pos = safe_y_max
            elif side == 'left':
                blackhole_x_pos = safe_x_min
                blackhole_y_pos = random.randint(safe_y_min, safe_y_max)
            else: 
                blackhole_x_pos = safe_x_max
                blackhole_y_pos = random.randint(safe_y_min, safe_y_max)
        if game_elapsed_time >55  and blackhole_appeared:
            blackhole_appeared=False

        if is_shield_active:
        # 쉴드 시작 후 5초가 지났으면 쉴드 해제
            if game_elapsed_time - shield_start_time > 5:
                is_shield_active = False
        
        #블랙홀 성공화면 
        if blackhole_appeared:
            bh_center_x = blackhole_x_pos + blackhole_radius
            bh_center_y = blackhole_y_pos + blackhole_radius
            sp_center_x = spaceship_x_pos + spaceship_radius
            sp_center_y = spaceship_y_pos + spaceship_radius
            distance = math.sqrt((sp_center_x - bh_center_x)**2 + (sp_center_y - bh_center_y)**2)

            if distance < spaceship_radius + blackhole_radius and running:
                pygame.mixer.music.pause()
                to_blackhole_sound.play()
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
                        meteor.update() 
                        meteor.draw(screen)
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
                landed_sound.play()
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

        # 기본 성공 
        if remaining_seconds <= 0 and running:
            
            fade_surface = pygame.Surface((screen_width, screen_height))
            fade_surface.fill((0, 0, 0)) # 검은색
            
            fade_start = pygame.time.get_ticks()
            fade_duration = 1000 
            pygame.mixer.music.pause()
            
            while True:
                elapsed = pygame.time.get_ticks() - fade_start
                if elapsed >= fade_duration:
                    break
                    
                progress = elapsed / fade_duration
                alpha = int(progress * 255) 
                
                fade_surface.set_alpha(alpha)
                screen.blit(fade_surface, (0, 0))
                pygame.display.update()
                clock.tick(60)
                
            pygame.time.delay(1000) 
            landed_sound.play()
            kkanttapia_rect = kkanttapia.get_rect(center=(screen_width / 2, screen_height / 2))
            
            fade_start = pygame.time.get_ticks()
            fade_duration = 1500 #
            
            while True:
                elapsed = pygame.time.get_ticks() - fade_start
                if elapsed >= fade_duration:
                    break
                
                progress = elapsed / fade_duration
                alpha = int(255 - (progress * 255)) 
                
                screen.blit(kkanttapia, kkanttapia_rect)
                fade_surface.set_alpha(alpha)
                screen.blit(fade_surface, (0, 0))
                
                pygame.display.update()
                clock.tick(60)
            move_success_cnt = 0
            
            success_font = pygame.font.Font(os.path.join(font_path, "DungGeunMo.ttf"), 70)
            success_text_surface = success_font.render("깐따삐아에 이주 성공하다!", True, (255, 255, 255))
            text_rect = success_text_surface.get_rect(center=(screen_width / 2, screen_height/3 - 100))
            
            while move_success_cnt < 3:
                for img in move_success_images: 
                    screen.blit(kkanttapia, kkanttapia_rect) 
                    screen.blit(img, (0,0)) 
                    screen.blit(success_text_surface, text_rect)
                    
                    pygame.display.update() 
                    pygame.time.delay(500) 
                
                move_success_cnt += 1

            pygame.time.delay(1500) 
            running = False


        #운석 계속 만들기
        if len(meteors) < max_meteors:
            meteors.append(meteor_util.Meteor(game_elapsed_time, screen_width, screen_height))

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
            meteor.update()
            if meteor.is_off_screen(screen_width,screen_height):
                meteors.remove(meteor)
                continue
            if is_shield_active:
            # 쉴드가 켜져 있을 때 운석과 부딪히면 운석만 파괴
                shield_center_x = spaceship_x_pos + spaceship_radius # 쉴드 중심 우주선과 같도록 설졍..
                shield_center_y = spaceship_y_pos + spaceship_radius
                meteor_center_x = meteor.center_x 
                meteor_center_y = meteor.center_y
                distance = math.sqrt((shield_center_x - meteor_center_x)**2 + (shield_center_y - meteor_center_y)**2)
                
                if distance < spaceship_radius + meteor_radius: #우주선이랑 충돌했는지
                    bubble_collision_sound.play()
                    meteors.remove(meteor) # 부딪힌 운석 제거
                    meteors.append(meteor_util.Meteor(game_elapsed_time, screen_width, screen_height))
            else:
            #쉴드 안켜져있을 때
                #무적 상태면 건너뛰기
                if is_invincible:
                    continue
            # 충돌 판정
                spaceship_center_x = spaceship_x_pos + spaceship_radius
                spaceship_center_y = spaceship_y_pos + spaceship_radius
                meteor_center_x = meteor.center_x
                meteor_center_y = meteor.center_y
                distance = math.sqrt((spaceship_center_x - meteor_center_x)**2 + (spaceship_center_y - meteor_center_y)**2)

                if distance < spaceship_radius + meteor_radius: #충돌하면 겜 오버
                    left_life = left_life - 1 
                    meteors.remove(meteor)    # 부딪힌 운석은 일단 제거
                    if left_life==0:
                        pygame.mixer.music.pause()
                        explosion_sound.play()
                        collision_rect = meteor_collision.get_rect(center=(screen_width / 2, screen_height / 2))
                        screen.blit(meteor_collision, collision_rect)
                        pygame.display.update() # 화면 업데이트해서 보여주기
                        pygame.time.delay(1500) # 2초 대기

                        game_over_rect = gameover.get_rect(center=(screen_width / 2, screen_height / 2))
                        screen.blit(gameover, game_over_rect)
                        pygame.display.update() # 화면 업데이트해서 보여주기
                        pygame.time.delay(1500) # 2초 대기
                        running = False
                        break
                    else:
                        is_invincible=True
                        collision_sound.play()
                        invincible_start_time=game_elapsed_time
    if not running:
        break

    screen.blit(background,(0,0))
    fuel_text_str = f"{left_fuel}%"
    fuel_surface = fuel_font.render(fuel_text_str, True, (255, 255, 255))
    fuel_rect = fuel_surface.get_rect(center=(80, 650)) 
    screen.blit(fuel_surface, fuel_rect)
    fuel_gauge.draw(screen)
    fuel_Indicator.update(left_fuel)
    fuel_Indicator.draw(screen)

    screen.blit(navigation_screen,(950,550))
    navigation_movement.draw(screen)

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
        meteor.draw(screen)

    if alien_appeared:
        screen.blit(alien, (alien_x_pos, alien_y_pos))
    if blackhole_appeared:
        screen.blit(blackhole, (blackhole_x_pos, blackhole_y_pos))

    current_spaceship_image = spaceship_images[keyborad_rotation]

    #무적
    if is_invincible:
        if (pygame.time.get_ticks() // 100) % 2 == 0: 
            screen.blit(current_spaceship_image,(spaceship_x_pos,spaceship_y_pos)) 
    else:
        screen.blit(current_spaceship_image,(spaceship_x_pos,spaceship_y_pos))
    #쉴드
    
    if is_shield_active:
        bubble_rect = bubble.get_rect(center = (spaceship_x_pos + spaceship_width/2, spaceship_y_pos + spaceship_height/2))
        screen.blit(bubble, bubble_rect)

    defect_font = pygame.font.Font(os.path.join(font_path, "DungGeunMo.ttf"), 60)
    defect_text_surface = defect_font.render("TAB 키를 눌러 우주선을 수리하십시오!", True, (255, 255, 255))
    text_rect = defect_text_surface.get_rect(center=(screen_width / 2, screen_height/2+20))
    
    if is_defect_event: 
        flicker_value = (pygame.time.get_ticks() // 200) % 2 
        if flicker_value == 0:
            screen.blit(warning_img1, (0,0))
        else: 
            screen.blit(warning_img2, (0,0))
        
        screen.blit(defect_text_surface,text_rect)
  
    
    pygame.display.update()

pygame.quit()