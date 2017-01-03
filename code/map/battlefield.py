from ..constants import *
from map import Map
from map_image import MapImageGenerator
from battle_grid import BattleGrid
from ..entities.grouping import Grouping
from random import randint
from ..entities.troop import *
from random import shuffle


class BattleField(object):
    
    left_w = 3
    center_w = 4
    right_w = 3

    lane_keys = ['left', 'center', 'right']

    lanes = {
        'left': range(left_w),
        'center': range(center_w),
        'right': range(right_w)
    }
    
    lane_offset = {'left': 0, 'center': left_w, 'right': left_w + center_w}

    height = BATTLEGRID_H

    @staticmethod
    def get_field_y(lane_key, lane_y):
        bf = BattleField
        return lane_y + bf.lane_offset[lane_key]

    def __init__(self):

        self.map = Map.load_map_file('battlemap.txt')
        self.map_image = self.set_map_image()
        self.map_image_rect = self.map_image.get_rect()

        self.lanes, self.rows = self.set_lanes_and_rows()

        self.grid = BattleGrid()

        # tacked on for testing
        #self.random_troops()

    # init methods
    def set_lanes_and_rows(self):

        bf = BattleField

        lanes = {
                'left': [],
                'center': [],
                'right': [],
                }
        
        rows = []

        for k in bf.lane_keys:
            for i in bf.lanes[k]:
                row = Row(k, i, self.get_field_y(k, i))
                lanes[k].append(row)
                rows.append(row)
        return lanes, rows
            
    def set_map_image(self):
        m_gen = MapImageGenerator.get_instance()
        return m_gen.generate_image(self.map)
        
    def random_troops(self):
        troop_sel = {
                    0: Infantry,
                    1: Archer,
                    2: Chariot
                    }
        for i in range(BattleField.height):
            row = self.rows[i]
            troop = troop_sel[randint(0, 2)](row, 'Red')
            row.add(troop)
            x, y = BATTLEFIELD_X_MARGIN, row.y
            # todo built in position algo
            troop.position((x, y))

    def draw(self, surface):
        surface.blit(self.map_image, self.map_image_rect)
        for i in range(10):
            self.rows[i].draw(surface)

    def assign_to_row(self, troop, row_id, side):
        row = self.rows[row_id]
        row.assign_to_row(troop, side)

    def get_empty_row(self, side):
        index = range(BATTLEGRID_H)
        shuffle(index)
        for i in index:
            row = self.rows[i]
            if not row.sides[side]:
                return row
        print 'uh oh!!! no empty rows!'


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
        return 1
        
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
        pos = self.get_start_coord(side)
        troop.position(pos)
        self.sides[side] = True

