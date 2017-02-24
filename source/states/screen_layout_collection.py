from ..gui.screen_layout import ScreenLayout
from ..gui.panel import Panel
from ..gui.button import Button

from ..constants import *


class ScreenLayoutCollection(object):

    BATTLE_LAYOUT = ScreenLayout()

    @classmethod
    def init_battle_layout(cls):

        top_frame = Panel(cls.BATTLE_LAYOUT, (0, 0), 2 * BATTLEFIELD_FRAME_W + BATTLEFIELD_W, BATTLEFIELD_FRAME_W, 0)

        left_frame = Panel(cls.BATTLE_LAYOUT, (0, BATTLEFIELD_FRAME_W), BATTLEFIELD_FRAME_W, BATTLEFIELD_H, 0)

        bot_frame = Panel(cls.BATTLE_LAYOUT, (0, SCREENH - BATTLEFIELD_FRAME_W), 2 * BATTLEFIELD_FRAME_W +
                          BATTLEFIELD_W, BATTLEFIELD_FRAME_W, 0)

        right_frame = Panel(cls.BATTLE_LAYOUT, (BATTLEFIELD_FRAME_W + BATTLEFIELD_W, BATTLEFIELD_FRAME_W),
                            BATTLEFIELD_FRAME_W, BATTLEFIELD_H, 0)

        right_panel = Panel.element_panel(cls.BATTLE_LAYOUT, (2 * BATTLEFIELD_FRAME_W + BATTLEFIELD_W, 0),
                            SCREENW - (2 * BATTLEFIELD_FRAME_W + BATTLEFIELD_W),
                            SCREENH, 0)

        test = Button(cls.BATTLE_LAYOUT, (10, 10), 20, 20, 1)
        right_panel.attach_element(test)

        cls.BATTLE_LAYOUT.add_panels((top_frame, left_frame, bot_frame, right_frame, right_panel))
        cls.BATTLE_LAYOUT.add_button(test)
