from battle_phase import BattlePhase


class CommandPhase(BattlePhase):

    @classmethod
    def left_army(cls, owner):
        phase = cls(owner, 'left_command')
        return phase

    @classmethod
    def right_army(cls, owner):
        phase = cls(owner, 'right_command')
        return phase

    def set_player(self, player):
        self.player = player

    def __init__(self, owner, name):
        BattlePhase.__init__(self, owner, name)
        self.player = None
        self.next_phase_id = self.set_next_phase_id()

    def set_next_phase_id(self):
        if self.name == 'left_command':
            return 'right_command'
        elif self.name == 'right_command':
            return 'action'

    def get_next_phase(self):
        return self.next_phase_id

    def init(self):  # when command phase begins, open command menus
        if self.player.type == 'human':
            screen = self.owner.battle.screen_layout
            screen.open_panel('commands')

    def run(self):
        pass

    def end_phase_effects(self):  # close command menus
        if self.player.type == 'human':
            screen = self.owner.battle.screen_layout
            screen.close_tagged_panels('command')
