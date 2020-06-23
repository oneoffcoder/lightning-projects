import itertools
import os
import sys

import pygame
from pygame.constants import KEYUP, QUIT, K_SPACE, K_q, K_c

from objects import Ship, Bullet, RockGenerator, GameInfo, GameOverMessage


def get_remaining_objects(bullets, rocks, bullet_group, rock_group):
    collisions = pygame.sprite.groupcollide(bullet_group, rock_group, True, True)
    n_collisions = len(collisions)
    if n_collisions > 0:
        collided_bullets = set([b.uuid for b in collisions.keys()])
        bullets = [b for b in bullets if b.uuid not in collided_bullets]

        collided_rocks = set([r.uuid for r in itertools.chain(*collisions.values())])
        rocks = [r for r in rocks if r.uuid not in collided_rocks]
    return bullets, rocks, n_collisions


def get_remaining_rocks(ship, rocks, rock_group):
    collisions = pygame.sprite.spritecollide(ship, rock_group, True)
    n_collisions = len(collisions)
    if n_collisions > 0:
        collided_rocks = set([r.uuid for r in collisions])
        rocks = [r for r in rocks if r.uuid not in collided_rocks]
    return rocks, -n_collisions


def get_params():
    width = 500
    height = 400

    DISPLAYSURF = pygame.display.set_mode((width, height))
    DISPLAYSURF.fill((255, 255, 255))

    score = 0
    lives = 1

    return {
        'FPS': 30,
        'width': width,
        'height': height,
        'DISPLAYSURF': DISPLAYSURF,
        'fps_clock': pygame.time.Clock(),
        'score': score,
        'lives': lives,
        'bullets': [],
        'rocks': [],
        'bullet_group': pygame.sprite.Group(),
        'rock_group': pygame.sprite.Group(),
        'ship': Ship((width / 2, height - 50), 0.5),
        'rock_generator': RockGenerator(width, height),
        'game_info': GameInfo(score, lives)
    }


def quit_game():
    pygame.quit()
    sys.exit()


def start_game(**params):
    width, height = params['width'], params['height']
    ship = params['ship']
    score, lives = params['score'], params['lives']
    bullets, rocks = params['bullets'], params['rocks']
    bullet_group, rock_group = params['bullet_group'], params['rock_group']
    rock_generator = params['rock_generator']
    game_info = params['game_info']
    DISPLAYSURF = params['DISPLAYSURF']
    fps_clock, FPS = params['fps_clock'], params['FPS']

    while True:
        kwargs = {
            'width': width,
            'height': height,
            'keys': pygame.key.get_pressed(),
            'position': ship.get_center(),
            'score': score,
            'lives': lives
        }

        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
            elif event.type == KEYUP and event.key == K_SPACE:
                bullet = Bullet.instance(**kwargs)
                bullet_group.add(bullet)
                bullets.append(bullet)

        if rock_generator.should_generate():
            rock = rock_generator.next()
            rocks.append(rock)
            rock_group.add(rock)

        DISPLAYSURF.fill((255, 255, 255, 0))

        game_info.draw(DISPLAYSURF, **kwargs)
        ship.draw(DISPLAYSURF, **kwargs)

        for bullet in bullets:
            bullet.draw(DISPLAYSURF, **kwargs)

        for rock in rocks:
            rock.draw(DISPLAYSURF, **kwargs)

        bullets, rocks, points = get_remaining_objects(bullets, rocks, bullet_group, rock_group)
        score += points

        rocks, hits = get_remaining_rocks(ship, rocks, rock_group)
        lives += hits

        pygame.display.update()
        fps_clock.tick(FPS)

        if lives <= 0:
            break

    return score, lives


def show_game_over(**params):
    DISPLAYSURF = params['DISPLAYSURF']
    fps_clock, FPS = params['fps_clock'], params['FPS']
    width, height = params['width'], params['height']
    score, lives = params['score'], params['lives']

    message = GameOverMessage(width, height, score, lives)
    do_continue = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
            elif event.type == KEYUP:
                if event.key == K_q:
                    quit_game()
                elif event.key == K_c:
                    print('continue')
                    do_continue = True
                    break

        if do_continue:
            break

        DISPLAYSURF.fill((255, 255, 255, 0))

        message.draw(DISPLAYSURF)

        pygame.display.update()
        fps_clock.tick(FPS)

    return do_continue


def start():
    pygame.init()
    pygame.display.set_caption('Space Battle')

    while True:
        params = get_params()
        params['score'], params['lives'] = start_game(**params)

        do_continue = show_game_over(**params)
        if not do_continue:
            break

    quit_game()


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    start()
