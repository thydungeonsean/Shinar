from ..constants import scale


class PositionGrid(object):

    def __init__(self, col_w, row_h, rows=1, columns=1, gap=scale(5), x=scale(5), y=scale(5)):

        self.x = x
        self.y = y
        self.columns = columns
        self.rows = rows

        self.col_w = col_w
        self.row_h = row_h
        self.gap = gap

        self.grid_keys = self.set_grid_keys()
        self.grid_pos_dict = self.set_grid_pos_dict()

    def position_button(self, i, button):
        button.move(self.get_grid_pos(i))

    def get_grid_pos(self, i):
        index = self._parse_index(i)
        return self.grid_pos_dict[index]

    # init methods
    def set_grid_keys(self):
        grid_keys = []
        for x in range(self.columns):
            for y in range(self.rows):
                grid_keys.append((x, y))

        return grid_keys

    def set_grid_pos_dict(self):
        grid_pos_dict = {}
        for x, y in self.grid_keys:
            grid_pos_dict[(x, y)] = self.get_pos((x, y))

        return grid_pos_dict

    # internal helper methods
    def get_pos(self, (gx, gy)):
        w_gaps = 0
        h_gaps = 0
        if gx > 0:
            w_gaps = gx * self.gap
        x = gx * self.col_w + w_gaps + self.x
        if gy > 0:
            h_gaps = gy * self.gap
        y = gy * self.row_h + h_gaps + self.y

        return x, y

    @staticmethod
    def _parse_index(i):
        if isinstance(i, tuple):
            return i
        elif isinstance(i, int):
            return 0, i
        else:
            raise Exception('Invalid index passed to menu grid')

