import pygame
from code.map.map_tools import *
from pygame.locals import *
from code.map.map import Map
from code.map.map_image import MapImageGenerator
import code.states.battle as battle
import code.map.battlefield as batfield

b = battle.Battle()
bf = batfield.BattleField()

pygame.init()
screen = pygame.display.set_mode((800, 600))

map = Map.load_map_file('map.txt')

m_gen = MapImageGenerator.get_instance()
map_image = m_gen.generate_image(map)

screen.blit(map_image, map_image.get_rect())
pygame.display.update()
pygame.image.save(screen, 's.png')

while pygame.event.wait().type != KEYDOWN:
    pygame.time.wait(50)

