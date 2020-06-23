import pygame
from pygame.constants import K_LEFT, K_a, K_RIGHT, K_d


class BaseObject(pygame.sprite.Sprite):
    def __init__(self, ipath, position, scale=0.5):
        pygame.sprite.Sprite.__init__(self)

        img = pygame.image.load(ipath)
        rect = img.get_rect(center=position)
        w, h = rect.size[0], rect.size[1]
        w, h = int(w * scale), int(h * scale)
        self.image = pygame.transform.scale(img, (w, h))
        self.rect = self.image.get_rect(center=position)
        self.should_kill = False

    def get_center(self):
        return self.rect.center

    def draw(self, surface, **kwargs):
        raise NotImplementedError('Not yet implemented')


class Bullet(BaseObject):
    def __init__(self, position, scale=1.0):
        BaseObject.__init__(self, './images/bullet.png', position, scale)

    def draw(self, surface, **kwargs):
        if self.should_kill:
            return

        x, y = self.rect.center
        self.rect.center = x, y - 1

        surface.blit(self.image, self.rect.center)

        if y <= 0:
            self.should_kill = True


class Rock(BaseObject):
    def __init__(self, position, scale=1.0):
        BaseObject.__init__(self, './images/rock.png', position, scale)

    def draw(self, surface, **kwargs):
        if self.should_kill:
            return

        x, y = self.rect.center
        self.rect.center = x, y + 1

        surface.blit(self.image, self.rect.center)

        if y >= kwargs['height']:
            self.should_kill = True


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
