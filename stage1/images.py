import pygame

background = pygame.image.load("stage1/assets/background.png")

enter = pygame.image.load("stage1/assets/enter.png")

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
U1 = pygame.image.load("stage1/assets/worker_U1.png")
U2 = pygame.image.load("stage1/assets/worker_U2.png")

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
paper = pygame.image.load("stage1/assets/paper.png")
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

rockBlock1 = pygame.image.load("stage1/assets/rock1.png")
rockBlock2 = pygame.image.load("stage1/assets/rock2.png")
rockBlock3 = pygame.image.load("stage1/assets/rock3.png")
rockBlock4 = pygame.image.load("stage1/assets/rock4.png")
rockBlock5 = pygame.image.load("stage1/assets/rock5.png")

soilBlock1 = pygame.image.load("stage1/assets/soil1.png")
soilBlock2 = pygame.image.load("stage1/assets/soil2.png")
soilBlock3 = pygame.image.load("stage1/assets/soil3.png")
soilBlock4 = pygame.image.load("stage1/assets/soil4.png")

special1 = pygame.image.load("stage1/assets/special1.png")
special2 = pygame.image.load("stage1/assets/special2.png")
special3 = pygame.image.load("stage1/assets/special3.png")

# 각 이미지들 배열에 저장
characters = [[LDc, LW1c, LW2c,LDPc], [RDc, RW1c, RW2c,RDPc], [DLc,DLc,DLc,DLc], [DRc,DRc,DRc,DRc], [U1,U1,U2,U2]]
blocks = [block1, block2, block3, block4]
picks = [[pick_LF, pick_LB], [pick_RF, pick_RB],[pick_LF, pick_LD],[pick_RF, pick_RD]]
items = [gem, sand, fossil, paper ,ladder, rock]
magmas = [magma1, magma2, magma3]
waters = [water1, water2, water3]
rockBlocks = [rockBlock1, rockBlock2, rockBlock3, rockBlock4, rockBlock5]
soilBlocks = [soilBlock1, soilBlock2, soilBlock3, soilBlock4]
specialBlocks = [special1, special2, special3]