import pygame
import os

SCREEN_WIDTH=1200
SCREEN_HEIGHT=800

BLACK=(0,0,0)
WHITE=(255,255,255)

pygame.init()
pygame.display.set_caption("KKANDDAPPIA!")

screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock=pygame.time.Clock()

current_path=os.path.dirname(__file__)
assets_path=os.path.join(current_path, 'kkanddabbia')

background_image=pygame.image.load(os.path.join(assets_path, 'inside.jpg'))
background_image=pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

origin_person_image=pygame.image.load(os.path.join(assets_path, 'dino.png'))
origin_person_image=pygame.transform.scale(origin_person_image, (250,250))

flip_person_image=pygame.transform.flip(origin_person_image, True, False)
person_image=flip_person_image

make_image=pygame.image.load(os.path.join(assets_path, 'make.png'))
make_image=pygame.transform.scale(make_image, (600,600))

make_image_x=(SCREEN_WIDTH-make_image.get_width())//2
make_image_y=(SCREEN_HEIGHT-make_image.get_height())//2

person_x=100
person_y=550
person_speed=5
person_direction_right=False

open_door=False
close_door=True


done=False

CLICK_AREA=pygame.Rect(900,400, 250,300)

while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True

        if event.type==pygame.MOUSEBUTTONDOWN:
            mouse_pos=pygame.mouse.get_pos()

            if CLICK_AREA.collidepoint(mouse_pos):
                open_door=not open_door

            if (not CLICK_AREA.collidepoint(mouse_pos))and (open_door==True):
                open_door=not open_door
    
    keys=pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        person_x-=person_speed
        if person_direction_right:
            person_image=origin_person_image
            person_direction_right=False

    if keys[pygame.K_RIGHT]:
        person_x+=person_speed
        if not person_direction_right:
            person_image=flip_person_image
            person_direction_right=True

    if person_x<0:
        person_x=0
    elif person_x>SCREEN_WIDTH-person_image.get_width():
        person_x=SCREEN_WIDTH-person_image.get_width()

    
    
    screen.blit(background_image, (0,0))
    screen.blit(person_image, (person_x, person_y))

    if open_door:
        screen.blit(make_image, (make_image_x, make_image_y))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
