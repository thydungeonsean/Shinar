from element import Element
from ..constants import FERTILE_GREEN


class DragBox(Element):

    def __init__(self, pos, w, h):
        Element.__init__(self, pos, w, h, 4)
        self.parent()
        self.state = 0
        self.anchor_x = 0
        self.anchor_y = 0

    def set_color(self):
        return FERTILE_GREEN

    def perform_function(self, (mx, my)):
        if self.state == 0:
            self.state = 1
            self.anchor_x = self.x - mx
            self.anchor_y = self.y - my

    def button_up(self):
        if self.state == 1:
            self.state = 0
            self.anchor_x = 0
            self.anchor_y = 0

    def motion(self, pos):
        if self.state == 1:
            self.coord.set(self.anchored_coord(pos))
            self.reset_pos()
            self.layout.refresh()  # TODO - might be too inefficient if redrawing all GUI is slow

    def anchored_coord(self, (x, y)):
        return x + self.anchor_x, y + self.anchor_y

    def toggle_redraw(self):
        pass
