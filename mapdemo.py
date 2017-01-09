import pygame
from source.map.map_tools import *
from pygame.locals import *
from source.map.map import Map
from source.map.map_image import MapImageGenerator


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

