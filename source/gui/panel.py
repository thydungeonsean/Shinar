from ..entities.coord import Coord
import pygame
from ..constants import *


class Panel(object):

    """
    Panel doesn't normally need redraw
    Panel coord is relative to screen
    Panel has no functions
    """

    def __init__(self, (x, y), w, h):
        self.coord = Coord(x, y)
        self.w = w
        self.h = h
        self.needs_redraw = True
        self.color = self.set_color()
        self.image, self.rect = self.set_basic_image()

    def set_color(self):
        return RIVER_BLUE

    @property
    def x(self):
        return self.coord.x

    @property
    def y(self):
        return self.coord.y

    def draw(self, surface):
        if self.needs_redraw:
            surface.blit(self.image, self.rect)
            self.toggle_redraw()

    def toggle_redraw(self):
        self.needs_redraw = False

    def refresh(self):
        self.needs_redraw = True

    def set_basic_image(self):
        image = pygame.Surface((self.w, self.h))
        image.fill(self.color)
        image = image.convert()
        rect = image.get_rect()
        rect.topleft = self.x, self.y
        return image, rect
