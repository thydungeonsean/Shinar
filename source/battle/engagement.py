

class EngagementManager(object):

    instance = None

    @classmethod
    def get_instance(cls):
        if EngagementManager.instance is None:
            EngagementManager.instance = cls()
        return EngagementManager.instance

    def __init__(self):

        self.battle = None

        self.engagements = []

    def init_battle(self, battle):

        self.battle = battle
        del self.engagements[:]

    def deinit_battle(self):

        self.battle = None
        del self.engagements[:]

    def initiate_engagement(self, attacker, defender):

        new_engagement = Engagement(attacker, defender)
        self.engagements.append(new_engagement)


class Engagement(object):

    def __init__(self, attacker, defender):

        self.manager = EngagementManager.get_instance()  # might not be necessary

        self.attacker = attacker
        self.defender = defender

        self.attack_supporters = []
        self.defence_supporters = []

        self.teams = self.set_teams()

    def set_teams(self):

        attacker_team = self.attacker.team
        defender_team = self.defender.team

        teams = {attacker_team: self.attack_supporters,
                 defender_team: self.defence_supporters}

        return teams

    def add_supporter(self, troop):
        support_team = troop.team
        self.teams[support_team].append(troop)

    def remove_supporter(self, troop):
        support_team = troop.team
        self.teams[support_team].remove(troop)
