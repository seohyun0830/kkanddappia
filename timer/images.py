import pygame

over1 = pygame.image.load("timer/assets/over1.png")
over2 = pygame.image.load("timer/assets/over2.png")
over3 = pygame.image.load("timer/assets/over3.png")
over4 = pygame.image.load("timer/assets/over4.png")
over5 = pygame.image.load("timer/assets/over5.png")
over6 = pygame.image.load("timer/assets/over6.png")

over1 = pygame.transform.smoothscale(over1, (1200, 800))
over2 = pygame.transform.smoothscale(over2, (1200, 800))
over3 = pygame.transform.smoothscale(over3, (1200, 800))
over4 = pygame.transform.smoothscale(over4, (1200, 800))
over5 = pygame.transform.smoothscale(over5, (1200, 800))
over6 = pygame.transform.smoothscale(over6, (1200, 800))

overs = [over1, over2, over3, over4, over5, over6]