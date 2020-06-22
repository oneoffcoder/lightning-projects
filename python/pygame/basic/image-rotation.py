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
        self.dx = 1 if random.random() < 0.5 else -1
        self.dy = 1 if random.random() < 0.5 else 1
        self.drot = 1 if random.random() < 0.5 else -1
        self.rotation = 0

    def draw(self, surface):
        image = pygame.transform.rotate(self.image, self.rotation)
        surface.blit(image, self.position)

    def update(self, width, height):
        x, y = self.position
        x_changed, y_changed = False, False

        if x + self.image.get_rect().size[0] >= width:
            self.dx = -1
            x_changed = True
        elif x <= 0:
            self.dx = 1
            x_changed = True

        if y + self.image.get_rect().size[1] >= height:
            self.dy = -1
            y_changed = True
        elif y <= 0:
            self.dy = 1
            y_changed = True

        x, y = x + 1 * self.dx, y + 1 * self.dy
        self.position = x, y

        if x_changed or y_changed:
            self.drot *= -1
            self.rotation += 10 * self.drot
        else:
            self.rotation += 5 * self.drot

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

    FPS = 30
    width = 400
    height = 400
    DISPLAYSURF = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Rotating Image')
    fps_clock = pygame.time.Clock()

    image = Image.rand('./images/ball.png', width, height)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill((0, 0, 0, 0))

        image.draw(DISPLAYSURF)
        image.update(width, height)

        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    start()
