from ..constants import *
from ..images.troop_image import TroopImage
from coord import Coord
from unit_state_archive import UnitStateArchive
from random import shuffle, randint


class Troop(object):

    count = 0

    def __init__(self, location, team, color, type, cohesion, morale, speed, strength, weakness):
        
        self.location = location
        self.coord = Coord()

        self.side = None
        self.dir_mod = 1

        self.team = team
        self.color = color
        
        self.type = type
        self.cohesion = cohesion
        self.max_cohesion = cohesion
        self.morale = morale
        self.max_morale = morale
        self.speed = speed
        self.strength = strength
        self.weakness = weakness
        self.break_points = 0
        self.retreat_count = 0

        self.needs_check = False

        self.state = UnitStateArchive.get_state('advance')
        
        self.x_offset, self.y_offset = self.set_image_offsets()
        self.image = self.set_image()
        self.coord.bind(self.image.coord)

    @property
    def pixel_coord(self):
        return self.get_pixel_coord(self.coord.get)

    def set_image(self):
        return TroopImage(self.type, self.color, self.x_offset, self.y_offset)
        
    def set_image_offsets(self):
        return 0, 0

    @property
    def advance_dir_mod(self):
        if self.side == 'left':
            return 1
        else:
            return -1

    @property
    def retreat_dir_mod(self):
        if self.side == 'left':
            return -1
        else:
            return 1

    @property
    def image_facing(self):
        if self.dir_mod == 1:
            return 'left'
        else:
            return 'right'

    @classmethod
    def set_tag(cls, self):
        tag = self.type + str(cls.count)
        cls.count += 1
        return tag

    def set_side(self, side):
        self.side = side
        self.init_dir_mod()
        self.change_facing(self.image_facing)

    def init_dir_mod(self):
        if self.side == 'left':
            self.set_dir_mod(1)
        else:
            self.set_dir_mod(-1)

    def set_dir_mod(self, dir_mod):
        self.dir_mod = dir_mod

    def draw(self, surface):
        self.image.draw(surface)

    def update_pos(self):  # TODO here is where coords interact with troop image
        self.image.position()

    def change_facing(self, facing):
        self.image.change_facing(facing)

    def retreat(self):
        self.set_dir_mod(self.retreat_dir_mod)
        self.change_facing(self.image_facing)

    def advance(self):
        self.set_dir_mod(self.advance_dir_mod)
        self.change_facing(self.image_facing)

    def get_pixel_coord(self, (x, y)):
        return x * BATTLEGRID_SQUARE_W + BATTLEFIELD_X_MARGIN, y * BATTLEGRID_SQUARE_H

    def move(self, (x, y)):
        self.coord.set((x, y))

    def change_state(self, state):
        self.state = UnitStateArchive.get_state(state)

    # combat algorithm methods
    def damage_cohesion(self):
        self.cohesion -= 1
        if self.cohesion <= 1:
            self.cohesion = 1

    def damage_morale(self):
        self.morale -= 1
        if self.morale < 1:
            self.morale = 0

    def add_break_point(self):
        self.break_points += 1

    def reset_break_points(self):
        self.break_points = 0

    def set_retreat_count(self, margin):
        self.retreat_count = margin

    def decrement_retreat(self):
        self.retreat_count -= 1
        if self.retreat_count <= 0:
            self.change_state('advance')
            self.advance()

    def hit(self, target):

        effect = randint(0, 2)
        if effect == 0:
            target.damage_cohesion()
        elif effect == 1:
            target.damage_morale()
        elif effect == 2:
            target.add_break_point()

    def fire(self, target):
        pass

    def harry(self, target):
        self.hit(target)
        target.check()

    def roll_engagement_dice(self, target, num):

        hits = 0

        str = self.set_die_str(target)
        for i in range(num):
            roll = randint(1, str)
            if roll >= 4:
                hits += 1

        return hits

    def apply_hits(self, target, hits):
        for hit in range(hits):
            self.hit(target)

    def set_die_str(self, target):
        if target.type == self.strength:
            return 8
        elif target.type == self.weakness:
            return 4
        return 6

    def morale_check(self):
        self.needs_check = False
        check = randint(1, 10)
        if check > (self.morale - self.break_points):
            # morale failure
            margin = check - (self.morale - self.break_points)
            self.set_retreat_count(margin)
            self.breaks()
            return True
        return False

    def check(self):
        self.needs_check = True

    def breaks(self):
        self.change_state('flee')
        self.reset_break_points()

    def get_next_action(self):
        if self.needs_check:
            self.morale_check()
        return self.state.get_next_action(self)


class Infantry(Troop):

    coh = 10
    mor = 10
    speed = 2
    str = 'chariot'
    weak = 'archer'

    count = 0

    def __init__(self, location, team, color):
        
        type = 'infantry'
        
        cohesion = Infantry.coh
        morale = Infantry.mor
        speed = Infantry.speed
        strength = Infantry.str
        weakness = Infantry.weak
        
        Troop.__init__(self, location, team, color, type, cohesion, morale, speed, strength, weakness)

        self.tag = Infantry.set_tag(self)

    def set_image_offsets(self):
        return scale_tuple((-1, 0))
        
        
class Archer(Troop):

    coh = 5
    mor = 10
    speed = 3
    str = 'infantry'
    weak = 'archer'

    count = 0

    def __init__(self, location, team, color):
        
        type = 'archer'
        
        cohesion = Archer.coh
        morale = Archer.mor
        speed = Archer.speed
        strength = Archer.str
        weakness = Archer.weak

        self.max_fire_range = 3

        Troop.__init__(self, location, team, color, type, cohesion, morale, speed, strength, weakness)

        self.tag = Archer.set_tag(self)

    def get_fire_range(self):

        base_y = self.coord.y
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
        x = self.coord.x
        s = self.dir_mod
        e = f_range * s + s
        for x_mod in range(s, e, s):
            row.append((x+x_mod, y))
        return row

    @property
    def fire_strength(self):
        str = self.cohesion/2
        if str < 1:
            str = 1
        return str

    def fire(self, target):
        hits = self.roll_engagement_dice(target, self.fire_strength)
        self.apply_hits(target, hits)
        if target.state.name != 'engage':
            target.check()


class Chariot(Troop):

    coh = 7
    mor = 10
    speed = 5
    str = 'archer'
    weak = 'infantry'

    count = 0

    def __init__(self, location, team, color):
        
        type = 'chariot'
        
        cohesion = Chariot.coh
        morale = Chariot.mor
        speed = Chariot.speed
        strength = Chariot.str
        weakness = Chariot.weak
        
        Troop.__init__(self, location, team, color, type, cohesion, morale, speed, strength, weakness)

        self.tag = Chariot.set_tag(self)

    def set_image_offsets(self):
        return scale_tuple((-2, 0))

    def set_retreat_count(self, margin):
        self.retreat_count = margin + 1  # TODO maybe make this more explicit
