import random
import sys

import pygame
from pygame.locals import *


class Image(object):
    def __init__(self, fpath, position, scale=1.0):
        img = pygame.image.load(fpath)
        w, h = img.get_rect(center=position).size[0], img.get_rect(center=position).size[1]
        w, h = int(w * scale), int(h * scale)
        img = pygame.transform.scale(img, (w, h))

        x = position[0] - int(img.get_rect(center=position).size[0] / 2.0)
        y = position[1] - int(img.get_rect(center=position).size[1] / 2.0)

        self.image = img
        self.position = x, y

    def draw(self, surface):
        surface.blit(self.image, self.position)

    def update(self, width, height, event):
        x, y = self.position
        rect = self.image.get_rect(center=self.position)
        img_width = rect.size[0]
        img_height = rect.size[1]

        if event.key in (K_LEFT, K_a):
            if x > 0:
                x -= 10
        elif event.key in (K_RIGHT, K_d):
            if x + img_width < width:
                x += 10

        if event.key in (K_UP, K_w):
            if y > 0:
                y -= 10
        elif event.key in (K_DOWN, K_s):
            if y + img_height < height:
                y += 10

        self.position = x, y

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

    satyr = Image('./images/Satyr_01_Idle_000.png', (200, 200), 0.25)

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
