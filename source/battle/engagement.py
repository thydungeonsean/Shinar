

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

        self.engagement_dict = {}

    def init_battle(self, battle):

        self.battle = battle
        del self.engagements[:]

    def deinit_battle(self):

        self.battle = None
        del self.engagements[:]

    def initiate_engagement(self, attacker, defender):

        new_engagement = Engagement(attacker, defender)
        attacker.change_state('engage')
        defender.change_state('engage')
        self.engagements.append(new_engagement)
        self.engagement_dict[attacker] = new_engagement
        self.engagement_dict[defender] = new_engagement

    def deinitiate_engagement(self, engagement):
        self.engagements.remove(engagement)
        for t in engagement.involved_troops:
            if t.state not in ('flee', 'rout'):
                t.state = 'advance'
            del self.engagement_dict[t]

    def support_engagement(self, supporter, target):
        engagement = self.get_engagement(target)
        engagement.add_supporter(supporter)

    def break_support(self, troop):  # when a troop supporting an engagement is engaged or forced to retreat
        engagement = self.get_engagement(troop)
        engagement.remove_supporter(troop)
        del self.engagement_dict[troop]

    def get_engagement(self, troop):
        return self.engagement_dict[troop]

    def get_opposing(self, troop):
        engagement = self.get_engagement(troop)
        return engagement.get_opposing(troop)

    # resolution
    def resolve_engagements(self):
        print 'resolving'

        ended = []

        for engagement in self.engagements:
            print 'rolling'
            if engagement.resolve():  # one side has broken
                print 'someone ran'
                ended.append(engagement)

        for engagement in ended:
            self.deinitiate_engagement(engagement)


class Engagement(object):

    def __init__(self, attacker, defender):

        self.manager = EngagementManager.get_instance()

        self.attacker = attacker
        self.defender = defender

        self.attack_supporters = []
        self.defence_supporters = []

        self.involved_troops = [attacker, defender]

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
        self.involved_troops.append(troop)

    def remove_supporter(self, troop):
        support_team = troop.team
        self.teams[support_team].remove(troop)
        self.involved_troops.remove(troop)

    def get_opposing(self, troop):
        if troop == self.attacker:
            return self.defender
        else:
            return self.attacker

    def resolve(self):

        attack_value = self.get_battle_value(self.attacker)
        defence_value = self.get_battle_value(self.defender)

        attacker_hits = self.attacker.roll_engagement_dice(self.defender, attack_value)
        defender_hits = self.defender.roll_engagement_dice(self.attacker, defence_value)

        self.attacker.apply_hits(self.defender, attacker_hits)
        self.defender.apply_hits(self.attacker, defender_hits)

        if defender_hits > attacker_hits:
            breaks = self.attacker.morale_check()
        else:
            breaks = self.defender.morale_check()

        return breaks

    def get_battle_value(self, troop):

        team = troop.team
        supporters = self.teams[team]

        return troop.cohesion + (len(supporters) * 2)
