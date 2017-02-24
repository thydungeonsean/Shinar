from panel import Panel
import pygame


class Element(Panel):

    """
    Element is visible to controller and can be interacted with
    """

    def __init__(self, layout, pos, w, h, layer):
        Panel.__init__(self, layout, pos, w, h, layer)
        
    def point_is_over(self, (px, py)):
        if self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h:
            return True
        return False

    def click(self, point):
        if self.point_is_over(point):
            self.perform_function()

    def perform_function(self):
        raise NotImplementedError
