from element import Element
from ..constants import scale, COMMAND_PANEL_W
from ..images.image import GUIImage
from font import MenuFont
from functions.function_archive import function_archive
from graphics.panel_image import PanelImage


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
        
    def __init__(self, pos, w, h, function=None, text=None, **kwargs):

        self.owner = None
        self.perform_function = self.set_function(function)
        Element.__init__(self, pos, w, h, 1, **kwargs)

        self.state = 0
        self.images = self.set_state_images(text)
        self.change_image()

    def set_function(self, function):
        if function is None:
            return Button.default
        return self.get_archived_function(function)

    def click(self, point):
        if self.state == 1:
            return 0
        if self.point_is_over(point):
            if self.owner is None:
                self.perform_function(self)
                self.set_state_to_clicked()
            elif self.owner.point_is_over(point):
                self.perform_function(self)
                self.set_state_to_clicked()
            else:
                return 0
        else:
            return 0

    def set_state_to_clicked(self):
        self.state = 1
        self.change_image()

    def perform_function(self):
        pass

    def draw_text(self, text, dest='def'):
        f = MenuFont.get_instance()
        if dest == 'def':
            dest = self.image
        f.draw(dest, (scale(2), scale(-4)), text)

    def get_archived_function(self, key):
        return function_archive[key]

    def set_state_images(self, text=None):

        images = {}

        for i in range(0, 2):
            image = PanelImage(self.w, self.h, style=i+1).image
            if text is not None:
                self.draw_text(text, dest=image)
            images[i] = image

        return images

    def change_image(self):
        self.image.blit(self.images[self.state], self.images[self.state].get_rect())


class CloseButton(Button):

    BACK_BUTTON_W = scale(40)
    BACK_BUTTON_H = scale(12)

    CLOSE_BUTTON_W = scale(25)
    CLOSE_BUTTON_H = scale(25)

    def __init__(self, owner, pos, w, h, **kwargs):
        Button.__init__(self, pos, w, h, text='BACK', **kwargs)
        self.owner = owner
        self.perform_function = self.get_archived_function('back_command')


class MenuButton(Button):

    def __init__(self, text, function=None, **kwargs):

        Button.__init__(self, (0, 0), Button.COMMAND_W, Button.COMMAND_H, function=function, text=text, **kwargs)
