from ..entities.coord import Coord
import pygame
from ..constants import *
from ..images.image import GUIImage


class Panel(object):

    """
    Panel doesn't normally need redraw
    Panel coord is relative to screen
    Panel has no functions
    """

    @classmethod
    def base(cls, layout, pos, w, h):
        instance = cls(layout, pos, w, h, 0)
        return instance

    @classmethod
    def from_image(cls, img_name, layout, pos, layer):
        img = GUIImage(img_name)
        w = img.w
        h = img.h
        instance = cls(layout, pos, w, h, layer)
        img.draw(instance.image)
        return instance

    # decorator methods - call on an instance of class to modify it
    @staticmethod
    def parent(instance):
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

        self.interactive = False

        self.needs_redraw = True
        self.color = self.set_color()
        self.image, self.rect = self.set_basic_image()

    def delete(self):
        self.layout.remove_element(self)
        if self.element_list is not None:
            for element in self.element_list:
                self.layout.remove_element(element)

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
        if self.element_list is not None:
            for element in self.element_list:
                element.reset_pos()

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
        # element.toggle_redraw = self.toggle_redraw

    def set_owner(self, owner):
        self.owner = owner
        self.reset_pos()
        self.layer = owner.layer + 1

    def draw(self, surface):
        if self.needs_redraw:
            surface.blit(self.image, self.rect)
            self.toggle_redraw()
        if self.element_list is not None:
            for element in self.element_list:
                element.forced_draw(surface)

    def forced_draw(self, surface):  # forced draw - no conditions
        surface.blit(self.image, self.rect)

    def toggle_redraw(self):
        self.needs_redraw = False

    def refresh_draw(self):
        self.needs_redraw = True
