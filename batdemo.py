import os
import pygame
from pygame.locals import *
from code.constants import *

import code.states.battle as battle

from code.entities.troop import *
from code.entities.army import Army
import code.states.battle_scheduler as bsched

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
screen = pygame.display.set_mode((SCREENW, SCREENH))

red = Army('a', RED, 4, 3, 2)
blue = Army('b', RIVER_BLUE, 1, 1, 5)

b = battle.Battle('s', red, blue)

BS = bsched.BattleScheduler(b)

clock = pygame.time.Clock()

for i in range(121):
    b.render()
    b.battlefield.grid.draw(screen)
    BS.run()

    pygame.display.update()
    clock.tick(60)
    # x=True
    # while x:
    #     key = pygame.event.wait()
    #     if key.type == KEYDOWN:
    #         if key.key == K_ESCAPE:
    #             quit()
    #         x = False
    #         clock.tick(60)
    #red.advance()
    #blue.advance()


pygame.image.save(screen, 's.png')

while pygame.event.wait().type != KEYDOWN:
    pygame.time.wait(50)

