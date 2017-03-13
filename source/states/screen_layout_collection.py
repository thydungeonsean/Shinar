from ..gui.screen_layout import ScreenLayout
from ..gui.panel import Panel
from ..gui.command_menu import CommandMenu
from ..gui.button import Button, CloseButton, MenuButton
from ..gui.drag_box import DragBox, FPSBox
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
        main_menu_button = MenuButton('MAIN MENU', function='make_pop_up')
        main_menu_button.move((MAIN_MENU_BUTTON_X, MAIN_MENU_BUTTON_Y))
        next_turn_button = MenuButton('NEXT TURN', function='end_command_phase')
        next_turn_button.move((NEXT_TURN_BUTTON_X, NEXT_TURN_BUTTON_Y))
        right_panel.attach_elements((main_menu_button, next_turn_button))

        # master command menu
        command_menu = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'commands', 5, 'COMMANDS', backbutton=False,
                                   tag='command').bind_layout(cls.BATTLE_LAYOUT)
        command_menu.attach_menu_buttons((MenuButton('DISPOSITION', function='open_disp'),
                                          MenuButton('GENERAL', function='open_general'),
                                          MenuButton('INFANTRY', function='open_infantry'),
                                          MenuButton('ARCHER', function='open_archer'),
                                          MenuButton('CHARIOT', function='open_chariot')))

        # command menus
        # disposition
        disposition_commands_panel = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'disposition_commands', 3,
                                                 'DISPOSITION', tag='command').bind_layout(cls.BATTLE_LAYOUT)

        disposition_commands_panel.attach_menu_buttons((MenuButton('INFANTRY'),
                                                        MenuButton('ARCHER'),
                                                        MenuButton('CHARIOT')))

        # general
        general_commands_panel = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'general_commands', 3, 'GENERAL',
                                             tag='command').bind_layout(cls.BATTLE_LAYOUT)
        general_commands_panel.attach_menu_buttons((MenuButton('MANEUVER'),
                                                    MenuButton('RALLY'),
                                                    MenuButton('REGROUP')))
        # infantry
        infantry_command_panel = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'infantry_commands', 2, 'INFANTRY',
                                             tag='command').bind_layout(cls.BATTLE_LAYOUT)
        infantry_command_panel.attach_menu_buttons((MenuButton('CHARGE'),
                                                    MenuButton('REFORM')))

        # archer
        archer_command_panel = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'archer_commands', 1, 'ARCHER',
                                           tag='command').bind_layout(cls.BATTLE_LAYOUT)
        archer_command_panel.attach_menu_buttons((MenuButton('FOCUS'),))

        # chariot
        chariot_command_panel = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'chariot_commands', 1, 'CHARIOT',
                                            tag='command').bind_layout(cls.BATTLE_LAYOUT)
        chariot_command_panel.attach_menu_buttons((MenuButton('RAID'),))

        # main menu
        #main_menu =


        # tests

        drag = DragBox((650, 20), 100, 100)
        fps = FPSBox((750, 550), 50, 50)
        # test2 = Button(cls.BATTLE_LAYOUT, (2, 2), 10, 10, function=make_pop_up)
        # test2 = Button.close_function(Button.from_image('close', cls.BATTLE_LAYOUT, (2, 2), func=make_pop_up), drag)
        button2 = MenuButton('Button', function='make_pop_up')
        drag.attach_element(button2)

        cls.BATTLE_LAYOUT.add_elements((top_frame, left_frame, bot_frame, right_frame, right_panel, fps))
        cls.BATTLE_LAYOUT.archive_elements((command_menu, disposition_commands_panel, general_commands_panel,
                                            infantry_command_panel, archer_command_panel, chariot_command_panel))
