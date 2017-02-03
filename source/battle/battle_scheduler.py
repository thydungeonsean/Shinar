from ..constants import *
from action_assigner import ActionAssigner
from engagement import EngagementManager


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

        self.phase = 'action'

        self.ready_troops = []
        self.action_queue = []

        self.phase_count = 0

    def init_battle(self, battle):

        self.battle = battle
        self.action_assigner = ActionAssigner.get_instance()
        self.action_assigner.init_battle(self.battle, self)
        self.engagements = EngagementManager.get_instance()

        for troop in self.battle.left_army.troops:
            self.ready_troops.append(troop)
        for troop in self.battle.right_army.troops:
            self.ready_troops.append(troop)

    def run(self):
        if self.phase == 'action':
            self.run_action_phase()
        elif self.phase == 'engagement':
            self.run_engage_phase()
        elif self.phase == 'aftermath':
            self.run_aftermath_phase()

    def run_action_phase(self):
        self.set_troop_actions()
        self.run_troop_actions()
        self.increment_tick()
        if self.tick >= self.end_tick:
            self.end_action_phase()

    def increment_tick(self):

        self.tick += 1

    def end_action_phase(self):
        print 'end of actions - bat sched'
        self.tick = 0
        self.determine_next_phase()

    def determine_next_phase(self):
        if not self.engagements.engagements:
            self.engage_all()

        if self.engagements.engagements:
            self.phase = 'engagement'
            self.assign_engagement_actions()
        else:
            self.end_turn()

    def set_troop_actions(self):

        for troop in self.ready_troops:
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

    def run_engage_phase(self):

        # if self.action_queue:
        #     for action in self.action_queue[:]:
        #         action.run()
        # else:
        #     self.resolve_engagements()
        self.resolve_engagements()

    def resolve_engagements(self):

        self.engagements.resolve_engagements()

        self.end_engage_phase()

    def end_engage_phase(self):
        self.phase = 'aftermath'
        self.assign_aftermath_actions()

    def engage_all(self):
        for troop in self.battle.left_army.troops:
            if troop.state not in ('flee', 'rout'):
                target = self.action_assigner.check_melee_target(troop)
                if target is not None:
                    # TODO need to find way to get supports to work here
                    self.engagements.initiate_engagement(troop, target)

    def assign_engagement_actions(self):

        for engagement in self.engagements.engagements:
            actions = self.action_assigner.get_engagement_melees(engagement)
            self.action_queue.extend(actions)

    def assign_aftermath_actions(self):

        actions = self.action_assigner.get_aftermath_actions()
        self.action_queue.extend(actions)

    def run_aftermath_phase(self):

        if self.action_queue:
            for action in self.action_queue[:]:
                action.run()
        else:
            self.end_turn()

    def end_turn(self):
        self.phase = 'action'
