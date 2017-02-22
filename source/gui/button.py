from element import Element
from ..constants import RED


class Button(Element):

    """
    Button has function
    Button is bound to a panel or menu
    Button coord is relative to its location
    Button needs some context sensitve images etc.
    Button needs to be visible to controller objects
    """

    @staticmethod
    def default():
        print 'No function bound to button'

    def __init__(self, owner, pos, w, h, function='default'):

        self.owner = owner
        self.function = self.set_function(function)
        Element.__init__(self, pos, w, h)

    def set_color(self):
        return RED

    @staticmethod
    def set_function(function):
        if function == 'default':
            return Button.default
        return function

    """ button is always placed on an owning panel or element
    so it overwrites its x, y topleft coord to be relative to
    it's owner's x, y
    """
    @property
    def x(self):
        return self.owner.x + self.coord.x

    @property
    def y(self):
        return self.owner.y + self.coord.y

    def perform_function(self):
        self.function()
