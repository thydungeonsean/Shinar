from ..constants import *
from ..entities.action_assigner import ActionAssigner
from ..entities.actions import *
from random import *


class BattleScheduler(object):

    instance = None

    @classmethod
    def get_instance(cls):
        if BattleScheduler.instance is None:
            BattleScheduler.instance = cls()
            return BattleScheduler.instance
        else:
            return BattleScheduler.instance

    def __init__(self):

        self.battle = None

        self.action_assigner = None

        self.tick = 0
        self.end_tick = FRAMES_PER_TURN

        self.ready_troops = []
        self.action_queue = []

    def init_battle(self, battle):

        self.battle = battle
        self.action_assigner = ActionAssigner.get_instance()
        self.action_assigner.init_battle(self.battle, self)

        for troop in self.battle.left_army.troops:
            self.ready_troops.append(troop)
        for troop in self.battle.right_army.troops:
            self.ready_troops.append(troop)

    def run(self):

        self.set_troop_actions()
        self.run_troop_actions()
        self.increment_tick()
        if self.tick >= self.end_tick:
            pass
            # print 'end of turn'

    def increment_tick(self):
        self.tick += 1

    def set_troop_actions(self):

        for troop in self.ready_troops:
            # new = Advance(self, troop)
            new = self.action_assigner.get_next_action(troop)
            self.action_queue.append(new)
        del self.ready_troops[:]

    def run_troop_actions(self):

        for action in self.action_queue[:]:
            action.run()

    def complete_action(self, action):
        troop = action.actor
        self.action_queue.remove(action)
        if troop in self.battle.left_army.troops:
            self.ready_troops.insert(0, troop)  # left army (attacker) gets initiative priority
        else:
            self.ready_troops.append(troop)

