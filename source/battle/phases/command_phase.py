from battle_phase import BattlePhase


class CommandPhase(BattlePhase):

    def __init__(self, owner):
        BattlePhase.__init__(self, owner, 'command')

    def get_next_phase(self):
        return 'action'

    def init(self):
        pass
        # set battle layout to command mode and activate elements

    def run(self):
        pass

