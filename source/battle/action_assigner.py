from actions import *


class ActionAssigner(object):

    instance = None

    @classmethod
    def get_instance(cls):
        if ActionAssigner.instance is None:
            ActionAssigner.instance = cls()
        return ActionAssigner.instance

    def __init__(self):
        self.battle = None
        self.scheduler = None
        self.battle_field = None
        self.engagements = None

    def init_battle(self, battle, scheduler):
        self.scheduler = scheduler
        self.battle = battle
        self.battle_field = battle.battlefield
        self.engagements = battle.engagements

    def check_melee_target(self, troop):
        row = troop.location
        target_coord = self.get_impeding_coord(troop, row)
        for t in row.troops:
            if t.coord == target_coord and t.side != troop.side:
                return t
        return None

    def check_range_target(self, troop):
        fire_range = troop.get_fire_range()
        fire_range_set = set(fire_range)
        in_range = {}
        for t in self.battle.get_opposing_army(troop).troops:
            if t.coord in fire_range_set:
                in_range[t.coord] = t
        for coord in fire_range:
            try:
                return in_range[coord]
            except KeyError:
                pass
        return None

    def get_impeding_coord(self, troop, row):
        #d = troop.dir_mod # TODO, this fix might not work
        d = troop.advance_dir_mod
        cx, cy = troop.coord
        ry = row.field_y
        return cx + d, ry

    def check_if_locked(self, troop):
        if troop.type == 'chariot':
            return False
        row_id = troop.location.field_y
        adj = self.battle_field.get_adj_rows(row_id)
        for row in adj:
            lock_coord = self.get_impeding_coord(troop, row)
            for t in row.troops:
                if t.coord == lock_coord and t.side != troop.side:
                    return True

        return False

    def get_next_action(self, troop):

        if troop.needs_check:
            troop.morale_check()

        if troop.state in ('advance', 'harry', 'fire'):
            action = self.get_advancing_action(troop)
        elif troop.state == 'support':
            action = Hold(self.scheduler, troop)
        elif troop.state == 'engage':
            action = self.continue_melee(troop)
        elif troop.state == 'hold':
            action = Hold(self.scheduler, troop)
        elif troop.state == 'flee':
            action = Retreat(self.scheduler, troop)
        elif troop.state == 'rout':
            action = Retreat(self.scheduler, troop)

        return action

    def get_melee_action(self, troop):

        target = self.check_melee_target(troop)
        if target is not None:
            if target.state in ('advance', 'flee', 'rout'):
                troop.change_state('harry')
                troop.harry(target)
            elif target.state == 'fire':
                self.engagements.initiate_engagement(troop, target)
            elif target.state == 'support':
                self.engagements.initiate_engagement(troop, target)
                print 'breaking support - action assigner'
            elif target.state == 'harry':
                self.engagements.initiate_engagement(troop, target)
                print 'break harry'
            else:
                self.engagements.initiate_engagement(troop, target)

            return Melee(self.scheduler, troop, target)
        else:
            return None

    def get_ranged_action(self, troop):

        target = self.check_range_target(troop)
        if target is not None:
            troop.change_state('fire')
            troop.fire(target)
            return Fire(self.scheduler, troop, target)
        return None

    def continue_melee(self, troop):

        target = self.engagements.get_opposing(troop)
        return Melee(self.scheduler, troop, target)

    def get_advancing_action(self, troop):

        melee = self.get_melee_action(troop)
        if melee is not None:
            return melee

        if troop.type == 'archer':
            ranged = self.get_ranged_action(troop)
            if ranged is not None:
                return ranged

        locked = self.check_if_locked(troop)
        if locked:
            return Hold(self.scheduler, troop)

        # free to advance
        return Advance(self.scheduler, troop)

    def get_engagement_melees(self, e):

        actions = [EngagementMelee(self.scheduler, e.attacker, e.defender),
                   EngagementMelee(self.scheduler, e.defender, e.attacker)]

        return actions

    def get_aftermath_actions(self):

        retreating = []
        for troop in self.battle.left_army.troops:  # TODO make it so it's only fresh retreats
            if troop.state in ('rout', 'flee'):
                retreating.append(troop)
        for troop in self.battle.right_army.troops:
            if troop.state in ('rout', 'flee'):
                retreating.append(troop)

        actions = []

        for troop in retreating:
            retreat = Retreat(self.scheduler, troop)
            actions.append(retreat)

        return actions
