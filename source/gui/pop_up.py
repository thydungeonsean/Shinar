from element import Element


class PopUp(Element):

    def __init__(self, pos, w, h):
        Element.__init__(self, pos, w, h, 6)

    def motion(self, point):
        self.delete()

    def set_color(self):
        return 255, 255, 255

    def toggle_redraw(self):
        pass
