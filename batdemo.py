import os
import pygame
from pygame.locals import *
from source.states.clock import Clock
from tools.rand_dist import rand_dist
from source.constants import *

import source.battle.battle as battle
from source.entities.army import Army
from source.player.player import Player


pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
screen = pygame.display.set_mode((SCREENW, SCREENH))

i, a, c = rand_dist()
red_player = Player('Sean', 'human', RED)
red = Army(red_player, i, a, c)

i, a, c = rand_dist()
player_b = Player('Nebuchadnezzar', 'ai', YELLOW)
blue = Army(player_b, 2, 2, 4)

b = battle.Battle('s', red, blue)

clock = Clock.get_instance()


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
    b.handle_input()

    pygame.display.update()
    clock.tick(60)


pygame.image.save(screen, 's.png')

while pygame.event.wait().type != KEYDOWN:
    clock.tick(60)

