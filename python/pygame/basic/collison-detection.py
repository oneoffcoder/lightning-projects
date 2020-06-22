import os
import random
import sys

import pygame
from pygame.locals import *


class Satyr(pygame.sprite.Sprite):
    def __init__(self, position, ipath, scale=0.5):
        pygame.sprite.Sprite.__init__(self)

        img = pygame.image.load(ipath)
        rect = img.get_rect(center=position)
        w, h = rect.size[0], rect.size[1]
        w, h = int(w * scale), int(h * scale)
        img = pygame.transform.scale(img, (w, h))

        rect = img.get_rect(center=position)

        self.image = img
        self.rect = rect
        self.rect.center = position

    def draw(self, surface, position):
        self.rect.center = position
        surface.blit(self.image, position)


class Image(pygame.sprite.Sprite):
    def __init__(self, position, ipath, scale=1.0):
        pygame.sprite.Sprite.__init__(self)

        img = pygame.image.load(ipath)
        w, h = img.get_rect().size[0], img.get_rect().size[1]
        w, h = int(w * scale), int(h * scale)
        img = pygame.transform.scale(img, (w, h))

        rect = img.get_rect(center=position)

        self.image = img
        self.rect = rect
        self.rect.center = position
        self.dx = 1 if random.random() < 0.5 else -1
        self.dy = 1 if random.random() < 0.5 else 1

    def draw(self, surface):
        surface.blit(self.image, self.rect.center)

    def update(self, width, height):
        x, y = self.rect.center

        if x + self.image.get_rect().size[0] >= width:
            self.dx = -1
        elif x <= 0:
            self.dx = 1

        if y + self.image.get_rect().size[1] >= height:
            self.dy = -1
        elif y <= 0:
            self.dy = 1

        x, y = x + 1 * self.dx, y + 1 * self.dy
        self.rect.center = x, y


def start():
    pygame.init()

    FPS = 30
    width = 400
    height = 400
    DISPLAYSURF = pygame.display.set_mode((width, height))
    DISPLAYSURF.fill((255, 255, 255))
    pygame.display.set_caption('Key Events')
    fps_clock = pygame.time.Clock()

    satyr = Satyr((200, 200), './images/Satyr_01_Idle_000.png', scale=0.25)

    ball = Image((random.randint(0, width), random.randint(0, height)), './images/ball.png', scale=0.25)
    ball_group = pygame.sprite.Group()
    ball_group.add(ball)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill((255, 255, 255, 0))

        if pygame.sprite.spritecollide(satyr, ball_group, False):
            print(f'collided {ball.rect.center}')

        satyr.draw(DISPLAYSURF, pygame.mouse.get_pos())
        ball.draw(DISPLAYSURF)
        ball.update(width, height)

        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    start()
