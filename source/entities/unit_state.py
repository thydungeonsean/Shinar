

class UnitState(object):

    def __init__(self):

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
        row = troop.location
        target_coord = self.get_impeding_coord(troop, row)
        for t in row.troops:
            if t.coord.get == target_coord and t.side != troop.side:
                return t
        return None

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

    def get_impeding_coord(self, troop, row):
        d = troop.advance_dir_mod
        cx, cy = troop.coord.get
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


class Advancing(UnitState):

    def __init__(self):
        UnitState.__init__(self)


class Harrying(UnitState):
    def __init__(self):
        UnitState.__init__(self)


class Supporting(UnitState):
    def __init__(self):
        UnitState.__init__(self)


class Firing(UnitState):
    def __init__(self):
        UnitState.__init__(self)


class Engaging(UnitState):
    def __init__(self):
        UnitState.__init__(self)


class Holding(UnitState):
    def __init__(self):
        UnitState.__init__(self)


class Fleeing(UnitState):
    def __init__(self):
        UnitState.__init__(self)


class Routing(Fleeing):
    def __init__(self):
        Fleeing.__init__(self)
