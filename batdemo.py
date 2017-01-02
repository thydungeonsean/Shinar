import pygame
from pygame.locals import *

import code.states.battle as battle
import code.map.battlefield as batfield

from code.entities.troop import *
from code.map.battlefield import Row

# r = Row(1, 1, 1)
# t = Infantry(r, 'sean')
# a = Archer(r, 'sean')
# a = Chariot(r, 'sean')
# a = Infantry(r, 'sean')

pygame.init()
screen = pygame.display.set_mode((800, 600))

b = battle.Battle('s')
map = batfield.BattleField()
map_image = map.map_image



# screen.blit(map_image, map_image.get_rect())
# a.image.position((0, 0))
# a.draw(screen)

b.render()

pygame.display.update()
pygame.image.save(screen, 's.png')

while pygame.event.wait().type != KEYDOWN:
    pygame.time.wait(50)

