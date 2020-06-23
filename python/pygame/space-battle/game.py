import os
import sys

import pygame
from pygame.constants import KEYUP, QUIT, KEYDOWN

from objects import Ship


def start():
    pygame.init()

    FPS = 30
    width = 500
    height = 400
    DISPLAYSURF = pygame.display.set_mode((width, height))
    DISPLAYSURF.fill((255, 255, 255))
    pygame.display.set_caption('Space Battle')
    fps_clock = pygame.time.Clock()

    bullets = pygame.sprite.Group()
    rocks = pygame.sprite.Group()
    ship = Ship((width / 2, height - 50), 0.5)

    while True:
        kwargs = {
            'width': width,
            'height': height
        }

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill((255, 255, 255, 0))

        keys = pygame.key.get_pressed()
        kwargs['keys'] = keys

        ship.draw(DISPLAYSURF, **kwargs)

        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    start()
