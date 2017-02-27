from panel import Panel
import pygame


class Element(Panel):

    """
    Element is visible to controller and can be interacted with
    """

    def __init__(self, layout, pos, w, h, layer):
        Panel.__init__(self, layout, pos, w, h, layer)
        self.interactive = True

    def point_is_over(self, (px, py)):
        if self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h:
            return True
        return False

    def click(self, point):
        if self.point_is_over(point):
            self.perform_function(point)
        else:
            return 0

    def right_click(self, point):
        return 0

    def motion(self, point):
        pass

    def button_up(self):
        pass

    def perform_function(self, point):
        raise NotImplementedError
