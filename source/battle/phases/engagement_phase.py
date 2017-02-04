import battle_phase


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
        self.resolve_engagements()
        self.assign_aftermath_actions()

    def resolve_engagements(self):
        self.owner.engagements.resolve_engagements()

    def get_next_phase(self):
        return 'aftermath'

    def assign_aftermath_actions(self):

        actions = self.owner.action_assigner.get_aftermath_actions()
        self.owner.action_queue.extend(actions)
