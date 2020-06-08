import random
import sys

import pygame
from pygame.locals import *


def get_rand_color(min_value=0, max_value=255):
    r = random.randint(min_value, max_value)
    g = random.randint(min_value, max_value)
    b = random.randint(min_value, max_value)
    a = random.randint(min_value, max_value)
    return r, g, b, a


def get_rand_position(width, height):
    x = random.randint(0, width)
    y = random.randint(0, height)
    return x, y


def get_rand_radius(min_value=10, max_value=30):
    r = random.randint(min_value, max_value)
    return r


def start():
    pygame.init()
    width = 400
    height = 400

    DISPLAYSURF = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Circles')

    iters = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if iters % 100 == 0:
            DISPLAYSURF.fill((0, 0, 0, 0))
            iters = 0

        pygame.draw.circle(DISPLAYSURF, get_rand_color(), get_rand_position(width, height), get_rand_radius())

        pygame.display.update()

        iters += 1


if __name__ == '__main__':
    start()
