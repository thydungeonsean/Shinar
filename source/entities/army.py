from grouping import Grouping
from troop import *


class Army(Grouping):

    """ Army keeps the roster of contained troops in self.troops like a normal Grouping
    It has the stacks dict of groupings sorting troops by type for selection purposes"""

    troop_types = ('infantry', 'archer', 'chariot')

    def __init__(self, player, inf=0, arch=0, char=0):

        self.player = player
        self.color = self.player.color
        self.side = None

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
            new = Infantry(self, self.player, self.color)
            self.add_troop(new)
        for i in range(arch):
            new = Archer(self, self.player, self.color)
            self.add_troop(new)
        for i in range(char):
            new = Chariot(self, self.player, self.color)
            self.add_troop(new)

    def add_troop(self, troop):
        self.add(troop)
        self.add_to_stack(troop)

    def add_to_stack(self, troop):
        stack = troop.type
        troop.init_location(self.stacks[stack])

    def get_troop(self, type):
        stack = self.stacks[type]
        next = stack.get_next()
        return next

    def set_side(self, side):
        self.side = side
        for troop in self.troops:
            troop.set_side(self.side)

    def contains(self, troop):
        if troop in self.troops:
            return True
        return False
