from panel import Panel
import pygame
from ..constants import LT_GREY


class Element(Panel):

    """
    Element is visible to controller and can be interacted with
    """

    def __init__(self, pos, w, h, layer):
        Panel.__init__(self, pos, w, h, layer)
        self.interactive = True

    def point_is_over(self, (px, py)):
        if self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h:
            return True
        return False

    def click(self, point):
        if self.point_is_over(point):
            self.perform_function(self)
        else:
            return 0

    def right_click(self, point):
        return 0

    def motion(self, point):
        pass

    def button_up(self):
        pass

    def hover(self, point):
        pass

    def perform_function(self, dummy):
        raise NotImplementedError


class PersistentPanel(Element):

    def __init__(self, pos, w, h, layer, id_key):
        Element.__init__(self, pos, w, h, layer)
        self.id_key = id_key
        self.persistent = True

    def delete(self):

        self.layout.remove_element(self)
        if self.element_list is not None:
            for element in self.element_list:
                self.layout.remove_element(element)

        self.layout.archive_element(self)

    def set_color(self):
        return LT_GREY

    def perform_function(self, dummy):
        pass
