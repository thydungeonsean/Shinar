from battle_phase import BattlePhase


class EndPhase(BattlePhase):

    def __init__(self, owner):
        BattlePhase.__init__(self, owner, 'end')

    def get_next_phase(self):
        return 'action'
