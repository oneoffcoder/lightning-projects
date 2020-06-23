import os
import sys
import itertools

import pygame
from pygame.constants import KEYUP, QUIT, K_SPACE

from objects import Ship, Bullet, RockGenerator


def start():
    pygame.init()

    FPS = 30
    width = 500
    height = 400
    DISPLAYSURF = pygame.display.set_mode((width, height))
    DISPLAYSURF.fill((255, 255, 255))
    pygame.display.set_caption('Space Battle')
    fps_clock = pygame.time.Clock()

    bullets = []
    rocks = []

    bullet_group = pygame.sprite.Group()
    rock_group = pygame.sprite.Group()
    ship = Ship((width / 2, height - 50), 0.5)

    rock_generator = RockGenerator(width, height)

    while True:
        kwargs = {
            'width': width,
            'height': height,
            'keys': pygame.key.get_pressed(),
            'position': ship.get_center()
        }

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_SPACE:
                bullet = Bullet.instance(**kwargs)
                bullet_group.add(bullet)
                bullets.append(bullet)

        if rock_generator.should_generate():
            rock = rock_generator.next()
            rocks.append(rock)
            rock_group.add(rock)

        DISPLAYSURF.fill((255, 255, 255, 0))

        ship.draw(DISPLAYSURF, **kwargs)

        for bullet in bullets:
            bullet.draw(DISPLAYSURF, **kwargs)

        for rock in rocks:
            rock.draw(DISPLAYSURF, **kwargs)

        collisions = pygame.sprite.groupcollide(bullet_group, rock_group, True, True)
        if len(collisions) > 0:
            collided_bullets = set([b.uuid for b in collisions.keys()])
            bullets = [b for b in bullets if b.uuid not in collided_bullets]

            collided_rocks = set([r.uuid for r in itertools.chain(*collisions.values())])
            rocks = [r for r in rocks if r.uuid not in collided_rocks]

        collisions = pygame.sprite.spritecollide(ship, rock_group, True)
        if len(collisions):
            collided_rocks = set([r.uuid for r in collisions])
            rocks = [r for r in rocks if r.uuid not in collided_rocks]

        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    start()
