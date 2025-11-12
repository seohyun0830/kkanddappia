import pygame
import os

CURRENT_DIR = os.path.dirname(__file__)

def load_image(name):
    return pygame.image.load(os.path.join(CURRENT_DIR, "assets", name))

puzzle1 = load_image("puzzle1.png")
puzzle2 = load_image("puzzle2.png")

outline1 = load_image("outline1.png")
outline2 = load_image("outline2.png")
outline3 = load_image("outline3.png")

check1 = load_image("check1.png")
check2 = load_image("check2.png")
check3 = load_image("check3.png")
check4 = load_image("check4.png")
check5 = load_image("check5.png")
check6 = load_image("check6.png")

checks = [check1, check2, check3, check4, check5, check6]

found = load_image("found.png")
notFound = load_image("notFound.png")
