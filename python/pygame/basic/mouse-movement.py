import os
import sys

import pygame
from pygame.locals import *


class Satyr(pygame.sprite.Sprite):
    def __init__(self, position, scale=0.5):
        pygame.sprite.Sprite.__init__(self)

        img = pygame.image.load('./images/Satyr_01_Idle_000.png')
        rect = img.get_rect(center=position)
        w, h = rect.size[0], rect.size[1]
        w, h = int(w * scale), int(h * scale)
        img = pygame.transform.scale(img, (w, h))

        rect = img.get_rect(center=position)
        x = position[0] - int(rect.size[0] / 2.0)
        y = position[1] - int(rect.size[1] / 2.0)

        self.image = img
        self.rect = rect
        self.position = x, y

    def draw(self, surface, position):
        self.position = position[0] - self.rect.width / 2, position[1] - self.rect.height / 2
        surface.blit(self.image, self.position)


def start():
    pygame.init()

    FPS = 30
    width = 400
    height = 400
    DISPLAYSURF = pygame.display.set_mode((width, height))
    DISPLAYSURF.fill((255, 255, 255))
    pygame.display.set_caption('Key Events')
    fps_clock = pygame.time.Clock()

    satyr = Satyr((200, 200), 0.25)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill((255, 255, 255, 0))

        satyr.draw(DISPLAYSURF, pygame.mouse.get_pos())

        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    start()
