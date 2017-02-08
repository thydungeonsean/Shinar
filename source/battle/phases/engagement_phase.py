import battle_phase
from ..actions import AftermathRetreat


class EngagementPhase(battle_phase.BattlePhase):

    def __init__(self, owner):
        battle_phase.BattlePhase.__init__(self, owner, 'engagement')

    def run(self):

        if self.owner.action_queue:
            for action in self.owner.action_queue[:]:
                action.run()
        else:
            self.end_phase()

    def end_phase_effects(self):
        retreats = self.resolve_engagements()
        self.assign_aftermath_actions(retreats)

    def resolve_engagements(self):
        return self.owner.engagements.resolve_engagements()

    def get_next_phase(self):
        return 'aftermath'

    def assign_aftermath_actions(self, retreats):

        actions = self.get_aftermath_actions(retreats)
        self.owner.action_queue.extend(actions)

    def get_aftermath_actions(self, retreats):

        actions = []

        for troop in retreats:
            retreat = AftermathRetreat(self.owner, troop)
            actions.append(retreat)

        return actions
