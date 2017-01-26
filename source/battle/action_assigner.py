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
        self.engagement_manager = None

    def init_battle(self, battle, scheduler):
        self.scheduler = scheduler
        self.battle = battle
        self.battle_field = battle.battlefield
        self.engagement_manager = battle.engagements

    def get_next_action(self, troop):

        if troop.state == 'advance':
            action = self.get_advancing_action(troop)
        elif troop.state == 'flee':
            action = Retreat(self.scheduler, troop)

        return action

    def get_advancing_action(self, troop):

        target = self.check_melee_target(troop)
        if target is not None:
            if target.state in ('advance', 'flee', 'rout'):
                # troop.harry(target)
                troop.change_state('harry')
                print '%s is harrying %s' % (troop, target)
            else:
                # troop.engage(target)
                troop.change_state('engage')

            return Engage(self.scheduler, troop, target)  # Engage(troop, target)

        if troop.type == 'archer':
            target = self.check_range_target(troop)
            if target is not None:
                return Fire(self.scheduler, troop, target)

        locked = self.check_if_locked(troop)
        if locked:
            return Hold(self.scheduler, troop)

        # free to advance
        return Advance(self.scheduler, troop)

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
        d = troop.direction
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
