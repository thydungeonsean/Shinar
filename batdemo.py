import os
import pygame
from pygame.locals import *
from tools.rand_dist import rand_dist
from source.constants import *

import source.battle.battle as battle
from source.entities.army import Army


pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
screen = pygame.display.set_mode((SCREENW, SCREENH))

i, a, c = rand_dist()
red = Army('a', RED, i, a, c)

i, a, c = rand_dist()
blue = Army('b', YELLOW, 2, 2, 4)

b = battle.Battle('s', red, blue)

clock = pygame.time.Clock()


def handle_input(phase):

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            else:
                phase.end_phase()


while True:
    b.render()
    # b.battlefield.grid.draw(screen)

    b.run()
    if b.scheduler.phase.name == 'end':
        handle_input(b.scheduler.phase)
        #b.scheduler.phase.end_phase()

    pygame.display.update()
    clock.tick(60)


pygame.image.save(screen, 's.png')

while pygame.event.wait().type != KEYDOWN:
    clock.tick(60)

