import random
import pygame


# --------------------------------------------
# 압력 미세 변화
# --------------------------------------------
def update_pressure_small(pressure, stage3):
    change = random.uniform(
        stage3.MIN_RANDOM_CHANGE,
        stage3.MAX_RANDOM_CHANGE
    )

    if random.choice([True, False]):
        pressure += change
    else:
        pressure -= change

    return max(0.0, min(100.0, pressure))


# --------------------------------------------
# 압력 급변
# --------------------------------------------
def update_pressure_spike(pressure, stage3):
    spike_change = random.uniform(
        stage3.MIN_SPIKE_CHANGE,
        stage3.MAX_SPIKE_CHANGE
    )

    if random.choice([True, False]):
        pressure += spike_change
    else:
        pressure -= spike_change

    return max(0.0, min(100.0, pressure))


# --------------------------------------------
# <-,-> 키로 압력 조절
# --------------------------------------------
def user_pressure_control(pressure, key_pressed, stage3):
    keys = pygame.key.get_pressed()

    amount = stage3.PRESSURE_CONTROL_AMOUNT

    if not key_pressed:
        if keys[pygame.K_q]:
            pressure = min(100.0, pressure + amount)
            key_pressed = True
        elif keys[pygame.K_w]:
            pressure = max(0.0, pressure - amount)
            key_pressed = True
    else:
        if not (keys[pygame.K_q] or keys[pygame.K_w]):
            key_pressed = False

    return pressure, key_pressed
