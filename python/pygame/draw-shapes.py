import random
import sys

import pygame
from pygame.locals import *


class Shape(object):
    def __init__(self, color):
        self.color = color

    def draw(self, surface):
        raise NotImplementedError('Not implemented')

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


class Line(Shape):
    def __init__(self, color, start, stop, width):
        super().__init__(color)
        self.start = start
        self.stop = stop
        self.width = width

    def draw(self, surface):
        pygame.draw.line(surface, self.color, self.start, self.stop, self.width)

    @staticmethod
    def get_rand_width(min_value=1, max_value=5):
        return random.randint(min_value, max_value)

    @staticmethod
    def rand(width, height):
        color = Shape.get_rand_color()
        start = Shape.get_rand_position(width, height)
        stop = Shape.get_rand_position(width, height)
        width = Line.get_rand_width()
        return Line(color, start, stop, width)


class Circle(Shape):
    def __init__(self, color, position, radius):
        super().__init__(color)
        self.position = position
        self.radius = radius

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)

    @staticmethod
    def get_rand_radius(min_value=10, max_value=30):
        r = random.randint(min_value, max_value)
        return r

    @staticmethod
    def rand(width, height):
        color = Shape.get_rand_color()
        position = Shape.get_rand_position(width, height)
        radius = Circle.get_rand_radius()
        return Circle(color, position, radius)


class Rectangle(Shape):
    def __init__(self, color, position, dimension):
        super().__init__(color)
        self.position = position
        self.dimension = dimension

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position, self.dimension))

    @staticmethod
    def get_rand_dimension(min_value=10, max_value=50):
        width = random.randint(min_value, max_value)
        height = random.randint(min_value, max_value)
        return width, height

    @staticmethod
    def rand(width, height):
        color = Shape.get_rand_color()
        position = Shape.get_rand_position(width, height)
        dimension = Rectangle.get_rand_dimension()
        return Rectangle(color, position, dimension)


def start():
    pygame.init()
    width = 400
    height = 400

    DISPLAYSURF = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Shapes')

    iters = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if iters % 100 == 0:
            DISPLAYSURF.fill((0, 0, 0, 0))
            iters = 0

        probability = random.random()
        if probability < 0.33:
            shape = Circle.rand(width, height)
        elif probability < 0.66:
            shape = Line.rand(width, height)
        else:
            shape = Rectangle.rand(width, height)

        shape.draw(DISPLAYSURF)

        pygame.display.update()

        iters += 1


if __name__ == '__main__':
    start()
