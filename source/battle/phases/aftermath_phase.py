import battle_phase


class AftermathPhase(battle_phase.BattlePhase):

    def __init__(self, owner):
        battle_phase.BattlePhase.__init__(self, owner, 'aftermath')

    def run(self):
        if self.owner.action_queue:
            for action in self.owner.action_queue[:]:
                action.run()
        else:
            self.end_phase()

    def get_next_phase(self):
        return 'left_command'
