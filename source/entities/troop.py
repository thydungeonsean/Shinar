from ..constants import *
from ..images.image import TroopImage
from random import shuffle


class Troop(object):
    
    def __init__(self, location, team, color, type, cohesion, morale, speed, strength, weakness):
        
        self.location = location
        self.coord = (0, 0)

        self.direction = 1
        self.side = None

        self.team = team
        self.color = color
        
        self.type = type
        
        self.cohesion = cohesion
        self.morale = morale
        self.speed = speed
        self.strength = strength
        self.weakness = weakness

        self.state = 'advance'
        
        self.x_offset, self.y_offset = self.set_image_offsets()
        self.image = self.set_image()

    @property
    def pixel_coord(self):
        return self.get_pixel_coord(self.coord)

    def set_image(self):
        return TroopImage(self.type, self.color, self.x_offset, self.y_offset)
        
    def set_image_offsets(self):
        return 0, 0

    def set_side(self, side):
        self.side = side

    def draw(self, surface):
        self.image.draw(surface)

    def position_image(self, (x, y)):
        self.image.position((x, y))

    def update_pos(self):
        self.image.position(self.coord)

    def change_facing(self):
        self.image.change_facing()

    def get_pixel_coord(self, (x, y)):
        return x * BATTLEGRID_SQUARE_W + BATTLEFIELD_X_MARGIN, y * BATTLEGRID_SQUARE_H

    def move(self, coord):
        self.coord = coord


class Infantry(Troop):

    coh = 10
    mor = 10
    speed = 2
    str = 'chariot'
    weak = 'archer'

    def __init__(self, location, team, color):
        
        type = 'infantry'
        
        cohesion = Infantry.coh
        morale = Infantry.mor
        speed = Infantry.speed
        strength = Infantry.str
        weakness = Infantry.weak
        
        Troop.__init__(self, location, team, color, type, cohesion, morale, speed, strength, weakness)

    def set_image_offsets(self):
        return scale_tuple((-1, 0))
        
        
class Archer(Troop):

    coh = 5
    mor = 7
    speed = 3
    str = 'infantry'
    weak = 'archer'

    def __init__(self, location, team, color):
        
        type = 'archer'
        
        cohesion = Archer.coh
        morale = Archer.mor
        speed = Archer.speed
        strength = Archer.str
        weakness = Archer.weak

        self.max_fire_range = 3

        Troop.__init__(self, location, team, color, type, cohesion, morale, speed, strength, weakness)

    def get_fire_range(self):

        base_y = self.coord[1]
        fire_range = []
        fire_range.extend(self.get_fire_row(base_y, self.max_fire_range))
        for i in range(2):
            adj = [base_y-i, base_y+i]
            shuffle(adj)
            for y in adj:
                fire_range.extend(self.get_fire_row(y, self.max_fire_range - i))

        return fire_range

    def get_fire_row(self, y, f_range):
        row = []
        x = self.coord[0]
        s = self.direction
        e = f_range * s + s
        for x_mod in range(s, e, s):
            row.append((x+x_mod, y))
        return row

        
class Chariot(Troop):

    coh = 7
    mor = 4
    speed = 5
    str = 'archer'
    weak = 'infantry'

    def __init__(self, location, team, color):
        
        type = 'chariot'
        
        cohesion = Chariot.coh
        morale = Chariot.mor
        speed = Chariot.speed
        strength = Chariot.str
        weakness = Chariot.weak
        
        Troop.__init__(self, location, team, color, type, cohesion, morale, speed, strength, weakness)

    def set_image_offsets(self):
        return scale_tuple((-2, 0))
