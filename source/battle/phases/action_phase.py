from ...constants import FRAMES_PER_TURN
import battle_phase
from ..actions import EngagementMelee


class ActionPhase(battle_phase.BattlePhase):

    def __init__(self, owner):
        battle_phase.BattlePhase.__init__(self, owner, 'action')
        self.tick = 0
        self.end_of_phase = FRAMES_PER_TURN

    def increment_tick(self):
        self.tick += 1

    def run(self):
        self.set_troop_actions()
        self.run_troop_actions()
        self.increment_tick()
        if self.tick >= self.end_of_phase:
            self.end_phase()

    def set_troop_actions(self):
        for troop in self.owner.ready_troops:
            new_action = troop.get_next_action()
            self.owner.action_queue.append(new_action)
        del self.owner.ready_troops[:]

    def run_troop_actions(self):

        for action in self.owner.action_queue[:]:
            action.run()

    def end_phase_effects(self):
        print 'end of action phase'
        self.tick = 0
        if not self.owner.engagements.engagements:
            self.engage_all()

    def get_next_phase(self):
        if self.owner.engagements.engagements:
            next_phase = 'engagement'
            self.assign_engagement_actions()
        else:
            next_phase = 'end'
        return next_phase

    def engage_all(self):
        for troop in self.owner.battle.left_army.troops:
            if troop.state.name not in ('flee', 'rout'):
                target = troop.state.check_melee_target(troop)
                if target is not None:
                    # TODO need to find way to get supports to work here
                    self.owner.engagements.initiate_engagement(troop, target)

    def assign_engagement_actions(self):
        for engagement in self.owner.engagements.engagements:
            actions = self.get_engagement_melees(engagement)
            self.owner.action_queue.extend(actions)

    def get_engagement_melees(self, e):

        actions = [EngagementMelee(self.owner, e.attacker, e.defender),
                   EngagementMelee(self.owner, e.defender, e.attacker)]

        return actions
