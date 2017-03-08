

class BattlePhase(object):

    def __init__(self, owner, name):
        self.owner = owner  # battle scheduler ref
        self.name = name

    def init(self):  # run any commands that should happen when phase starts
        pass

    def run(self):
        pass

    def end_phase(self):
        self.end_phase_effects()
        next = self.get_next_phase()
        self.owner.next_phase(next)

    def end_phase_effects(self):
        pass

    def get_next_phase(self):
        raise NotImplementedError
