from ..gui.screen_layout import ScreenLayout
from ..gui.panel import Panel
from ..gui.element import PersistentPanel
from ..gui.command_menu import CommandMenu
from ..gui.button import Button, CloseButton, MenuButton
from ..gui.drag_box import DragBox
from ..gui.pop_up import PopUp

from ..constants import *


class ScreenLayoutCollection(object):

    BATTLE_LAYOUT = ScreenLayout()

    @classmethod
    def init_battle_layout(cls):

        # frame of battle view
        top_frame = Panel.base((0, 0), 2 * BATTLEFIELD_FRAME_W + BATTLEFIELD_W, BATTLEFIELD_FRAME_W)

        left_frame = Panel.base((0, BATTLEFIELD_FRAME_W), BATTLEFIELD_FRAME_W, BATTLEFIELD_H)

        bot_frame = Panel.base((0, SCREENH - BATTLEFIELD_FRAME_W), 2 * BATTLEFIELD_FRAME_W +
                               BATTLEFIELD_W, BATTLEFIELD_FRAME_W)

        right_frame = Panel.base((BATTLEFIELD_FRAME_W + BATTLEFIELD_W, BATTLEFIELD_FRAME_W),
                                 BATTLEFIELD_FRAME_W, BATTLEFIELD_H)

        # right panel

        right_panel = Panel.base((2 * BATTLEFIELD_FRAME_W + BATTLEFIELD_W, 0), COMMAND_PANEL_W, SCREENH).parent()

        #button1 = Button((10, 10), 20, 20, function=open_gen_com)
        #right_panel.attach_element(button1)

        # master command menu
        command_menu = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'commands', 5, backbutton=False)
        command_menu.attach_menu_buttons((MenuButton('DISPOSITION'),
                                          MenuButton('GENERAL'),
                                          MenuButton('INFANTRY'),
                                          MenuButton('ARCHER'),
                                          MenuButton('CHARIOT')))

        # command menus
        # disposition
        disposition_commands_panel = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'disposition_commands', 3)
        disposition_commands_panel.attach_menu_buttons((MenuButton('INFANTRY'),
                                                        MenuButton('ARCHER'),
                                                        MenuButton('CHARIOT')))

        # general
        general_commands_panel = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'general_commands', 3)
        general_commands_panel.attach_menu_buttons((MenuButton('MANEUVER'),
                                                    MenuButton('RALLY'),
                                                    MenuButton('REGROUP')))
        # infantry
        infantry_command_panel = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'infantry_commands', 2)
        infantry_command_panel.attach_menu_buttons((MenuButton('CHARGE'),
                                                    MenuButton('REFORM')))

        # archer
        archer_command_panel = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'archer_commands', 1)
        archer_command_panel.attach_menu_buttons((MenuButton('FOCUS'),))

        # chariot
        chariot_command_panel = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'chariot_commands', 1)
        chariot_command_panel.attach_menu_buttons((MenuButton('RAID'),))

        # main menu
        #main_menu =


        # tests

        drag = DragBox((650, 20), 100, 100)
        # test2 = Button(cls.BATTLE_LAYOUT, (2, 2), 10, 10, function=make_pop_up)
        # test2 = Button.close_function(Button.from_image('close', cls.BATTLE_LAYOUT, (2, 2), func=make_pop_up), drag)
        button2 = MenuButton('Button', function=make_pop_up)
        drag.attach_element(button2)

        cls.BATTLE_LAYOUT.add_elements((top_frame, left_frame, bot_frame, right_frame, right_panel, command_menu))
        cls.BATTLE_LAYOUT.archive_elements((disposition_commands_panel, general_commands_panel, infantry_command_panel,
                                            archer_command_panel, chariot_command_panel))


def make_pop_up():

    new = PopUp((40, 40), 100, 100)
    ScreenLayoutCollection.BATTLE_LAYOUT.add_element(new)


def open_gen_com():
    self = ScreenLayoutCollection.BATTLE_LAYOUT
    try:
        panel = self.inactive_elements['general_commands']
        del self.inactive_elements['general_commands']
        self.add_element(panel)
        panel.refresh_draw()
    except KeyError:
        print 'already open'

def open_command():
    self = ScreenLayoutCollection.BATTLE_LAYOUT
    try:
        panel = self.inactive_elements['general_commands']
        del self.inactive_elements['general_commands']
        self.add_element(panel)
        panel.refresh_draw()
    except KeyError:
        print 'already open'