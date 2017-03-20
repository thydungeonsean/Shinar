from element import Element
from text_box import TextBox
from box_border import BoxBorder
from ..controller.mouse import Mouse
from ..controller.click_subscriber import ClickSubscriber


class PopUp(Element):

    def __init__(self, pos, w, h):
        Element.__init__(self, pos, w, h, 6)
        self.mouse_sub = self.get_mouse_subscriptions()

    def get_mouse_subscriptions(self):

        observer = Mouse.get_instance().click_observer
        subscription = ClickSubscriber.close_element_sub(self, observer)

        return subscription

    def motion(self, point):
        #self.delete()
        pass

    def toggle_redraw(self):
        pass


class TextPopUp(PopUp):

    def __init__(self, pos, t_w, text):
        self.text = text
        self.text_box = TextBox(t_w, self.text)
        self.border = BoxBorder.frame_box(self.text_box)

        w = self.border.w
        h = self.border.h
        PopUp.__init__(self, pos, w, h)
        self.border.draw(self.image)
        self.text_box.draw(self.image)

        # self.image.set_alpha(200)

    def perform_function(self, dummy):
        pass

