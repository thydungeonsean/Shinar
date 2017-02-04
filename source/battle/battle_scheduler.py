from ..constants import *
from action_assigner import ActionAssigner
from engagement import EngagementManager
from phases.action_phase import ActionPhase
from phases.engagement_phase import EngagementPhase
from phases.aftermath_phase import AftermathPhase


class BattleScheduler(object):

    instance = None

    @classmethod
    def get_instance(cls):
        if BattleScheduler.instance is None:
            BattleScheduler.instance = cls()

        return BattleScheduler.instance

    def __init__(self):

        self.battle = None

        self.action_assigner = None
        self.engagements = None

        self.tick = 0
        self.end_tick = FRAMES_PER_TURN

        self.phase = None
        self.phases = {'action': ActionPhase(self),
                       'engagement': EngagementPhase(self),
                       'aftermath': AftermathPhase(self)}

        self.ready_troops = []
        self.action_queue = []

        self.phase_count = 0

    def init_battle(self, battle):

        self.battle = battle
        self.action_assigner = ActionAssigner.get_instance()
        self.action_assigner.init_battle(self.battle, self)
        self.engagements = EngagementManager.get_instance()

        self.phase = self.phases['action']

        for troop in self.battle.left_army.troops:
            self.ready_troops.append(troop)
        for troop in self.battle.right_army.troops:
            self.ready_troops.append(troop)

    def run(self):
        self.phase.run()

    def next_phase(self, phase):
        self.phase = self.phases[phase]

    def complete_action(self, action, ready=True):

        troop = action.actor
        self.action_queue.remove(action)
        if ready:
            if troop in self.battle.left_army.troops:
                self.ready_troops.insert(0, troop)  # left army (attacker) gets initiative priority
            else:
                self.ready_troops.append(troop)
