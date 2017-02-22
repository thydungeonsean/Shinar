from ..gui.screen_layout import ScreenLayout
from ..gui.panel import Panel
from ..gui.button import Button

from ..constants import *


class ScreenLayoutCollection(object):

    BATTLE_LAYOUT = ScreenLayout()

    @classmethod
    def init_battle_layout(cls):

        top_frame = Panel((0, 0), 2 * BATTLEFIELD_FRAME_W + BATTLEFIELD_W, BATTLEFIELD_FRAME_W)

        left_frame = Panel((0, BATTLEFIELD_FRAME_W), BATTLEFIELD_FRAME_W, BATTLEFIELD_H)

        bot_frame = Panel((0, SCREENH - BATTLEFIELD_FRAME_W), 2 * BATTLEFIELD_FRAME_W +
                          BATTLEFIELD_W, BATTLEFIELD_FRAME_W)

        right_frame = Panel((BATTLEFIELD_FRAME_W + BATTLEFIELD_W, BATTLEFIELD_FRAME_W),
                            BATTLEFIELD_FRAME_W, BATTLEFIELD_H)

        right_panel = Panel((2 * BATTLEFIELD_FRAME_W + BATTLEFIELD_W, 0),
                            SCREENW - (2 * BATTLEFIELD_FRAME_W + BATTLEFIELD_W),
                            SCREENH)

        test = Button(right_panel, (10, 10), 20, 20)

        cls.BATTLE_LAYOUT.add_panels((top_frame, left_frame, bot_frame, right_frame, right_panel))
        cls.BATTLE_LAYOUT.add_button(test)
