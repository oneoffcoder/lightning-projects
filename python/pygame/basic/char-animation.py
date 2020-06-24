import os
import sys

import pygame
from pygame.locals import *


class Bird(pygame.sprite.Sprite):
    def __init__(self, position, scale=0.5):
        pygame.sprite.Sprite.__init__(self)

        paths = [f'./images/frame-{i + 1}.png' for i in range(8)]
        imgs = [pygame.image.load(p) for p in paths]
        rect = imgs[0].get_rect()

        w, h = rect.size[0], rect.size[1]
        w, h = int(w * scale), int(h * scale)

        self.imgs = [pygame.transform.scale(img, (w, h)) for img in imgs]
        self.rect = self.imgs[0].get_rect()
        self.rect.center = position[0] - w / 2.0, position[1] - h / 2.0
        self.index = 0

    def draw(self, surface):
        surface.blit(self.imgs[self.index], self.rect.center)
        self.index += 1
        if self.index >= len(self.imgs):
            self.index = 0


def start():
    pygame.init()

    FPS = 30
    width = 400
    height = 400
    DISPLAYSURF = pygame.display.set_mode((width, height))
    DISPLAYSURF.fill((255, 255, 255))
    pygame.display.set_caption('Key Events')
    fps_clock = pygame.time.Clock()

    bird = Bird((200, 200), 0.10)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill((255, 255, 255, 0))

        bird.draw(DISPLAYSURF)

        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    start()
