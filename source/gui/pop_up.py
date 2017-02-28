from element import Element


class PopUp(Element):

    def __init__(self, layout, pos, w, h):
        Element.__init__(self, layout, pos, w, h, 4)

    def motion(self, point):
        self.delete()

    def set_color(self):
        return 255, 255, 255

    def toggle_redraw(self):
        pass