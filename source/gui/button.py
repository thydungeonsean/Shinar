from element import Element
from ..constants import RED, scale, COMMAND_PANEL_W
from ..images.image import GUIImage
from font import MenuFont
from functions.function_archive import function_archive


class Button(Element):

    """
    Button has function
    Button is bound to a panel or menu
    Button coord is relative to its location
    Button needs some context sensitve images etc.
    Button needs to be visible to controller objects
    """

    COMMAND_W = COMMAND_PANEL_W - scale(10)
    COMMAND_H = scale(15)

    SMALL_W = scale(10)
    SMALL_H = scale(10)

    # @classmethod
    # def command_size(cls, pos, func='default', layout=None):
    #     instance = cls(pos, cls.COMMAND_W, cls.COMMAND_H, function=func, layout=layout)
    #     return instance

    # @classmethod
    # def small_size(cls, pos, func='default', layout=None):
    #     instance = cls(pos, cls.SMALL_W, cls.SMALL_H, function=func, layout=layout)
    #     return instance

    @classmethod
    def from_image(cls, img_name, pos, func=None, layout=None):
        img = GUIImage(img_name)
        w = img.w
        h = img.h
        instance = cls(pos, w, h, function=func, layout=layout)
        img.draw(instance.image)
        return instance

    @staticmethod
    def default(self):
        print 'No function bound to button'

    # @staticmethod
    # def close_function(instance, owner):
    #     instance.set_owner(owner)
    #     instance.perform_function = instance.close_owner
    #     return instance

    # def close_owner(self, point):
    #     self.owner.delete()
    #     self.layout.refresh()
        
    def __init__(self, pos, w, h, function=None):

        self.owner = None
        self.perform_function = self.set_function(function)
        Element.__init__(self, pos, w, h, 1)

    def set_color(self):
        return RED

    def set_function(self, function):
        if function is None:
            return Button.default
        return self.get_archived_function(function)

    def perform_function(self):
        pass

    def hover(self, point):
        if self.point_is_over(point):
            pass

    def draw_text(self, text):
        f = MenuFont.get_instance()
        f.draw(self.image, (scale(2), scale(-4)), text)

    def get_archived_function(self, key):
        return function_archive[key]


class CloseButton(Button):

    BACK_BUTTON_W = scale(40)
    BACK_BUTTON_H = scale(12)

    CLOSE_BUTTON_W = scale(25)
    CLOSE_BUTTON_H = scale(25)

    def __init__(self, owner, pos, w, h):
        Button.__init__(self, pos, w, h)
        self.owner = owner
        self.perform_function = self.get_archived_function('back_command')


class MenuButton(Button):

    def __init__(self, text, function=None):

        Button.__init__(self, (0, 0), Button.COMMAND_W, Button.COMMAND_H, function=function)
        self.draw_text(text)
