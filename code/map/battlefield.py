from map import Map
from map_image import MapImageGenerator
from ..entities.locations import Location
from random import randint
from ..entities.troop import *


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

    width = 9
    height = left_w + center_w + right_w
    
    @staticmethod
    def get_field_y(lane_key, lane_y):
        bf = BattleField
        return lane_y + bf.lane_offset[lane_key]

    def __init__(self):
        
        # self.map = Map(BattleField.width, BattleField.height)
        self.map = Map.load_map_file('battlemap.txt')
        self.map_image = self.set_map_image()
        self.map_image_rect = self.map_image.get_rect()

        self.lanes, self.rows = self.set_lanes_and_rows()

        # tacked on for testing
        self.random_troops()

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
            x, y = 10, row.y
            # todo built in position algo
            troop.position((x, y))

    def draw(self, surface):
        surface.blit(self.map_image, self.map_image_rect)
        for i in range(10):
            self.rows[i].draw(surface)


class Row(Location):
    
    width = 9
    
    def __init__(self, lane_id, lane_y, field_y):
        
        self.lane_id = lane_id
        
        self.lane_y = lane_y
        self.field_y = field_y
        
        self.y = self.set_y()
        
        Location.__init__(self)
        
    def get_position(self, troop):
        return 1
        
    def set_y(self):
        return scale(24)*self.field_y + BATTLEFIELD_MARGIN

    def draw(self, surface):

        for item in self.items:
            item.draw(surface)
