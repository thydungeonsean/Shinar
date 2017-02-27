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
