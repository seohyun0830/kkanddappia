import pygame
import os

SCREEN_WIDTH=1200
SCREEN_HEIGHT=800

BLACK=(0,0,0)
WHITE=(255,255,255)

pygame.init()
pygame.display.set_caption("KKANDDABBIA!")

screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock=pygame.time.Clock()

current_path=os.path.dirname(__file__)
assets_path=os.path.join(current_path, 'kkanddabbia')

start_background_image=pygame.image.load(os.path.join(assets_path, 'outside.jpg'))
start_background_image=pygame.transform.scale(start_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

go_to_inside=False

background_image=pygame.image.load(os.path.join(assets_path, 'inside.jpg'))
background_image=pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

origin_person_image=pygame.image.load(os.path.join(assets_path, 'person.png')).convert()
origin_person_image.set_colorkey(WHITE)
origin_person_image=pygame.transform.scale(origin_person_image, (250,250))

flip_person_image=pygame.transform.flip(origin_person_image, True, False)
person_image=origin_person_image

make_image=pygame.image.load(os.path.join(assets_path, 'make.png'))
make_image=pygame.transform.scale(make_image, (600,600))

make_image_x=(SCREEN_WIDTH-make_image.get_width())//2
make_image_y=(SCREEN_HEIGHT-make_image.get_height())//2

person_x=100
person_y=500
person_speed=5
person_direction_right=False

open_door=False

done=False

CLICK_AREA=pygame.Rect(900,400,210,260)
OUTSIDE_DOOR_AREA=pygame.Rect(400,400,400,300)

#################아이템################

ITEM_SIZE=70

inventory=['stone', 'soil', 'wood', 'stick', 'glass', 'window']

item_images={}

stone_image=pygame.image.load(os.path.join(assets_path, 'stone.png')).convert()
stone_image.set_colorkey(WHITE)
item_images['stone']=pygame.transform.scale(stone_image,(ITEM_SIZE, ITEM_SIZE))

soil_image=pygame.image.load(os.path.join(assets_path, 'soil.png')).convert()
soil_image.set_colorkey(WHITE)
item_images['soil']=pygame.transform.scale(soil_image,(ITEM_SIZE, ITEM_SIZE))

wood_image=pygame.image.load(os.path.join(assets_path, 'wood.png')).convert()
wood_image.set_colorkey(WHITE)
item_images['wood']=pygame.transform.scale(wood_image,(ITEM_SIZE, ITEM_SIZE))

stick_image=pygame.image.load(os.path.join(assets_path, 'stick.png')).convert()
stick_image.set_colorkey(WHITE)
item_images['stick']=pygame.transform.scale(stick_image,(ITEM_SIZE, ITEM_SIZE))

glass_image=pygame.image.load(os.path.join(assets_path, 'glass.png')).convert()
glass_image.set_colorkey(WHITE)
item_images['glass']=pygame.transform.scale(glass_image,(ITEM_SIZE, ITEM_SIZE))

window_image=pygame.image.load(os.path.join(assets_path, 'window.png')).convert()
window_image.set_colorkey(WHITE)
item_images['window']=pygame.transform.scale(window_image,(ITEM_SIZE, ITEM_SIZE))

SLOT_POSITIONS=[]

'''
NUM_COLS=6
NUM_ROWS=2

X_START_RELATIVE=32
Y_START_RELATIVE=375

GAP=96


for row in range(NUM_ROWS):
    for col in range(NUM_COLS):
        absolute_x=make_image_x+X_START_RELATIVE+col*GAP
        absolute_y=make_image_y+Y_START_RELATIVE+row*GAP

        SLOT_POSITIONS.append((absolute_x, absolute_y))

'''

X_POSITIONS=[34, 128, 220, 310, 404, 496]
Y_POSITIONS=[375,467]

for rel_y in Y_POSITIONS:
    for rel_x in X_POSITIONS:
        absolute_x=make_image_x+rel_x
        absolute_y=make_image_y+rel_y
        SLOT_POSITIONS.append((absolute_x, absolute_y))



#########메인루프#########

while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True

        if event.type==pygame.MOUSEBUTTONDOWN:
            mouse_pos=pygame.mouse.get_pos()

            if go_to_inside==False:
                if OUTSIDE_DOOR_AREA.collidepoint(mouse_pos):
                    go_to_inside=True
                    person_x=100

            else:
                if CLICK_AREA.collidepoint(mouse_pos):
                    open_door=not open_door

                if (not CLICK_AREA.collidepoint(mouse_pos))and (open_door==True):
                    open_door=not open_door
    
    keys=pygame.key.get_pressed()

    if go_to_inside==False:
        if keys[pygame.K_LEFT]:
            person_x-=person_speed
            if person_direction_right:
                person_image=flip_person_image
                person_direction_right=False

        if keys[pygame.K_RIGHT]:
            person_x+=person_speed
            if not person_direction_right:
                person_image=origin_person_image
                person_direction_right=True

        if person_x<0:
            person_x=0
        elif person_x>SCREEN_WIDTH-person_image.get_width():
            person_x=SCREEN_WIDTH-person_image.get_width()

        screen.blit(start_background_image, (0,0))
        screen.blit(person_image, (person_x, person_y))

    else:
        if keys[pygame.K_LEFT]:
            person_x-=person_speed
            if person_direction_right:
                person_image=flip_person_image
                person_direction_right=False

        if keys[pygame.K_RIGHT]:
            person_x+=person_speed
            if not person_direction_right:
                person_image=origin_person_image
                person_direction_right=True

        if person_x<0:
            person_x=0
            go_to_inside=False
        elif person_x>SCREEN_WIDTH-person_image.get_width():
            person_x=SCREEN_WIDTH-person_image.get_width()
        
        screen.blit(background_image, (0,0))
        screen.blit(person_image, (person_x, person_y))

        if open_door:
            screen.blit(make_image, (make_image_x, make_image_y))

            have_num=min(len(inventory), len(SLOT_POSITIONS))

            for i in range(have_num):
                slot_x, slot_y=SLOT_POSITIONS[i]

                item_name=inventory[i]

                item_draw=item_images.get(item_name)

                if item_draw:
                    screen.blit(item_draw, (slot_x, slot_y))


    pygame.display.flip()

    clock.tick(60)

pygame.quit()
