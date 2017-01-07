from ..constants import *
from ..entities.actions import *
from random import *


class BattleScheduler(object):

    def __init__(self, battle):

        self.battle = battle

        self.tick = 0
        self.end_tick = FRAMES_PER_TURN

        self.ready_troops = []
        self.busy_troops = []
        self.action_queue = []

        self.init_battle()

    def init_battle(self):

        for troop in self.battle.left_army.troops:
            self.ready_troops.append(troop)
        for troop in self.battle.right_army.troops:
            self.ready_troops.append(troop)

    def run(self):

        self.set_troop_actions()
        self.run_troop_actions()
        self.increment_tick()

    def increment_tick(self):
        self.tick += 1

    def set_troop_actions(self):

        for troop in self.ready_troops:
            self.activate_troop(troop)
            new = Advance(self, troop)
            self.action_queue.append(new)
        del self.ready_troops[:]

    def activate_troop(self, troop):
        self.busy_troops.append(troop)

    def run_troop_actions(self):

        for action in self.action_queue[:]:
            action.run()

    def complete_action(self, action):
        troop = action.actor
        self.action_queue.remove(action)
        self.busy_troops.remove(troop)
        self.ready_troops.append(troop)

