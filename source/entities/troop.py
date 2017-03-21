from ..constants import *
from ..images.troop_image import TroopImage
from coord import Coord
from battle_stats import BattleStats
from unit_state_archive import UnitStateArchive
from ..gui.troop_handle import TroopHandle
from random import shuffle


class Troop(object):

    count = 0

    def __init__(self, army, team, color, type):

        self.army = army
        self.location = None
        self.coord = Coord()
        self.team = team
        self.color = color

        # these will be set according to battle_init
        self.side = None
        self.dir_mod = 1
        self.reporter_component = None

        self.active = False

        # stats
        self.type = type

        self.stats = BattleStats(self, self.type)

        self.state = UnitStateArchive.get_state('advance')
        
        self.x_offset, self.y_offset = self.set_image_offsets()
        self.image = self.set_image()
        self.coord.bind(self.image.coord)

        self.ui_handle = TroopHandle(self)

    def init_location(self, location):
        self.set_location(location)

    def remove_from_location(self):
        self.location.remove(self)
        self.location = None

    def remove_from_army(self):
        self.army.remove(self)

    def change_location(self, new):
        self.remove_from_location()
        self.set_location(new)

    def set_location(self, location):
        self.location = location
        location.add(self)

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

    def set_reporter_component(self, reporter):
        self.reporter_component = reporter

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def draw(self, surface):
        self.image.draw(surface)

    def update_pos(self):  # TODO here is where coords interact with troop image
        self.image.position()

    def change_facing(self, facing):
        self.image.change_facing(facing)

    def set_image_to_retreat(self):
        self.set_dir_mod(self.retreat_dir_mod)
        self.change_facing(self.image_facing)

    def set_image_to_advance(self):
        self.set_dir_mod(self.advance_dir_mod)
        self.change_facing(self.image_facing)

    def get_pixel_coord(self, (x, y)):
        return x * BATTLEGRID_SQUARE_W + BATTLEFIELD_X_MARGIN, y * BATTLEGRID_SQUARE_H

    def move(self, (x, y)):
        self.coord.set((x, y))

    def change_state(self, state):
        self.state = UnitStateArchive.get_state(state)
        if self.state.name == 'flee':
            self.reporter_component.send_report('unit', self.side, 'flee')

    # combat api methods
    @property
    def needs_check(self):
        return self.stats.needs_morale_check

    def rout(self):  # remove from battle
        self.remove_from_location()
        self.remove_from_army()
        self.deactivate()
        self.reporter_component.send_report('unit', self.side, 'rout')

    def pursue(self):
        self.remove_from_location()
        self.remove_from_army()
        self.deactivate()
        self.reporter_component.send_report('unit', self.side, 'pursue')

    def harry(self, target):
        self.stats.harry(target)

    def check(self):
        self.stats.check()

    def get_next_action(self):
        if self.needs_check:
            self.stats.morale_check()
        return self.state.get_next_action(self)

    @property
    def speed(self):
        return self.stats.speed


class Infantry(Troop):

    count = 0

    def __init__(self, location, team, color):
        
        type = 'infantry'
        
        Troop.__init__(self, location, team, color, type)

        self.tag = Infantry.set_tag(self)

    def set_image_offsets(self):
        return scale_tuple((-1, 0))
        
        
class Archer(Troop):

    count = 0

    def __init__(self, location, team, color):
        
        type = 'archer'

        self.max_fire_range = 3

        Troop.__init__(self, location, team, color, type)

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

    def fire(self, target):
        self.stats.fire(target)


class Chariot(Troop):

    count = 0

    def __init__(self, location, team, color):
        
        type = 'chariot'
        
        Troop.__init__(self, location, team, color, type)

        self.tag = Chariot.set_tag(self)

    def set_image_offsets(self):
        return scale_tuple((-2, 0))
