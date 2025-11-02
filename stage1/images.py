import pygame

background = pygame.image.load("stage1/assets/background.png")

block1 = pygame.image.load("stage1/assets/block1.jpg")
block2 = pygame.image.load("stage1/assets/block2.png")
block3 = pygame.image.load("stage1/assets/block3.png")
block4 = pygame.image.load("stage1/assets/block4.png")

LDc = pygame.image.load("stage1/assets/worker_LD.png")
LDPc = pygame.image.load("stage1/assets/worker_LDP.png")
LW1c = pygame.image.load("stage1/assets/worker_LW1.png")
LW2c = pygame.image.load("stage1/assets/worker_LW2.png")
RDc = pygame.image.load("stage1/assets/worker_RD.png")
RDPc = pygame.image.load("stage1/assets/worker_RDP.png")
RW1c = pygame.image.load("stage1/assets/worker_RW1.png")
RW2c = pygame.image.load("stage1/assets/worker_RW2.png")
DLc = pygame.image.load("stage1/assets/worker_DL.png")
DRc = pygame.image.load("stage1/assets/worker_DR.png")

pick_LF = pygame.image.load("stage1/assets/pick_LF.png")
pick_LB = pygame.image.load("stage1/assets/pick_LB.png")
pick_LD = pygame.image.load("stage1/assets/pick_LD.png")
pick_RF = pygame.image.load("stage1/assets/pick_RF.png")
pick_RB = pygame.image.load("stage1/assets/pick_RB.png")
pick_RD = pygame.image.load("stage1/assets/pick_RD.png")

inven = pygame.image.load("stage1/assets/invenBlock.png")
sand = pygame.image.load("stage1/assets/sand.png")
gem = pygame.image.load("stage1/assets/gem.png")
fossil = pygame.image.load("stage1/assets/fossil.png")
ladder = pygame.image.load("stage1/assets/ladder.png")

rock = pygame.image.load("stage1/assets/rock.png")

magma1 = pygame.image.load("stage1/assets/magma1.png")
magma2 = pygame.image.load("stage1/assets/magma2.png")
magma3 = pygame.image.load("stage1/assets/magma3.png")
magma_back = pygame.image.load("stage1/assets/magma_background.png")

water1 = pygame.image.load("stage1/assets/water1.png")
water2 = pygame.image.load("stage1/assets/water2.png")
water3 = pygame.image.load("stage1/assets/water3.png")
water_back = pygame.image.load("stage1/assets/water_background.png")

restart_btn = pygame.image.load("stage1/assets/restart_btn.png")

# 각 이미지들 배열에 저장
characters = [[LDc, LW1c, LW2c,LDPc], [RDc, RW1c, RW2c,RDPc], [DLc,DLc,DLc,DLc], [DRc,DRc,DRc,DRc]]
blocks = [block1, block2, block3, block4]
picks = [[pick_LF, pick_LB], [pick_RF, pick_RB],[pick_LF, pick_LD],[pick_RF, pick_RD]]
items = [gem, sand, fossil, ladder, rock]
magmas = [magma1, magma2, magma3]
waters = [water1, water2, water3]