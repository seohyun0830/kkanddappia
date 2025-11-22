import pygame
import os
def collision_ending(screen, meteor_collision, gameover, explosion_sound):
    pygame.mixer.music.pause()
    explosion_sound.play()
    collision_rect = meteor_collision.get_rect(center=(1200 / 2, 800 / 2))
    screen.blit(meteor_collision, collision_rect)
    pygame.display.update() 
    pygame.time.delay(1500)

    game_over_rect = gameover.get_rect(center=(1200 / 2, 800 / 2))
    screen.blit(gameover, game_over_rect)
    pygame.display.update() 
    pygame.time.delay(1500) 
