from unit_state import *


class UnitStateArchive(object):

    states = {
              'advance': Advancing(),
              'harry': Harrying(),
              'support': Supporting(),
              'engage': Engaging(),
              'fire': Firing(),
              'flee': Fleeing(),
              'rout': Routing(),
              'hold': Holding()
             }

    @classmethod
    def init_battle(cls, battle):
        for unit_state in cls.states.values():
            unit_state.init_battle(battle)

    @classmethod
    def deinit_battle(cls):
        for unit_state in cls.states.values():
            unit_state.deinit_battle()
