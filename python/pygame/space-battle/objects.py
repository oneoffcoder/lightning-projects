import random
import time
import uuid

import pygame
from pygame.constants import K_LEFT, K_a, K_RIGHT, K_d


class BaseObject(pygame.sprite.Sprite):
    def __init__(self, ipath, position, scale=0.5):
        pygame.sprite.Sprite.__init__(self)

        self.uuid = str(uuid.uuid4())
        self.image = BaseObject.__scale__(ipath, position, scale)
        self.rect = self.image.get_rect(center=position)

    def get_center(self):
        return self.rect.center

    def draw(self, surface, **kwargs):
        raise NotImplementedError('Not yet implemented')

    @staticmethod
    def __scale__(ipath, position, scale):
        img = pygame.image.load(ipath)
        rect = img.get_rect(center=position)
        w, h = rect.size[0], rect.size[1]
        w, h = int(w * scale), int(h * scale)
        return pygame.transform.scale(img, (w, h))


class Bullet(BaseObject):
    def __init__(self, position, scale=1.0):
        BaseObject.__init__(self, './images/bullet.png', position, scale)

    def draw(self, surface, **kwargs):
        x, y = self.rect.center
        self.rect.center = x, y - 5

        surface.blit(self.image, self.rect.center)

        if y <= 0:
            self.kill()

    @staticmethod
    def instance(**kwargs):
        return Bullet(kwargs['position'])


class Rock(BaseObject):
    def __init__(self, position, scale=1.0):
        BaseObject.__init__(self, './images/rock.png', position, scale)

    def draw(self, surface, **kwargs):
        x, y = self.rect.center
        self.rect.center = x, y + 1

        surface.blit(self.image, self.rect.center)

        if y >= kwargs['height']:
            self.kill()


class Ship(BaseObject):
    def __init__(self, position, scale=1.0):
        BaseObject.__init__(self, './images/ship.png', position, scale)

    def draw(self, surface, **kwargs):
        width, height = kwargs['width'], kwargs['height']
        x, y = self.rect.center
        w, h = self.rect.size

        if 'keys' in kwargs:
            keys = kwargs['keys']
            if keys[K_LEFT] or keys[K_a]:
                if x - w / 2.0 >= 0:
                    x -= 4
            elif keys[K_RIGHT] or keys[K_d]:
                if x + w / 2.0 <= width:
                    x += 4

        self.rect.center = x, y

        surface.blit(self.image, self.rect.center)


class RockGenerator(object):
    def __init__(self, width, height):
        rock = Rock((width / 2.0, height / 2.0))
        w, h = rock.rect.size
        self.x_pos = [x for x in range(0, width, w)]
        self.prev_x = None
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

    def next(self):
        while True:
            curr_x = random.choice(self.x_pos)
            if curr_x != self.prev_x:
                self.prev_x = curr_x
                return Rock((curr_x, 20))


class GameInfo(object):
    def __init__(self, score, lives):
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.color = (0, 0, 0)
        self.position = 10, 10
        self.score = score
        self.lives = lives

    def __get_drawing_objects__(self):
        text_surface = self.font.render(f'Score: {self.score}, Lives: {self.lives}', True, self.color)
        rect = text_surface.get_rect()
        rect.x, rect.y = 10, 10

        return text_surface, rect

    def draw(self, surface, **kwargs):
        self.score = kwargs['score']
        self.lives = kwargs['lives']

        text_surface, rect = self.__get_drawing_objects__()
        surface.blit(text_surface, rect)


class GameOverMessage(object):
    def __init__(self, width, height, score, lives):
        self.game_over_font = pygame.font.Font('freesansbold.ttf', 30)
        self.game_info_font = pygame.font.Font('freesansbold.ttf', 20)
        self.game_action_font = pygame.font.Font('freesansbold.ttf', 20)

        self.game_over_color = (255, 0, 0)
        self.game_info_color = (0, 0, 0)
        self.game_action_color = (0, 0, 0)

        self.center = width / 2.0, height / 2.0
        self.score = score
        self.lives = lives

    def __get_game_over__(self):
        text = 'Game Over'
        text_surface = self.game_over_font.render(text, True, self.game_over_color)
        rect = text_surface.get_rect()
        rect.center = self.center

        return text_surface, rect

    def __get_game_info__(self):
        text = f'Score: {self.score}, Lives: {self.lives}'
        text_surface = self.game_info_font.render(text, True, self.game_info_color)
        rect = text_surface.get_rect()
        rect.center = self.center[0], self.center[1] + 30

        return text_surface, rect

    def __get_game_action__(self):
        text = 'Hit "q" to quit. Hit "c" to continue.'
        text_surface = self.game_action_font.render(text, True, self.game_action_color)
        rect = text_surface.get_rect()
        rect.center = self.center[0], self.center[1] + 60

        return text_surface, rect

    def draw(self, surface):
        text_surface, rect = self.__get_game_over__()
        surface.blit(text_surface, rect)

        text_surface, rect = self.__get_game_info__()
        surface.blit(text_surface, rect)

        text_surface, rect = self.__get_game_action__()
        surface.blit(text_surface, rect)
