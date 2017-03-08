from ..constants import *
from ..entities.unit_state_archive import UnitStateArchive
from engagement_manager import EngagementManager
from phases.action_phase import ActionPhase
from phases.engagement_phase import EngagementPhase
from phases.aftermath_phase import AftermathPhase
from phases.command_phase import CommandPhase


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
        self.phases = {'command': CommandPhase(self),
                       'action': ActionPhase(self),
                       'engagement': EngagementPhase(self),
                       'aftermath': AftermathPhase(self),
                       }

        self.ready_troops = []
        self.action_queue = []

    def init_battle(self, battle):

        self.battle = battle
        UnitStateArchive.init_battle(battle)
        self.engagements = EngagementManager.get_instance()

        self.phase = self.phases['command']

        for troop in self.battle.left_army.troops:
            self.ready_troops.append(troop)
        for troop in self.battle.right_army.troops:
            self.ready_troops.append(troop)

    def run(self):
        self.phase.run()

    def next_phase(self, phase):
        self.phase = self.phases[phase]
        self.phase.init()

    def complete_action(self, action, ready=True):

        troop = action.actor
        self.action_queue.remove(action)
        if ready:
            if troop in self.battle.left_army.troops:
                self.ready_troops.insert(0, troop)  # left army (attacker) gets initiative priority
            else:
                self.ready_troops.append(troop)
