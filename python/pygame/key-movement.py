import random
import sys

import pygame
from pygame.locals import *


class Image(object):
    def __init__(self, fpath, position, scale=1.0):
        img = pygame.image.load(fpath)
        w, h = img.get_rect().size[0], img.get_rect().size[1]
        w, h = int(w * scale), int(h * scale)
        img = pygame.transform.scale(img, (w, h))

        self.image = img
        self.position = position

    def draw(self, surface):
        surface.blit(self.image, self.position)

    def update(self, width, height, event):
        x, y = self.position
        dx, dy = 0, 0

        if event.key in (K_UP, K_w):
            dy = -10
        if event.key in (K_DOWN, K_s):
            dy = 10
        if event.key in (K_LEFT, K_a):
            dx = -10
        if event.key in (K_RIGHT, K_d):
            dx = 10

        x += dx
        y += dy

        if x >= width:
            x = width
        elif x <= 0:
            x = 0

        if y >= height:
            y = height
        elif y <= 0:
            y = 0

        self.position = x, y
        print(self.position)

    @staticmethod
    def get_rand_color(min_value=0, max_value=255):
        r = random.randint(min_value, max_value)
        g = random.randint(min_value, max_value)
        b = random.randint(min_value, max_value)
        a = random.randint(min_value, max_value)
        return r, g, b, a

    @staticmethod
    def get_rand_position(width, height):
        x = random.randint(0, width)
        y = random.randint(0, height)
        return x, y

    @staticmethod
    def get_rand_radius(min_value=10, max_value=30):
        r = random.randint(min_value, max_value)
        return r

    @staticmethod
    def rand(fpath, width, height, scale=0.25):
        position = Image.get_rand_position(width, height)
        return Image(fpath, position, scale=scale)


def start():
    pygame.init()

    width = 400
    height = 400
    DISPLAYSURF = pygame.display.set_mode((width, height))
    DISPLAYSURF.fill((255, 255, 255))
    pygame.display.set_caption('Key Events')

    satyr = Image('./images/Satyr_01_Idle_000.png', (150, 150), 0.25)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                satyr.update(width, height, event)

        DISPLAYSURF.fill((255, 255, 255, 0))

        satyr.draw(DISPLAYSURF)

        pygame.display.update()


if __name__ == '__main__':
    start()
