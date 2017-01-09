from ..entities.grouping import Grouping
from ..constants import *


class Row(Grouping):

    width = BATTLEGRID_W

    def __init__(self, lane_id, lane_y, field_y):

        self.lane_id = lane_id

        self.lane_y = lane_y
        self.field_y = field_y

        self.y = self.set_y()

        self.sides = {'left': False, 'right': False}

        Grouping.__init__(self)

    def get_position(self, troop):
        pass

    def set_y(self):
        return BATTLEGRID_SQUARE_H * self.field_y + BATTLEFIELD_Y_MARGIN

    def draw(self, surface):

        for item in self.troops:
            item.draw(surface)

    def get_start_coord(self, side):

        if side == 'left':
            x = BATTLEFIELD_X_MARGIN
        elif side == 'right':
            x = BATTLEFIELD_W - BATTLEFIELD_X_MARGIN - BATTLEGRID_SQUARE_W
        return x, self.y

    def assign_to_row(self, troop, side):
        self.add(troop)
        troop.location = self
        if side == 'left':
            x = 0
        else:
            x = BATTLEGRID_W - 1
        y = self.field_y
        troop.coord = (x, y)
        image_pos = self.get_start_coord(side)
        #troop.position_image(image_pos)
        self.sides[side] = True
