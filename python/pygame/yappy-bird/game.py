import os
import sys

import pygame
from pygame.constants import QUIT, K_SPACE

from objects import Bird, Pipe, PipeGenerator


def quit_game():
    pygame.quit()
    sys.exit()


def get_params():
    width = 900
    height = 600

    DISPLAYSURF = pygame.display.set_mode((width, height))
    DISPLAYSURF.fill((255, 255, 255))

    score = 0

    return {
        'FPS': 30,
        'width': width,
        'height': height,
        'DISPLAYSURF': DISPLAYSURF,
        'fps_clock': pygame.time.Clock(),
        'score': score,
        'pipes': [],
        'pipe_group': pygame.sprite.Group(),
        'bird': Bird((width / 10.0, height / 2.0))
    }


def start_game(**params):
    width, height = params['width'], params['height']
    bird = params['bird']
    score = params['score']
    pipes = params['pipes']
    pipe_group = params['pipe_group']
    DISPLAYSURF = params['DISPLAYSURF']
    fps_clock, FPS = params['fps_clock'], params['FPS']

    started = False
    pipe_gen = PipeGenerator()

    while True:
        if not started:
            started = pygame.key.get_pressed()[K_SPACE]

        kwargs = {
            'width': width,
            'height': height,
            'keys': pygame.key.get_pressed(),
            'score': score,
            'started': started
        }

        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()

        DISPLAYSURF.fill((255, 255, 255, 0))

        if pipe_gen.should_generate() and started:
            t_pipe, b_pipe = pipe_gen.next(**kwargs)
            pipes.extend([t_pipe, b_pipe])
            pipe_group.add(t_pipe)
            pipe_group.add(b_pipe)

        bird.draw(DISPLAYSURF, **kwargs)

        for pipe in pipes:
            pipe.draw(DISPLAYSURF, **kwargs)

        pygame.display.update()
        fps_clock.tick(FPS)

        collisions = pygame.sprite.spritecollide(bird, pipes, False)
        n_collisions = len(collisions)
        if n_collisions > 0:
            break


def start():
    pygame.init()
    pygame.display.set_caption('Yappy Bird')

    params = get_params()
    start_game(**params)


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    start()

