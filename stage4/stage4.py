import pygame
import os
import random
import math
from . import restart_ani
from . import guide
from . import crash_ani
from . import ui
from . import meteor_util
from . import Alien
from . import Bubble
from . import Blackhole
from . import Spaceship
from . import Success_animation
from . import collision_ending
from .puzzle import puzzle_main
from engine.fuel_manager import fuel_manager


class Stage4:
    def __init__(self, screen,mode):
        self.screen = screen
        self.clock = pygame.time.Clock()

        # --- pause / resume 관련 ---
        # total_paused_ms : 퍼즐 + 4to3에 있던 시간까지 모두 포함한 "멈춘 시간" 누적
        self.total_paused_ms = 0
        self.stage4to3_pause_start = 0  # 4→3 넘어갈 때 기준 시간
        self.pause_start_ticks = 0      # 퍼즐(결함)용 기준 시간

        # 기본 설정
        self.screen_width = 1200
        self.screen_height = 800

        if mode=="easy":
            self.rotation_cnt=2
        elif mode=="hard":
            self.rotation_cnt=1
        current_path = os.path.dirname(__file__)
        self.image_path = os.path.join(current_path, "images")
        self.audio_path = os.path.join(current_path, "audios")
        self.font_path = os.path.join(current_path, "font")

        # 시간 관련 (run()에서 start_ticks 세팅)
        self.start_ticks = None
        self.last_fuel_drop_time = 0
        self.TOTAL_GAME_TIME = 100

        # 상태 변수들
        self.left_life = 4
        self.invincible_start_time = 0

        self.next_rotation = 25.0  # 자동 회전 타이밍

        # defect event
        self.is_defect_event = False
        self.was_defect_paused = False

        # 보조 이벤트
        self.is_shield_active = False
        self.shield_start_time = 0
        self.blackhole_appeared = False
        self.alien_once = False

        # 이미지 / 사운드 / UI 로드
        self.load_images()
        self.load_sounds()
        
        self.fule_stage4to3=False
        # UI
        self.navigation = ui.navigation(self.navi)
        self.fuelGauge = ui.fuelgauge(0, 660, self.fuelgauge_img)
        self.fuelIndicator = ui.fuel_indicator(
            78, 760, self.fuelindicator_img, fuel_manager.fuel, fuel_manager.max_fuel
        )

        # 객체 생성
        self.spaceship = Spaceship.Spaceship(self.spaceship_img_paths)
        self.bubble = Bubble.Bubble(self.bubble_img)
        self.alien = Alien.Alien(self.alien_img)
        self.blackhole = Blackhole.Blackhole(self.blackhole_img)

        # 운석들
        meteor_util.Meteor.images = self.meteor_images
        self.meteors = []

        # 폰트
        self.game_font = pygame.font.Font(os.path.join(self.font_path, "DungGeunMo.ttf"), 40)
        self.fuel_font = pygame.font.Font(os.path.join(self.font_path, "DungGeunMo.ttf"), 30)
        self.talk_font = pygame.font.Font(os.path.join(self.font_path, "DungGeunMo.ttf"), 25)
        pygame.mixer.music.play(-1)

    # ------------------------------------------------------------------
    #  처음 Stage4 들어올 때 한 번만 호출
    # ------------------------------------------------------------------
    def run(self):
        
        guide.show_guide(self.screen, self.guide_bk_img, self.game_font)
        self.start_ticks = pygame.time.get_ticks()
        self.total_paused_ms = 0 
        
        return self._loop()
    # ------------------------------------------------------------------
    #  Stage4To3 갔다가 돌아올 때 호출 (이어달리기)
    # ------------------------------------------------------------------
    def resume(self):
        now = pygame.time.get_ticks()
        if self.stage4to3_pause_start > 0:
            self.total_paused_ms += (now - self.stage4to3_pause_start)

        pygame.mixer.music.load(os.path.join(self.audio_path, "cosmic_zoo.mp3"))
        pygame.mixer.music.play(-1)
        self.spaceship.to_x = 0
        self.spaceship.to_y = 0
        return self._loop()

    def _loop(self):
       
        running = True
        while running:
            dt = self.clock.tick(60)
            current_ticks = pygame.time.get_ticks()

            # 시간 계산 (퍼즐 + 4to3 모두 멈춘 시간 보정)
            game_elapsed_ms = current_ticks - self.start_ticks - self.total_paused_ms
            game_elapsed_time = game_elapsed_ms / 1000.0
            self.game_elapsed_time = game_elapsed_time

            # 연료 부족 → stage4to3 이동
            if fuel_manager.fuel < 50 and self.fule_stage4to3==False:  # 테스트용 기준

                pygame.mixer.music.pause()
                self.screen.blit(self.fuel_failure_img, (0, 0))
                #410,300
                fuel_text = self.game_font.render("연료를 충전하십시오!", True, (255, 0, 0))
                self.screen.blit(fuel_text,(410,300))
                pygame.display.update()
                pygame.time.delay(2500)

                # 4→3에 들어가는 시점 기록 (돌아와서 resume()에서 사용)
                self.stage4to3_pause_start = pygame.time.get_ticks()
                self.fule_stage4to3=True
                return "stage4to3"
            ####연료 부족
            if fuel_manager.fuel < 50 and self.fule_stage4to3==True:    #이미 3갔다왔으면
                sounds_to_play={'fuel_empty':self.fuel_empty_sound,
                                    'siren':self.siren_sound}
                crash_ani.fuel_empty_ani(self.screen,self.fuel_empty_img,sounds_to_play)
                crash_sounds={
                            'ground_crash':self.crash_ground_sound,
                            'burning':self.burnning_sound
                        }
                crash_ani.crash_animation(self.screen,self.crash_fail_images,crash_sounds)
                restart_ani.restart_ani(self.screen,self.crash_fail_images[9],self.crash_after_person_images,self.crash_stand_p_img)
                restart_ani.restart_talk(self.screen,self.talking_box)
                pygame.display.update()
                pygame.time.delay(1500)
                return "fule_empty"   #이건 아예 재시작으로 바꿔야됨 23합치고

            # 연료 감소 (2초마다, defect 아닐 때만)
            if (not self.is_defect_event) and (game_elapsed_time - self.last_fuel_drop_time > 2):
                fuel_manager.consume_fuel(1)
                self.last_fuel_drop_time = game_elapsed_time

            # defect event 발동
            if 20 <= game_elapsed_time < 20.1 and not self.is_defect_event:
                self.start_defect_event(current_ticks)

            # 타이머 계산
            remaining_seconds = max(0, self.TOTAL_GAME_TIME - game_elapsed_time)
            timer_str = f"{int(remaining_seconds // 60):02}:{int(remaining_seconds % 60):02}"

            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "end"

                if self.is_defect_event:
                    res = self.handle_defect_input(event)
                    if res == "menu":
                        return "menu"
                    elif res== "dead":
                        return "dead"
                else:
                    self.spaceship.hard_handle_input(event)

            # defect 아닐 때만 게임 로직 진행
            if not self.is_defect_event:
                logic_result = self.update_game_logic()

                # 블랙홀 성공
                if logic_result == "blackhole_success":
                    return "success"

                # 죽었을 때
                if logic_result == "dead":
                    return "dead"

                # 남은 시간 0초 → 기본 성공
                if remaining_seconds <= 0:
                    self.default_success()
                    return "success"

            # 그리기
            self.render(timer_str)
            pygame.display.update()

        return "end"

    # ------------------------------------------------------------------

    def load_images(self):
        self.background = pygame.image.load(os.path.join(self.image_path, "background_color.png"))
        self.gameover_img = pygame.image.load(os.path.join(self.image_path, "gameover.png"))
        self.warning_img1 = pygame.image.load(os.path.join(self.image_path, "warning1.png"))
        self.warning_img2 = pygame.image.load(os.path.join(self.image_path, "warning2.png"))
        self.alien_img = pygame.image.load(os.path.join(self.image_path, "alien.png"))
        self.bubble_img = pygame.image.load(os.path.join(self.image_path, "bubble.png"))
        self.blackhole_img = pygame.image.load(os.path.join(self.image_path, "blackhole.png"))
        self.success_img = pygame.image.load(os.path.join(self.image_path, "success.png"))
        #self.kkanttapia_img = pygame.image.load(os.path.join(self.image_path, "kkanttapia.png"))

        self.meteor_collision = pygame.transform.scale(
            pygame.image.load(os.path.join(self.image_path, "meteor_collision.png")),
            (1200, 800)
        )

        self.puzzle_fail = pygame.image.load(os.path.join(self.image_path, "puzzle_failure.png"))
        
        self.fuel_failure_img = pygame.image.load(os.path.join(self.image_path, "fuel_failure.png"))

        self.navigation_screen = pygame.image.load(os.path.join(self.image_path, "navigation_screen.png"))
        self.navi = pygame.image.load(os.path.join(self.image_path, "spaceship_navi.png"))

        self.fuelgauge_img = pygame.image.load(os.path.join(self.image_path, "fuelgauge.png"))
        self.fuelindicator_img = pygame.image.load(os.path.join(self.image_path, "fuel_indicator.png"))

        self.sp_meteor_crash_img=pygame.image.load(os.path.join(self.image_path, "spaceship_meteor_crash.png"))
        self.crash_fail_images=[
            pygame.image.load(os.path.join(self.image_path,"crash1.png")), 
            pygame.image.load(os.path.join(self.image_path,"crash2.png")), 
            pygame.image.load(os.path.join(self.image_path,"crash3.png")), 
            pygame.image.load(os.path.join(self.image_path,"crash4.png")), 
            pygame.image.load(os.path.join(self.image_path,"crash5.png")), 
            pygame.image.load(os.path.join(self.image_path,"crash6.png")), 
            pygame.image.load(os.path.join(self.image_path,"crash7.png")), 
            pygame.image.load(os.path.join(self.image_path,"crash8.png")), 
            pygame.image.load(os.path.join(self.image_path,"crash9.png")),
            pygame.image.load(os.path.join(self.image_path,"crash10.png")) ]
        self.crash_after_person_images=[
            
            pygame.image.load(os.path.join(self.image_path,"crash_person2.png")),
            pygame.image.load(os.path.join(self.image_path,"crash_person1.png")),
            pygame.image.load(os.path.join(self.image_path,"crash_person3.png")),
            pygame.image.load(os.path.join(self.image_path,"crash_person1.png"))

        ]
        self.crash_stand_p_img= pygame.image.load(os.path.join(self.image_path,"crash_stand_person.png"))
        self.move_success_p=pygame.image.load(os.path.join(self.image_path,"move_success_p.png"))
        self.talking_box=pygame.image.load(os.path.join(self.image_path,"talking.png"))
        self.talking_box2=pygame.image.load(os.path.join(self.image_path,"talking2.png"))
        self.guide_bk_img=pygame.image.load(os.path.join(self.image_path,"guide_background.png"))
        self.fuel_empty_img=pygame.image.load(os.path.join(self.image_path,"fuel_empty_alarm.png"))
        # life 이미지 (life1 ~ life4)
        self.life_images = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(self.image_path, f"life{i}.png")), (200, 40)
            )
            for i in range(1, 5)
        ]
        #최종 성공 이미지
        self.ending_bk_images=[
            pygame.image.load(os.path.join(self.image_path,"ending_bk1.png")),
            pygame.image.load(os.path.join(self.image_path,"ending_bk2.png")),
            pygame.image.load(os.path.join(self.image_path,"ending_bk3.png")),
            pygame.image.load(os.path.join(self.image_path,"ending_bk4.png"))
        ]

        self.walking_p=pygame.image.load(os.path.join(self.image_path,"walking_p1.png"))

        # 성공 UI 이미지
        '''
        self.move_success_images = [
            pygame.image.load(os.path.join(self.image_path, f"move_success{i}.png"))
            for i in range(1, 5)
        ]
'''
        # 운석 이미지 로드
        meteor_size = 70
        meteor_list = ["meteor.png", "meteor2.png", "meteor3.png", "meteor4.png"]
        self.meteor_images = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(self.image_path, fn)),
                (meteor_size, meteor_size)
            )
            for fn in meteor_list
        ]

        # 우주선 이미지 방향별
        self.spaceship_img_paths = [
            os.path.join(self.image_path, f"spaceship_{i}.png")
            for i in (0, 90, 180, 270)
        ]

    # ------------------------------------------------------------------

    def load_sounds(self):
        self.rotate_sound = pygame.mixer.Sound(os.path.join(self.audio_path, "rotate.mp3"))
        pygame.mixer.music.load(os.path.join(self.audio_path, "cosmic_zoo.mp3"))
        self.defect_sound = pygame.mixer.Sound(os.path.join(self.audio_path, "machine_call.mp3"))
        self.collision_sound = pygame.mixer.Sound(os.path.join(self.audio_path, "collision.mp3"))
        self.bubble_collision_sound = pygame.mixer.Sound(os.path.join(self.audio_path, "bubble_collision.mp3"))
        self.to_blackhole_sound = pygame.mixer.Sound(os.path.join(self.audio_path, "to_blackhole.mp3"))
        self.landed_sound = pygame.mixer.Sound(os.path.join(self.audio_path, "landed.mp3"))
        self.alien_sound = pygame.mixer.Sound(os.path.join(self.audio_path, "contact_alien.mp3"))
        self.explosion_sound = pygame.mixer.Sound(os.path.join(self.audio_path, "explosion.mp3"))
        self.siren_sound=pygame.mixer.Sound(os.path.join(self.audio_path, "siren.mp3"))
        self.burnning_sound=pygame.mixer.Sound(os.path.join(self.audio_path, "burning.mp3"))
        self.crash_ground_sound=pygame.mixer.Sound(os.path.join(self.audio_path, "crash_ground.mp3"))
        self.external_failure_sound=pygame.mixer.Sound(os.path.join(self.audio_path, "external_failure.mp3"))
        self.inner_system_sound=pygame.mixer.Sound(os.path.join(self.audio_path, "inner_system.mp3"))
        self.inner_system_sound.set_volume(1.0)
        self.fuel_empty_sound=pygame.mixer.Sound(os.path.join(self.audio_path, "fuel_empty.mp3"))
    # ------------------------------------------------------------------

    def start_defect_event(self, current_ticks):
        self.is_defect_event = True
        pygame.mixer.music.pause()
        self.defect_sound.play(loops=-1)
        self.spaceship.to_x = 0
        self.spaceship.to_y = 0

        if not self.was_defect_paused:
            self.pause_start_ticks = current_ticks
        self.was_defect_paused = True

    # ------------------------------------------------------------------

    def handle_defect_input(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            self.screen.blit(self.warning_img2, (0, 0))
            pygame.display.update()
            self.defect_sound.stop()

            puzzle_start = pygame.time.get_ticks()
            result = puzzle_main.f_puzzle(self.screen)

            if result == -1:    #퍼즐 실패
                self.inner_system_sound.play()
                self.screen.blit(self.puzzle_fail, (0, 0))
                crash_ani.inner_fail_ani(self.screen,self.puzzle_fail)
                crash_sounds={
                            'ground_crash':self.crash_ground_sound,
                            'burning':self.burnning_sound
                        }
                crash_ani.crash_animation(self.screen,self.crash_fail_images,crash_sounds)
                restart_ani.restart_ani(self.screen,self.crash_fail_images[9],self.crash_after_person_images,self.crash_stand_p_img)
                restart_ani.restart_talk(self.screen,self.talking_box)
                
                return "dead"

            puzzle_end = pygame.time.get_ticks()
            # 퍼즐 하는 동안 흐른 시간은 전부 total_paused_ms에 더해줌
            self.total_paused_ms += (puzzle_end - self.pause_start_ticks)

            self.is_defect_event = False
            self.was_defect_paused = False

            pygame.time.delay(1000)
            pygame.mixer.music.unpause()

        return None

    # ------------------------------------------------------------------

    def update_game_logic(self):
        game_elapsed_time = self.game_elapsed_time

        # 자동 회전
        if game_elapsed_time >= self.next_rotation:
            self.spaceship.idx = (self.spaceship.idx + self.rotation_cnt) % 4
            self.rotate_sound.play()
            self.next_rotation += 25
            self.spaceship.to_x = 0
            self.spaceship.to_y = 0

        # navigation
        sec = self.TOTAL_GAME_TIME - game_elapsed_time
        if sec >= 84: self.navigation.update(1)
        elif sec >= 68: self.navigation.update(2)
        elif sec >= 52: self.navigation.update(3)
        elif sec >= 36: self.navigation.update(4)
        elif sec >= 20: self.navigation.update(5)
        else: self.navigation.update(6)

        # 외계인 등장
        if 25 < game_elapsed_time < 38 and not self.alien_once:
            if not self.alien.is_active:
                self.alien.appearance()
        if game_elapsed_time > 38:
            self.alien.is_active = False

        # 외계인 → 쉴드 충돌
        if self.alien.is_active and not self.is_shield_active:
            if self.alien.detect_collision(
                self.spaceship.center_x, self.spaceship.center_y,
                self.spaceship.radius, True
            ):
                self.alien_sound.play()
                self.is_shield_active = True
                self.alien_once = True
                self.shield_start_time = game_elapsed_time

        # 쉴드 종료
        if self.is_shield_active and (game_elapsed_time - self.shield_start_time > 5):
            self.is_shield_active = False

        # 블랙홀 등장
        if 47 <= game_elapsed_time <= 53 and not self.blackhole_appeared:
            self.blackhole_appeared = True
            for meteor in self.meteors:
                meteor.blackhole_appeared_func()
            self.blackhole.make_blackhole()

        # 블랙홀 흡수 성공 체크
        if self.blackhole_appeared:
            if self.check_blackhole_success():
                return "blackhole_success"

        # 53초 지나면 블랙홀 사라짐
        if game_elapsed_time > 53 and self.blackhole_appeared:
            self.blackhole_appeared = False

        # 운석 생성
        max_meteors = 3 if game_elapsed_time < 5 else 10
        if len(self.meteors) < max_meteors:
            self.meteors.append(
                meteor_util.Meteor(game_elapsed_time, self.screen_width, self.screen_height, self.blackhole_appeared)
            )

        # 운석 업데이트/충돌
        hit_result = self.update_meteors()
        if hit_result == "dead":
            return "dead"

        return None

    # ------------------------------------------------------------------

    def check_blackhole_success(self):
        # 거리 계산 (버그 수정: center_y, center_y → center_x, center_y)
        dist = math.dist(
            (self.spaceship.center_x, self.spaceship.center_y),
            (self.blackhole.center_x, self.blackhole.center_y)
        )

        if dist < self.spaceship.radius + self.blackhole.radius:
            sounds = {"to_blackhole": self.to_blackhole_sound}
            Success_animation.blackhole_ending(
                self.screen, self.background, self.blackhole.image,
                self.spaceship.images[self.spaceship.idx],
                (self.spaceship.x_pos, self.spaceship.y_pos),
                (self.blackhole.x_pos, self.blackhole.y_pos),
                (self.spaceship.width, self.spaceship.height),
                sounds
            )

            sounds = {"landed": self.landed_sound}
            Success_animation.default_ending(
                self.screen, self.ending_bk_images[0], sounds
            )
            Success_animation.kkanddappia_land(self.screen,self.ending_bk_images[1],self.walking_p,self.move_success_p,self.talking_box2,self.talk_font)
            Success_animation.final_ending(self.screen,self.ending_bk_images[2],self.ending_bk_images[3],self.talking_box2,self.talk_font,"easy")
            return True

        return False

    # ------------------------------------------------------------------

    def update_meteors(self):
        game_elapsed_time = self.game_elapsed_time

        for meteor in self.meteors[:]:
            meteor.update()

            if meteor.is_off_screen(self.screen_width, self.screen_height):
                self.meteors.remove(meteor)
                continue

            # 쉴드 켜져 있을 때 → 운석 파괴만
            if self.is_shield_active:
                if meteor.check_collision(
                    self.spaceship.center_x, self.spaceship.center_y, self.spaceship.radius
                ):
                    self.bubble_collision_sound.play()
                    self.meteors.remove(meteor)
                continue

            # 우주선이 자체 무적이면 충돌 무시
            if self.spaceship.is_invincible:
                continue

            # 충돌 처리
            if meteor.check_collision(
                self.spaceship.center_x, self.spaceship.center_y, self.spaceship.radius
            ):
                self.left_life -= 1
                self.meteors.remove(meteor)

                if self.left_life <= 0: #목숨 다 썼을 때
                    sounds_to_play={'external_failure':self.external_failure_sound,
                                    'siren':self.siren_sound}
                    crash_ani.zoom_effect(self.screen,self.sp_meteor_crash_img,sounds_to_play)
                    crash_sounds={
                            'ground_crash':self.crash_ground_sound,
                            'burning':self.burnning_sound
                        }
                    crash_ani.crash_animation(self.screen,self.crash_fail_images,crash_sounds)
                    restart_ani.restart_ani(self.screen,self.crash_fail_images[9],self.crash_after_person_images,self.crash_stand_p_img)
                    restart_ani.restart_talk(self.screen,self.talking_box)
                    pygame.display.update()
                    pygame.time.delay(1500)
                    return "dead"

                self.spaceship.set_invincible(game_elapsed_time)
                self.collision_sound.play()

        return None

    # ------------------------------------------------------------------

    def default_success(self):
        sounds = {"landed": self.landed_sound}
        Success_animation.default_ending(
            self.screen, self.ending_bk_images[0], sounds,
        )
        Success_animation.kkanddappia_land(self.screen,self.ending_bk_images[1],self.walking_p,self.move_success_p,self.talking_box2,self.talk_font)
        Success_animation.final_ending(self.screen,self.ending_bk_images[2],self.ending_bk_images[3],self.talking_box2,self.talk_font,"easy")

    # ------------------------------------------------------------------

    def render(self, timer_text):
        game_elapsed_time = self.game_elapsed_time

        # 배경
        self.screen.blit(self.background, (0, 0))

        # 연료 표시 (fuel_manager.fuel 기준)
        fuel_text = self.fuel_font.render(f"{int(fuel_manager.fuel)}%", True, (255, 255, 255))
        fuel_rect = fuel_text.get_rect(center=(80, 650))
        self.screen.blit(fuel_text, fuel_rect)

        # 연료 UI
        self.fuelGauge.draw(self.screen)
        self.fuelIndicator.update(fuel_manager.fuel)
        self.fuelIndicator.draw(self.screen)

        # navigation
        self.screen.blit(self.navigation_screen, (950, 550))
        self.navigation.draw(self.screen)

        # 우주선
        self.spaceship.check_invincible_end(game_elapsed_time)
        self.spaceship.update()
        self.spaceship.draw(self.screen)

        # life UI (left_life : 4,3,2,1)
        idx = max(0, min(3, self.left_life-1))
        self.screen.blit(self.life_images[idx], (1000, 10))

        # timer 표시
        timer_surface = self.game_font.render(timer_text, True, (200, 200, 200))
        self.screen.blit(timer_surface, (10, 10))

        # 운석
        for meteor in self.meteors:
            meteor.draw(self.screen)

        # 외계인
        if self.alien.is_active:
            self.alien.draw(self.screen)

        # 블랙홀
        if self.blackhole_appeared:
            self.blackhole.draw(self.screen)

        # 쉴드
        if self.is_shield_active:
            self.bubble.draw(
                self.spaceship.x_pos, self.spaceship.y_pos,
                self.spaceship.width, self.spaceship.height,
                self.screen
            )

        # defect event
        if self.is_defect_event:
            self.draw_defect_event()

    # ------------------------------------------------------------------

    def draw_defect_event(self):
        defect_font = pygame.font.Font(os.path.join(self.font_path, "DungGeunMo.ttf"), 60)
        defect_text = defect_font.render("TAB 키를 눌러 우주선을 수리하십시오!", True, (255, 255, 255))

        rect = defect_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 + 20))

        flicker = (pygame.time.get_ticks() // 200) % 2
        if flicker == 0:
            self.screen.blit(self.warning_img1, (0, 0))
        else:
            self.screen.blit(self.warning_img2, (0, 0))

        self.screen.blit(defect_text, rect)