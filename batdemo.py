import os
import pygame
from pygame.locals import *
from code.constants import *

import code.states.battle as battle

from code.entities.troop import *
from code.entities.army import Army


pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
screen = pygame.display.set_mode((SCREENW, SCREENH))

red = Army('a', RED, 5, 3, 2)
blue = Army('b', RIVER_BLUE, 5, 5, 0)

b = battle.Battle('s', red, blue)

clock = pygame.time.Clock()


for i in range(480):
    b.render()
    # b.battlefield.grid.draw(screen)
    b.run()

    pygame.display.update()
    clock.tick(60)
    # x = True
    # while x:
    #     key = pygame.event.wait()
    #     if key.type == KEYDOWN:
    #         if key.key == K_ESCAPE:
    #             quit()
    #         x = False
    #         clock.tick(60)


pygame.image.save(screen, 's.png')

while pygame.event.wait().type != KEYDOWN:
    clock.tick(60)

