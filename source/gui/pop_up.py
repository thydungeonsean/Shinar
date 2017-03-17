from element import Element
from text_box import TextBox


class PopUp(Element):

    def __init__(self, pos, w, h):
        Element.__init__(self, pos, w, h, 6)

    def motion(self, point):
        self.delete()

    def set_color(self):
        return 255, 255, 255

    def toggle_redraw(self):
        pass


class TextPopUp(PopUp):

    def __init__(self, pos, w, text):
        self.text = text
        self.text_box = TextBox(w, self.text)
        h = self.text_box.h
        PopUp.__init__(self, pos, w, h)
        self.text_box.draw(self.image)

    def perform_function(self, dummy):
        pass

