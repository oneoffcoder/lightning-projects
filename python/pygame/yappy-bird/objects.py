import random
import time
import uuid

import pygame
from pygame.constants import K_SPACE


class Bird(pygame.sprite.Sprite):
    def __init__(self, position, scale=0.1):
        pygame.sprite.Sprite.__init__(self)

        paths = [f'./images/frame-{i + 1}.png' for i in range(8)]
        imgs = [pygame.image.load(p) for p in paths]
        rect = imgs[0].get_rect()

        w, h = rect.size[0], rect.size[1]
        w, h = int(w * scale), int(h * scale)

        self.uuid = str(uuid.uuid4())
        self.width, self.height = w, h
        self.imgs = [pygame.transform.scale(img, (w, h)) for img in imgs]
        self.rect = self.imgs[0].get_rect()
        self.rect.center = position[0] - w / 2.0, position[1] - h / 2.0
        self.index = 0
        self.is_killed = False

    def draw(self, surface, **kwargs):
        if self.is_killed:
            return

        if kwargs['started']:
            if 'keys' in kwargs and kwargs['keys'][K_SPACE]:
                dy = -10
            else:
                dy = 10
        else:
            dy = 0

        x, y = self.rect.center[0], self.rect.center[1] + dy
        y = max(0, y)
        y = min(kwargs['height'] - self.height, y)

        self.rect.center = x, y

        surface.blit(self.imgs[self.index], self.rect.center)
        self.index += 1
        if self.index >= len(self.imgs):
            self.index = 0

        if y >= kwargs['height'] - self.height:
            self.is_killed = True
            self.kill()


class Pipe(pygame.sprite.Sprite):
    def __init__(self, position, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.uuid = str(uuid.uuid4())
        self.color = (10, 200, 10, 1)
        self.position = position
        self.dimension = width, height
        self.rect = (self.position, self.dimension)
        self.is_killed = False

    def draw(self, surface, **kwargs):
        if self.is_killed:
            return

        pygame.draw.rect(surface, self.color, (self.position, self.dimension))
        self.position = self.position[0] - 5, self.position[1]
        self.rect = (self.position, self.dimension)

        if self.position[0] <= 0:
            self.is_killed = True
            self.kill()

    def __repr__(self):
        return f'pipe: pos={self.position} | dim={self.dimension}'


class PipeGenerator(object):
    def __init__(self, pipe_width=70, tb_spacing=200):
        self.pipe_width = pipe_width
        self.tb_spacing = tb_spacing
        self.start_time = None

    def should_generate(self):
        if self.start_time is None:
            self.start_time = time.time()
            return True

        stop_time = time.time()
        diff = int(stop_time - self.start_time)
        if diff >= 2:
            self.start_time = stop_time
            return True
        return False

    def next(self, **kwargs):
        width, height = kwargs['width'], kwargs['height']

        top_height = random.randint(int(height * 0.25), int(height * 0.50))
        bot_height = height - (top_height + self.tb_spacing)

        top_x, top_y = width, 0
        bot_x, bot_y = width, top_height + self.tb_spacing

        top_pipe = Pipe((top_x, top_y), self.pipe_width, top_height)
        bot_pipe = Pipe((bot_x, bot_y), self.pipe_width, bot_height)

        return top_pipe, bot_pipe
