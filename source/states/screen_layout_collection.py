from ..gui.screen_layout import ScreenLayout
from ..gui.panel import Panel
from ..gui.button import Button
from ..gui.drag_box import DragBox
from ..gui.pop_up import PopUp

from ..constants import *


class ScreenLayoutCollection(object):

    BATTLE_LAYOUT = ScreenLayout()

    @classmethod
    def init_battle_layout(cls):

        top_frame = Panel.base(cls.BATTLE_LAYOUT, (0, 0), 2 * BATTLEFIELD_FRAME_W + BATTLEFIELD_W, BATTLEFIELD_FRAME_W)

        left_frame = Panel.base(cls.BATTLE_LAYOUT, (0, BATTLEFIELD_FRAME_W), BATTLEFIELD_FRAME_W, BATTLEFIELD_H)

        bot_frame = Panel.base(cls.BATTLE_LAYOUT, (0, SCREENH - BATTLEFIELD_FRAME_W), 2 * BATTLEFIELD_FRAME_W +
                               BATTLEFIELD_W, BATTLEFIELD_FRAME_W)

        right_frame = Panel.base(cls.BATTLE_LAYOUT, (BATTLEFIELD_FRAME_W + BATTLEFIELD_W, BATTLEFIELD_FRAME_W),
                                 BATTLEFIELD_FRAME_W, BATTLEFIELD_H)

        right_panel = Panel.parent(Panel.base(cls.BATTLE_LAYOUT, (2 * BATTLEFIELD_FRAME_W + BATTLEFIELD_W, 0),
                                   SCREENW - (2 * BATTLEFIELD_FRAME_W + BATTLEFIELD_W),
                                   SCREENH))

        test = Button(cls.BATTLE_LAYOUT, (10, 10), 20, 20, function=make_pop_up)
        right_panel.attach_element(test)

        drag = DragBox(cls.BATTLE_LAYOUT, (650, 20), 50, 50)
        test2 = Button(cls.BATTLE_LAYOUT, (2, 2), 10, 10, function=make_pop_up)
        drag.attach_element(test2)

        cls.BATTLE_LAYOUT.add_elements((top_frame, left_frame, bot_frame, right_frame, right_panel, drag))


def make_pop_up():

    new = PopUp(ScreenLayoutCollection.BATTLE_LAYOUT, (40, 40), 100, 100)
    ScreenLayoutCollection.BATTLE_LAYOUT.add_element(new)
