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
    def base(cls, pos, w, h):
        instance = cls(pos, w, h, 0)
        return instance

    @classmethod
    def from_image(cls, img_name, pos, layer):
        img = GUIImage(img_name)
        w = img.w
        h = img.h
        instance = cls(pos, w, h, layer)
        img.draw(instance.image)
        return instance

    # decorator methods - call on construction
    def parent(self):
        self.init_element_list()
        return self

    def __init__(self, (x, y), w, h, layer):

        self.coord = Coord(x, y)
        self.w = w
        self.h = h

        self.layer = layer

        self.owner = None
        self.element_list = None
        self.layout = None

        self.interactive = False
        self.persistent = False

        self.needs_redraw = True
        self.color = self.set_color()
        self.image, self.rect = self.set_basic_image()

    # setters
    def set_layout(self, layout):
        self.layout = layout
        if self.element_list is not None:
            for element in self.element_list:
                element.set_layout(layout)

    def set_owner(self, owner):
        self.owner = owner
        self.reset_pos()
        self.layer = owner.layer + 1

    def init_element_list(self):
        self.element_list = []

    def set_color(self):
        return RIVER_BLUE

    def set_basic_image(self):
        image = pygame.Surface((self.w, self.h))
        image.fill(self.color)
        image = image.convert()
        rect = image.get_rect()
        rect.topleft = self.x, self.y
        return image, rect

    # positional methods and properties
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

    def move(self, (x, y)):
        self.coord.set((x, y))
        self.reset_pos()

    def reset_pos(self):
        self.rect.topleft = self.x, self.y
        if self.element_list is not None:
            for element in self.element_list:
                element.reset_pos()

    # membership methods
    def attach_element(self, element):
        self.element_list.append(element)
        element.set_owner(self)
        if self.layout is not None:
            element.set_layout(self.layout)

    def attach_elements(self, elements):
        for element in elements:
            self.attach_element(element)

    def delete(self):
        self.layout.remove_element(self)
        if self.element_list is not None:
            for element in self.element_list:
                self.layout.remove_element(element)

    # draw methods
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
