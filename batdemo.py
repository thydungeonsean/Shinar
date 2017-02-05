import os
import pygame
from pygame.locals import *
from source.constants import *

import source.battle.battle as battle

from source.entities.troop import *
from source.entities.army import Army


pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
screen = pygame.display.set_mode((SCREENW, SCREENH))

red = Army('a', RED, 3, 5, 2)
blue = Army('b', YELLOW, 4, 4, 0)

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
    b.battlefield.grid.draw(screen)

    b.run()
    if b.scheduler.phase.name == 'end':
        handle_input(b.scheduler.phase)
        pass

    pygame.display.update()
    clock.tick(60)


pygame.image.save(screen, 's.png')

while pygame.event.wait().type != KEYDOWN:
    clock.tick(60)

