from ..entities.coord import Coord
import pygame
from ..constants import *


class Panel(object):

    """
    Panel doesn't normally need redraw
    Panel coord is relative to screen
    Panel has no functions
    """

    @classmethod
    def element_panel(cls, layout, (x, y), w, h, layer):
        instance = cls(layout, (x, y), w, h, layer)
        instance.init_element_list()
        return instance
    
    def __init__(self, layout, (x, y), w, h, layer):

        self.layout = layout

        self.coord = Coord(x, y)
        self.w = w
        self.h = h

        self.layer = layer

        self.owner = None

        self.element_list = None

        self.needs_redraw = True
        self.color = self.set_color()
        self.image, self.rect = self.set_basic_image()

    def set_color(self):
        return RIVER_BLUE

    def set_basic_image(self):
        image = pygame.Surface((self.w, self.h))
        image.fill(self.color)
        image = image.convert()
        rect = image.get_rect()
        rect.topleft = self.x, self.y
        return image, rect

    def reset_pos(self):
        self.rect.topleft = self.x, self.y

    @property
    def x(self):
        return self.coord.x + self.owner_x

    @property
    def y(self):
        return self.coord.y + self.owner_y

    @property
    def owner_x(self):
        if self.owner is None:
            return 0
        return self.owner.x

    @property
    def owner_y(self):
        if self.owner is None:
            return 0
        return self.owner.y

    def init_element_list(self):
        self.element_list = []
        
    def attach_element(self, element):
        self.element_list.append(element)
        element.set_owner(self)

    def set_owner(self, owner):
        self.owner = owner
        self.reset_pos()

    def draw(self, surface):
        if self.needs_redraw:
            surface.blit(self.image, self.rect)
            self.toggle_redraw()
        if self.element_list is not None:
            for element in self.element_list:
                element.draw(surface)

    def toggle_redraw(self):
        self.needs_redraw = False

    def refresh(self):
        self.needs_redraw = True
