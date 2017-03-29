from ..gui.screen_layout import ScreenLayout
from ..gui.panel import Panel
from ..gui.command_menu import CommandMenu
from ..gui.button import MenuButton
from ..gui.drag_box import DragBox, FPSBox
from ..gui.persistent_panel import PersistentPanel
from ..gui.hover_component import *

from ..constants import *


def dummy():
    pass

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

        right_panel = Panel.base((RIGHT_PANEL_X, 0), COMMAND_PANEL_W, SCREENH).parent()
        main_menu_button = MenuButton('MAIN MENU', function='make_pop_up')
        main_menu_button.move((MAIN_MENU_BUTTON_X, MAIN_MENU_BUTTON_Y))
        right_panel.attach_element(main_menu_button)

        # skip command button - only player command phase

        skip_turn_button = MenuButton('SKIP COMMAND', function='end_command_phase')
        skip_button_panel = PersistentPanel.wrap_button(skip_turn_button, (NEXT_TURN_BUTTON_X, NEXT_TURN_BUTTON_Y), 2,
                                                        'skip_command', tag='command').bind_layout(cls.BATTLE_LAYOUT)\
            .parent()
        skip_button_panel.attach_element(skip_turn_button)

        # master command menu
        command_menu = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'commands', 5, 'COMMANDS', backbutton=False,
                                   tag='command').bind_layout(cls.BATTLE_LAYOUT)

        command_menu.attach_menu_buttons((add_text_pop_up(MenuButton('DISPOSITION', function='open_disp'), 'disp'),
                                          add_text_pop_up(MenuButton('GENERAL', function='open_general'), 'general'),
                                          add_text_pop_up(MenuButton('INFANTRY', function='open_infantry'), 'infantry'),
                                          add_text_pop_up(MenuButton('ARCHER', function='open_archer'), 'archer'),
                                          add_text_pop_up(MenuButton('CHARIOT', function='open_chariot'), 'chariot')))

        # command menus
        # disposition
        disposition_commands_panel = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'disposition_commands', 3,
                                                 'DISPOSITION', tag='command').bind_layout(cls.BATTLE_LAYOUT)

        disposition_commands_panel.attach_menu_buttons((
                                add_text_pop_up(MenuButton('INFANTRY', function='open_inf_disp'), ''),
                                add_text_pop_up(MenuButton('ARCHER', function='open_arch_disp'), ''),
                                add_text_pop_up(MenuButton('CHARIOT', function='open_char_disp'), '')))

        # disposition sub menus
        infantry_disposition = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'inf_disp', 2, 'INFANTRY', tag='command'
                                           ).bind_layout(cls.BATTLE_LAYOUT)

        archer_disposition = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'arch_disp', 2, 'ARCHER', tag='command'
                                         ).bind_layout(cls.BATTLE_LAYOUT)

        chariot_disposition = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'char_disp', 2, 'CHARIOT', tag='command'
                                          ).bind_layout(cls.BATTLE_LAYOUT)

        # general
        general_commands_panel = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'general_commands', 3, 'GENERAL',
                                             tag='command').bind_layout(cls.BATTLE_LAYOUT)
        general_commands_panel.attach_menu_buttons((add_text_pop_up(MenuButton('MANEUVER'), 'maneuver'),
                                                    add_text_pop_up(MenuButton('RALLY'), 'rally'),
                                                    add_text_pop_up(MenuButton('REGROUP'), 'regroup')))
        # infantry
        infantry_command_panel = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'infantry_commands', 3, 'INFANTRY',
                                             tag='command').bind_layout(cls.BATTLE_LAYOUT)
        infantry_command_panel.attach_menu_buttons((add_text_pop_up(MenuButton('CHARGE'), 'charge'),
                                                    add_text_pop_up(MenuButton('REFORM'), 'reform'),
                                                    add_text_pop_up(MenuButton('RESURGE'), 'resurge')))

        # archer
        archer_command_panel = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'archer_commands', 2, 'ARCHER',
                                           tag='command').bind_layout(cls.BATTLE_LAYOUT)
        archer_command_panel.attach_menu_buttons((add_text_pop_up(MenuButton('FOCUS'), 'focus'),
                                                  add_text_pop_up(MenuButton('BARRAGE'), 'barrage')))

        # chariot
        chariot_command_panel = CommandMenu((right_panel.x, COMMAND_PANEL_Y), 2, 'chariot_commands', 1, 'CHARIOT',
                                            tag='command').bind_layout(cls.BATTLE_LAYOUT)
        chariot_command_panel.attach_menu_buttons((add_text_pop_up(MenuButton('RAID'), 'raid'),))

        # main menu
        # main_menu =

        # tests
        fps = FPSBox((750, 550))

        cls.BATTLE_LAYOUT.add_elements((top_frame, left_frame, bot_frame, right_frame, right_panel,
                                        fps))
        cls.BATTLE_LAYOUT.archive_elements((skip_button_panel, command_menu, disposition_commands_panel,
                                            general_commands_panel, infantry_command_panel, archer_command_panel,
                                            chariot_command_panel, infantry_disposition, archer_disposition,
                                            chariot_disposition))

