import pygame
import os

SCREEN_WIDTH=1200
SCREEN_HEIGHT=800

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)

pygame.init()
pygame.display.set_caption("KKANDDABBIA!")

screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock=pygame.time.Clock()

current_path=os.path.dirname(__file__)
assets_path=os.path.join(current_path, 'kkanddabbia')

font = pygame.font.Font(None, 74) 

start_background_image=pygame.image.load(os.path.join(assets_path, 'outside.jpg'))
start_background_image=pygame.transform.scale(start_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

current_map="outside1" 

background_image=pygame.image.load(os.path.join(assets_path, 'inside.jpg'))
background_image=pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

second_background_image=pygame.image.load(os.path.join(assets_path, 'outside2.jpg'))
second_background_image=pygame.transform.scale(second_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


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
person_direction_right=True

open_door=False

done=False

game_over=False

CLICK_AREA=pygame.Rect(900,400,210,260)
OUTSIDE_DOOR_AREA=pygame.Rect(400,400,400,300)

MAKE_BUTTON_X=351
MAKE_BUTTON_Y=29
MAKE_BUTTON_W=111
MAKE_BUTTON_H=111

MAKE_BUTTON_AREA = pygame.Rect(
    make_image_x + MAKE_BUTTON_X,
    make_image_y + MAKE_BUTTON_Y,
    MAKE_BUTTON_W,
    MAKE_BUTTON_H
)


#################아이템################

ITEM_SIZE=70

inventory=['fire', 'stone', 'stone', 'wood', 'stick', 'glass', 'window', 'soil', 'stick', 'glass', 'stone', 'wood']

crafting_table=[None]*9

item_images={}

def load_item(name, filename):
    try:
        image = pygame.image.load(os.path.join(assets_path, filename))
        item_images[name] = pygame.transform.scale(image, (ITEM_SIZE, ITEM_SIZE))
    except pygame.error:
        print(f"Error loading {filename}. Skipping.")

load_item('fire', 'fire.png')
load_item('stone', 'stone.png')
load_item('soil', 'soil.png')
load_item('wood', 'wood.png')
load_item('stick', 'stick.png')
load_item('glass', 'glass.png')
load_item('window', 'window-piece.png')


##################제작 조합#################

RECIPES=[
    {
        'recipe':['stone', 'stone', 'fire', None,None, None, None, None, None],
        'result':'steel'
    }
]


#################연구실 제작창################

INVENTORY_SLOT_POSITIONS=[]
INVENTORY_SLOT_RECTS=[]

INV_X_POSITIONS=[34, 128, 220, 310, 404, 496]
INV_Y_POSITIONS=[375, 467]

for rel_y in INV_Y_POSITIONS:
    for rel_x in INV_X_POSITIONS:
        absolute_x=make_image_x+rel_x
        absolute_y=make_image_y+rel_y
        INVENTORY_SLOT_POSITIONS.append((absolute_x, absolute_y))
        
        INVENTORY_SLOT_RECTS.append(pygame.Rect(absolute_x, absolute_y, ITEM_SIZE, ITEM_SIZE))


CRAFT_SLOT_POSITIONS=[]
CRAFT_SLOT_RECTS=[]

CRAFT_X_POSITIONS = [53, 145, 237] 
CRAFT_Y_POSITIONS = [62, 154, 246]

for rel_y in CRAFT_Y_POSITIONS:
    for rel_x in CRAFT_X_POSITIONS:
        absolute_x=make_image_x+rel_x
        absolute_y=make_image_y+rel_y
        CRAFT_SLOT_POSITIONS.append((absolute_x, absolute_y))
        CRAFT_SLOT_RECTS.append(pygame.Rect(absolute_x, absolute_y, ITEM_SIZE, ITEM_SIZE))


#########메인루프#########


while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True

        if event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE and game_over:
            done = True

        if event.type==pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_pos=pygame.mouse.get_pos()
            
            if current_map == "outside1":
                if OUTSIDE_DOOR_AREA.collidepoint(mouse_pos):
                    current_map="inside"
                    person_x=100
                    continue

            elif current_map == "inside":
                if CLICK_AREA.collidepoint(mouse_pos):
                    open_door=not open_door
                    continue
                
                if open_door:
                    
                    if MAKE_BUTTON_AREA.collidepoint(mouse_pos):
                        found_recipe=False
                        
                        for recipe_data in RECIPES:
                            if crafting_table==recipe_data['recipe']:
                                inventory.append(recipe_data['result'])
                                crafting_table=[None]*9
                                found_recipe=True
                                break
                        
                        if not found_recipe:
                            game_over=True
                            open_door = False
                            
                        continue 
                    
                    for i in range(len(inventory)):
                        if i < len(INVENTORY_SLOT_RECTS) and INVENTORY_SLOT_RECTS[i].collidepoint(mouse_pos):
                            
                            item_name_clicked = inventory[i] 
                            
                            try:
                                empty_slot_index = crafting_table.index(None) 
                                crafting_table[empty_slot_index] = item_name_clicked
                                inventory.pop(i) 
                                continue
                            except ValueError:
                                continue
                                
                    for i in range(len(crafting_table)):
                        if crafting_table[i] is not None and CRAFT_SLOT_RECTS[i].collidepoint(mouse_pos):
                            inventory.append(crafting_table[i])
                            crafting_table[i] = None 
                            continue

                make_window_rect = make_image.get_rect(topleft=(make_image_x, make_image_y))
                
                if open_door and not make_window_rect.collidepoint(mouse_pos) and not CLICK_AREA.collidepoint(mouse_pos):
                    open_door = False
                        
            elif current_map == "outside2":
                 pass


    
    if game_over:
        screen.fill(BLACK)
        game_over_text=font.render("GAME OVER", True, RED)
        small_font_for_sub = pygame.font.Font(None, 40)
        
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
    
    else:
        keys=pygame.key.get_pressed()
        
        if current_map == "outside1":
            if keys[pygame.K_LEFT]:
                person_x-=person_speed
                person_image=flip_person_image
                person_direction_right=False
            
            if keys[pygame.K_RIGHT]:
                person_x+=person_speed
                person_image=origin_person_image
                person_direction_right=True

            if person_x<0:
                person_x=0
            elif person_x > SCREEN_WIDTH - person_image.get_width():
                current_map = "outside2" 
                person_x = 5

            screen.blit(start_background_image, (0,0))
            screen.blit(person_image, (person_x, person_y))
        
        elif current_map == "inside":
            if keys[pygame.K_LEFT]:
                person_x-=person_speed
                person_image=flip_person_image
                person_direction_right=False
            
            if keys[pygame.K_RIGHT]:
                person_x+=person_speed
                person_image=origin_person_image
                person_direction_right=True

            if person_x<0:
                current_map = "outside1"
                person_x = SCREEN_WIDTH - person_image.get_width() - 5 
            elif person_x>SCREEN_WIDTH-person_image.get_width():
                person_x=SCREEN_WIDTH-person_image.get_width()
            
            screen.blit(background_image, (0,0))
            screen.blit(person_image, (person_x, person_y))

            if open_door:
                screen.blit(make_image, (make_image_x, make_image_y))

                have_num=min(len(inventory), len(INVENTORY_SLOT_POSITIONS))
                for i in range(have_num):
                    slot_x, slot_y=INVENTORY_SLOT_POSITIONS[i]
                    item_name=inventory[i]
                    item_draw=item_images.get(item_name)
                    if item_draw:
                        screen.blit(item_draw, (slot_x, slot_y))
                        
                for i in range(len(crafting_table)):
                    item_name = crafting_table[i]
                    if item_name is not None:
                        slot_x, slot_y = CRAFT_SLOT_POSITIONS[i]
                        item_draw = item_images.get(item_name)
                        if item_draw:
                            screen.blit(item_draw, (slot_x, slot_y))

        elif current_map == "outside2":
            if keys[pygame.K_LEFT]:
                person_x-=person_speed
                person_image=flip_person_image
                person_direction_right=False

            if keys[pygame.K_RIGHT]:
                person_x+=person_speed
                person_image=origin_person_image
                person_direction_right=True

            if person_x<0:
                current_map = "outside1"
                person_x = SCREEN_WIDTH - person_image.get_width() - 5 
            elif person_x>SCREEN_WIDTH-person_image.get_width():
                person_x=SCREEN_WIDTH-person_image.get_width()
            
            screen.blit(second_background_image, (0,0))
            screen.blit(person_image, (person_x, person_y))
        

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
