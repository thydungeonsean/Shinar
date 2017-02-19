from ..battle.actions import *
from random import choice


class UnitState(object):

    def __init__(self, name, moving=False):

        self.name = name
        self.moving = moving

        self.battle = None
        self.battlefield = None
        self.scheduler = None
        self.engagements = None

    def init_battle(self, battle):

        self.battle = battle
        self.battlefield = battle.battlefield
        self.scheduler = battle.scheduler
        self.engagements = battle.engagements

    def deinit_battle(self):

        self.battle = None
        self.battlefield = None
        self.scheduler = None
        self.engagements = None

    def check_melee_target(self, troop):

        impedeing = self.check_impedeing_target(troop)
        if impedeing is not None:
            return impedeing, 'orth'

        diagonal = self.check_diagonal_target(troop)

        return diagonal, 'diag'

    def check_impedeing_target(self, troop):
        row = troop.location
        target_coord = self.get_impeding_coord(troop, row)
        for t in row.troops:
            if t.coord.get == target_coord and t.side != troop.side:
                return t
        return None

    def check_diagonal_target(self, troop):
        if troop.type == 'chariot':
            return None

        adj_rows = self.battlefield.get_adj_rows(troop.location.field_y)
        targets = []
        for row in adj_rows:
            target_coord = self.get_impeding_coord(troop, row)
            for target in row.troops:
                if target.coord.get == target_coord and target.side != troop.side:
                    targets.append(target)

        if not targets:
            return None
        if len(targets) == 1:
            return targets[0]

        return self.get_preferred_target(targets)

    @staticmethod
    def get_preferred_target(targets):

        engaged = []
        supporting = []
        free = []

        for t in targets:
            if t.state.name == 'engage':
                engaged.append(t)
            elif t.state.name == 'support':
                supporting.append(t)
            else:
                free.append(t)

        for l in [free, supporting, engaged]:
            if l:  # list has members
                return choice(l)

    def check_range_target(self, troop):
        fire_range = troop.get_fire_range()
        fire_range_set = set(fire_range)
        in_range = {}
        for t in self.battle.get_opposing_army(troop).troops:
            if t.coord.get in fire_range_set:
                in_range[t.coord.get] = t
        for coord in fire_range:
            try:
                return in_range[coord]
            except KeyError:
                pass
        return None

    @staticmethod
    def get_impeding_coord(troop, row):
        d = troop.advance_dir_mod
        cx, cy = troop.coord.get
        ry = row.field_y
        return cx + d, ry

    def check_if_locked(self, troop):
        if troop.type == 'chariot':
            return False
        row_id = troop.location.field_y
        adj = self.battlefield.get_adj_rows(row_id)
        for row in adj:
            lock_coord = self.get_impeding_coord(troop, row)
            for t in row.troops:
                if t.coord.get == lock_coord and t.side != troop.side:
                    return True

        return False

    def get_melee_action(self, troop):

        target, direction = self.check_melee_target(troop)
        if target is not None:
            if target.state.moving:
                if direction == 'orth':
                    troop.harry(target)
                    troop.change_state('harry')
                elif direction == 'diag':
                    pass  #TODO something for this state?
            else:
                self.engagements.determine_engagement(troop, target, direction)

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

    def get_next_action(self, troop):
        return True


class Advancing(UnitState):

    def __init__(self):
        UnitState.__init__(self, 'advance', True)

    def get_next_action(self, troop):

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


class Harrying(UnitState):
    def __init__(self):
        UnitState.__init__(self, 'harry')

    def get_next_action(self, troop):

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


class Firing(UnitState):
    def __init__(self):
        UnitState.__init__(self, 'fire')

    def get_next_action(self, troop):

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


class Engaging(UnitState):
    def __init__(self):
        UnitState.__init__(self, 'engage')

    def get_next_action(self, troop):

        target = self.engagements.get_opposing(troop)
        return Melee(self.scheduler, troop, target)


class Supporting(Engaging):
    def __init__(self):
        Engaging.__init__(self)
        self.name = 'support'


class Holding(UnitState):
    def __init__(self):
        UnitState.__init__(self, 'hold')

    def get_next_action(self, troop):
        return Hold(self.scheduler, troop)


class Fleeing(UnitState):
    def __init__(self):
        UnitState.__init__(self, 'flee', True)

    def get_next_action(self, troop):
        return Retreat(self.scheduler, troop)


class Routing(Fleeing):
    def __init__(self):
        Fleeing.__init__(self)
        self.name = 'rout'

    def get_next_action(self, troop):
        return Rout(self.scheduler, troop)
