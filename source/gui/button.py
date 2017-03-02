from element import Element
from ..constants import RED
from ..images.image import GUIImage


class Button(Element):

    """
    Button has function
    Button is bound to a panel or menu
    Button coord is relative to its location
    Button needs some context sensitve images etc.
    Button needs to be visible to controller objects
    """

    @classmethod
    def from_image(cls, img_name, layout, pos, func='default'):
        img = GUIImage(img_name)
        w = img.w
        h = img.h
        instance = cls(layout, pos, w, h, function=func)
        img.draw(instance.image)
        return instance

    @staticmethod
    def default():
        print 'No function bound to button'

    @staticmethod
    def close_function(instance, owner):
        instance.set_owner(owner)
        instance.perform_function = instance.close_owner
        return instance

    def close_owner(self, point):
        self.owner.delete()
        self.layout.refresh()
        
    def __init__(self, layout, pos, w, h, function='default'):

        self.owner = None
        self.function = self.set_function(function)
        Element.__init__(self, layout, pos, w, h, 1)

    def set_color(self):
        return RED

    @staticmethod
    def set_function(function):
        if function == 'default':
            return Button.default
        return function

    def perform_function(self, point):
        self.function()

    def hover(self, point):
        if self.point_is_over(point):
            pass


class CloseButton(Button):




    def __init__(self, owner, layout, pos, w, h):
        Button.__init__(self, layout, pos, w, h)
        self.owner = owner
        self.perform_function = self.close_owner


