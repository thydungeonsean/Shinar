from element import PersistentPanel
from button import CloseButton, MenuButton
from menu_grid import MenuGrid
from ..constants import COMMAND_PANEL_W, scale


class CommandMenu(PersistentPanel):

    GAP = scale(5)

    def __init__(self, pos, layer, id_key, num_buttons, backbutton=True, layout=None):

        self.num_buttons = num_buttons
        w, h = self.set_dimensions()

        PersistentPanel.__init__(self, pos, w, h, layer, id_key, layout=layout)
        self.menu_grid = MenuGrid(self, MenuButton.COMMAND_W, MenuButton.COMMAND_H)

        self.parent()
        if backbutton:
            self.attach_back_button()

    def set_dimensions(self):
        h = self.num_buttons * MenuButton.COMMAND_H + (((self.num_buttons+3) * CommandMenu.GAP) +
                                                       CloseButton.BACK_BUTTON_H)

        return COMMAND_PANEL_W, h

    def get_back_button_coord(self):

        w = self.w - CloseButton.BACK_BUTTON_W - CommandMenu.GAP
        h = self.h - CloseButton.BACK_BUTTON_H - CommandMenu.GAP

        return w, h

    def attach_back_button(self):
        button = CloseButton(self, self.get_back_button_coord(), CloseButton.BACK_BUTTON_W, CloseButton.BACK_BUTTON_H)
        self.attach_element(button)

    def attach_menu_buttons(self, buttons):
        i = 0
        for button in buttons:
            self.attach_element(button)
            self.menu_grid.position_button(i, button)
            i += 1

