from pop_up import TextPopUp
from troop_display import TroopDisplay
from ..constants import *
from ..states.data_parser import *


class HoverComponent(object):

    STND_W = scale(100)

    def new_text_pop_up(self, *args):
        text_w = args[0]
        text = args[1]
        new = TextPopUp(text_w, text)
        self.owner.layout.add_element(new)
        self.element = new

    def new_troop_display(self, *args):
        troop = args[0]
        new = TroopDisplay(troop)
        self.owner.layout.add_element(new)
        self.element = new

    @classmethod
    def text_box(cls, owner, text, text_w='default'):
        instance = cls(owner)
        if text_w == 'default':
            text_w = cls.STND_W
        instance.hover_effect = cls.new_text_pop_up
        instance.args = (text_w, text)
        return instance

    @classmethod
    def troop_display(cls, owner, troop):
        instance = cls(owner)
        instance.hover_effect = cls.new_troop_display
        instance.args = (troop,)
        return instance

    def __init__(self, owner):
        self.owner = owner
        self.state = 0  # 0 - awaiting activation, 1 - hovering
        self.element = None
        self.args = None

    def hovering(self):
        if self.state == 1:
            pass
        elif self.state == 0:
            self.start_hover()  # TODO don't allow hover if element is not on it's owner panel
            self.state = 1

    def end_hover(self):
        if self.state == 1:
            self.element = None
            self.state = 0
            self.owner.layout.refresh()

    def start_hover(self):
        self.hover_effect(self, *self.args)

    def hover_effect(self, *args):
        raise NotImplementedError


def add_text_pop_up(element, text_key, width='default'):

    text = get_ui_text(text_key)
    h = HoverComponent.text_box(element, text, text_w=width)

    element.set_hover_component(h)

    return element


def add_troop_display(element, troop):

    h = HoverComponent.troop_display(element, troop)
    element.set_hover_component(h)

    return element
