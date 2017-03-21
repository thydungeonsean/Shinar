import element
from text_box import TextBox
from box_border import BoxBorder
from ..controller.mouse import Mouse
from ..controller.click_subscriber import ClickSubscriber
from ..constants import scale, SCREENW, SCREENH


class PopUp(element.Element):

    def __init__(self, pos, w, h):
        element.Element.__init__(self, pos, w, h, 6)
        self.mouse_sub = self.get_mouse_subscriptions()

    def get_mouse_subscriptions(self):

        observer = Mouse.get_instance().click_observer
        subscription = ClickSubscriber.close_element_sub(self, observer)

        return subscription

    def delete(self):
        self.layout.remove_element(self)
        if self.element_list is not None:
            for element in self.element_list:
                self.layout.remove_element(element)
        self.layout.refresh()
        self.mouse_sub.unsubscribe()

    def motion(self, point):
        self.delete()

    def toggle_redraw(self):
        pass


class TextPopUp(PopUp):

    STND_W = scale(50)

    def __init__(self, t_w, text):
        self.text = text
        self.text_box = TextBox(t_w, self.text)
        self.border = BoxBorder.frame_box(self.text_box)

        w = self.border.w
        h = self.border.h

        pos = self.get_mouse_pos()

        PopUp.__init__(self, pos, w, h)
        self.border.draw(self.image)
        self.text_box.draw(self.image)

        # self.image.set_alpha(200)

    def perform_function(self, dummy):
        pass

    def get_mouse_pos(self):
        mx, my = Mouse.get_instance().position

        if mx + self.border.w > SCREENW:
            x = mx - self.border.w - scale(1)
        else:
            x = mx + scale(1)

        if my + self.border.h > SCREENH:
            y = my - self.border.h
        else:
            y = my

        return x, y
