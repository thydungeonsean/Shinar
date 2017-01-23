from grouping import Grouping
from troop import *


class Army(Grouping):

    """ Army keeps the roster of contained troops in self.troops like a normal Grouping
    It has the stacks dict of groupings sorting troops by type for selection purposes"""

    troop_types = ('infantry', 'archer', 'chariot')

    def __init__(self, team, color, inf=0, arch=0, char=0):

        self.team = team
        self.color = color
        self.side = None
        self.direction = 1

        Grouping.__init__(self)

        self.stacks = self.set_stacks()

        self.init_troops(inf, arch, char)

    # init_methods
    def set_stacks(self):

        stacks = {
            'infantry': Grouping(),
            'archer': Grouping(),
            'chariot': Grouping()
            }

        return stacks

    def init_troops(self, inf, arch, char):

        for i in range(inf):
            new = Infantry(self, self.team, self.color)
            self.add(new)
        for i in range(arch):
            new = Archer(self, self.team, self.color)
            self.add(new)
        for i in range(char):
            new = Chariot(self, self.team, self.color)
            self.add(new)

    def add(self, troop):
        self.troops.append(troop)
        self.add_to_stack(troop)

    def add_to_stack(self, troop):
        stack = troop.type
        self.stacks[stack].add(troop)

    def get_troop(self, type):
        stack = self.stacks[type]
        return stack.get_next()

    def set_side(self, side):
        self.side = side
        self.direction = self.set_direction(side)

    def set_direction(self, side):
        if side == 'left':
            return 1
        else:
            return -1

    def contains(self, troop):
        if troop in self.troops:
            return True
        return False
