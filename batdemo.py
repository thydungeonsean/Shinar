import os
import pygame
from pygame.locals import *
from code.constants import *

import code.states.battle as battle

from code.entities.troop import *
from code.map.battlefield import Row
from code.entities.army import Army


pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
screen = pygame.display.set_mode((SCREENW, SCREENH))

red = Army('a', RED, 4, 3, 2)
blue = Army('b', RIVER_BLUE, 1, 1, 5)

b = battle.Battle('s', red, blue)

clock = pygame.time.Clock()

for i in range(20):
    b.render()
    b.battlefield.grid.draw(screen)

    pygame.display.update()
    clock.tick(30)
    red.advance()
    blue.advance()


pygame.image.save(screen, 's.png')

while pygame.event.wait().type != KEYDOWN:
    pygame.time.wait(50)

