from engagement import Engagement


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

    def determine_engagement(self, attacker, defender, direction):

        if defender.state.name == 'engage':
            if direction == 'orth':
                self.switch_engagement_direction(attacker, defender)
            else:
                self.support_engagement(attacker, defender)
        elif defender.state.name == 'support':
            self.break_support(defender)
            self.initiate_engagement(attacker, defender)
        else:
            self.initiate_engagement(attacker, defender)

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
            if t.state.name not in ('flee', 'rout'):
                t.change_state('advance')
            del self.engagement_dict[t]

    def support_engagement(self, supporter, target):
        engagement = self.get_engagement(target)
        engagement.add_supporter(supporter)
        self.engagement_dict[supporter] = engagement
        supporter.change_state('support')

    def break_support(self, troop):  # when a troop supporting an engagement is engaged or forced to retreat
        engagement = self.get_engagement(troop)
        engagement.remove_supporter(troop)
        if troop.state.name not in ('flee', 'rout'):
            troop.change_state('advance')
        del self.engagement_dict[troop]
        # TODO does harrying / firing have any effect on supporters?

    def switch_engagement_direction(self, attacker, defender):
        diagonal_engagement = self.get_engagement(defender)


        involved_troops = diagonal_engagement.involved_troops[:]
        self.deinitiate_engagement(diagonal_engagement)

        self.initiate_engagement(attacker, defender)
        for t in (attacker, defender):
            if t in involved_troops:
                involved_troops.remove(t)

        while involved_troops:
            t = involved_troops[0]
            action = t.state.get_melee_action(t)
            if action is None:
                print '********************** is this ok?'
            involved_troops.remove(t)

    def get_engagement(self, troop):
        return self.engagement_dict[troop]

    def get_opposing(self, troop):
        engagement = self.get_engagement(troop)
        return engagement.get_opposing(troop)

    # resolution
    def resolve_engagements(self):
        print 'resolving'

        ended = []
        retreats = []

        for engagement in self.engagements:
            print 'rolling'
            morale_break, troop = engagement.resolve()
            if morale_break:
                print troop.tag + ' breaks'
                ended.append(engagement)
                retreats.append(troop)

        for engagement in ended:
            self.deinitiate_engagement(engagement)

        return retreats
