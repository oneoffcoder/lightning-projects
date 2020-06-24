import os
import random
import sys

import pygame
from pygame.locals import *


class Ball(object):
    def __init__(self, color, position, radius):
        self.color = color
        self.position = position
        self.radius = radius
        self.dx = 1 if random.random() < 0.5 else -1
        self.dy = 1 if random.random() < 0.5 else 1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)

    def update(self, width, height):
        x, y = self.position
        x_changed, y_changed = False, False

        if x + self.radius >= width:
            self.dx = -1
            x_changed = True
        elif x <= 0:
            self.dx = 1
            x_changed = True

        if y + self.radius >= height:
            self.dy = -1
            y_changed = True
        elif y <= 0:
            self.dy = 1
            y_changed = True

        x, y = x + 1 * self.dx, y + 1 * self.dy
        self.position = x, y

        if x_changed or y_changed:
            self.color = Ball.get_rand_color()

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
    def rand(width, height):
        color = Ball.get_rand_color()
        position = Ball.get_rand_position(width, height)
        radius = Ball.get_rand_radius()
        return Ball(color, position, radius)


def start():
    pygame.init()

    FPS = 30
    width = 400
    height = 400
    DISPLAYSURF = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Bouncing Balls')
    fps_clock = pygame.time.Clock()

    balls = [Ball.rand(width, height) for _ in range(10)]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill((0, 0, 0, 0))

        for ball in balls:
            ball.draw(DISPLAYSURF)
            ball.update(width, height)

        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    start()
