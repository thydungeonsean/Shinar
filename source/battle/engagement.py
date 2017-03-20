import engagement_manager as em


# TODO - find fatal error with removing troops from engagements - rare
class Engagement(object):

    def __init__(self, attacker, defender):

        self.manager = em.EngagementManager.get_instance()

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

        attacker_hits = self.attacker.stats.roll_engagement_dice(self.defender, attack_value)
        defender_hits = self.defender.stats.roll_engagement_dice(self.attacker, defence_value)

        self.attacker.stats.apply_hits(self.defender, attacker_hits)
        self.defender.stats.apply_hits(self.attacker, defender_hits)

        if defender_hits > attacker_hits:
            wavering = self.attacker
        else:
            wavering = self.defender

        breaks = wavering.stats.morale_check()

        return breaks, wavering

    def get_battle_value(self, troop):

        team = troop.team
        supporters = self.teams[team]

        return troop.stats.cohesion + (len(supporters) * 2)
