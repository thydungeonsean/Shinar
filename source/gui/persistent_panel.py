from element import Element
from ..constants import LT_GREY


class PersistentPanel(Element):

    @classmethod
    def wrap_button(cls, button, pos, layer, id_key, **kwargs):
        w = button.w
        h = button.h
        return cls(pos, w, h, layer, id_key, **kwargs)

    def __init__(self, pos, w, h, layer, id_key, **kwargs):
        Element.__init__(self, pos, w, h, layer)
        self.id_key = id_key
        self.persistent = True
        self.tag = kwargs.get('tag')

    def delete(self):

        self.layout.remove_element(self)
        if self.element_list is not None:
            for element in self.element_list:
                self.layout.remove_element(element)

        self.layout.archive_element(self)

    def set_color(self):
        return LT_GREY

    def perform_function(self, dummy):
        pass
