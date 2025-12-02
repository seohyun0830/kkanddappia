import random
import pygame
from engine import constants


"""
압력 미세 변화
0.2초마다 1~3 범위에서 랜덤 증가, 감소
"""
def update_pressure_small(pressure):
    change = random.uniform(constants.MIN_RANDOM_CHANGE,
                            constants.MAX_RANDOM_CHANGE)

    # True면 증가, False면 감소
    if random.choice([True, False]):
        pressure += change
    else:
        pressure -= change

    # 범위 제한
    pressure = max(0.0, min(100.0, pressure))
    return pressure

"""
압력 급변
초 랜덤 간격 10~30 강한 압력 변화 발생
"""
def update_pressure_spike(pressure):
    spike_change = random.uniform(constants.MIN_SPIKE_CHANGE,
                                  constants.MAX_SPIKE_CHANGE)

    if random.choice([True, False]):
        pressure += spike_change
    else:
        pressure -= spike_change

    pressure = max(0.0, min(100.0, pressure))

    return pressure

#Q/W키에 의한 압력 조절
def user_pressure_control(pressure, key_pressed, n=3):
    keys = pygame.key.get_pressed()

    # 키가 막 눌린 순간만 감지
    if not key_pressed:
        if keys[pygame.K_q]:
            pressure = min(100.0, pressure + n)
            key_pressed = True
        elif keys[pygame.K_w]:
            pressure = max(0.0, pressure - n)
            key_pressed = True

    # 키에서 손을 뗀 순간 감지 → 다시 입력 가능
    else:
        if not (keys[pygame.K_q] or keys[pygame.K_w]):
            key_pressed = False

    return pressure, key_pressed
