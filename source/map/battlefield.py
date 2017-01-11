from ..constants import *
from map import Map
from map_image import MapImageGenerator
from battle_grid import BattleGrid
from row import Row
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
        # self.random_troops()

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
        
    def random_troops(self):  #TODO prob don't need this period
        troop_sel = {
                    0: Infantry,
                    1: Archer,
                    2: Chariot
                    }
        for i in range(BattleField.height):
            row = self.rows[i]
            troop = troop_sel[randint(0, 2)](row, 'Red')
            row.add(troop)
            x, y = 0, row.field_y
            # todo built in position algo
            troop.position_image((x, y))

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

    def get_adj_rows(self, i):

        adj = []
        adj_i = (i-1, i+1)
        for row_id in adj_i:
            if row_id in range(BATTLEGRID_H):
                adj.append(self.rows[row_id])
        return adj
