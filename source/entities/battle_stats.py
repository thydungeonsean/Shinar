from random import randint


class BattleStats(object):

    def_infantry = {
        'coh': 10,
        'mor': 10,
        'speed': 2,
        'str': 'chariot',
        'weak': 'archer',
        'x_ret': 0
    }

    def_archer = {
        'coh': 5,
        'mor': 10,
        'speed': 3,
        'str': 'infantry',
        'weak': 'archer',
        'x_ret': 0
    }

    def_chariot = {
        'coh': 10,
        'mor': 10,
        'speed': 5,
        'str': 'archer',
        'weak': 'infantry',
        'x_ret': 1
    }

    default_stats = {
        'infantry': def_infantry,
        'archer': def_archer,
        'chariot': def_chariot
    }

    def __init__(self, owner, troop_type, **kwargs):

        self.owner = owner
        self.troop_type = troop_type

        stats = BattleStats.default_stats[self.troop_type]

        self.base_cohesion = stats['coh']
        self.max_cohesion = stats['coh']
        self.base_morale = stats['mor']
        self.max_morale = stats['mor']
        self.base_speed = stats['speed']

        self.strength = stats['str']
        self.weakness = stats['weak']

        self.bonus_coh = 0
        self.bonus_mor = 0
        self.bonus_speed = 0

        self.break_points = 0
        self.retreat_count = 0

        self.extra_retreats = stats['x_ret']

        self.needs_morale_check = False

    @property
    def cohesion(self):
        return self.base_cohesion + self.bonus_coh

    @property
    def morale(self):
        return self.base_morale + self.bonus_mor

    @property
    def speed(self):
        return self.base_speed + self.bonus_speed

    def damage_cohesion(self):
        self.base_cohesion -= 1
        if self.base_cohesion <= 1:
            self.base_cohesion = 1

    def damage_morale(self):
        self.base_morale -= 1
        if self.base_morale < 1:
            self.base_morale = 0

    def add_break_point(self):
        self.break_points += 1

    def reset_break_points(self):
        self.break_points = 0

    def set_retreat_count(self, margin):
        self.retreat_count = margin + self.extra_retreats

    def decrement_retreat(self):
        self.retreat_count -= 1
        if self.retreat_count <= 0:
            self.owner.change_state('advance')
            self.owner.set_image_to_advance()
            self.owner.reporter_component.send_report('unit', self.owner.side, 'recover')

    def hit(self, target):

        effect = randint(0, 2)
        if effect == 0:
            target.stats.damage_cohesion()
            self.owner.reporter_component.send_report('unit', self.owner.side, 'hit')
        elif effect == 1:
            target.stats.damage_morale()
            self.owner.reporter_component.send_report('unit', self.owner.side, 'hit')
        elif effect == 2:
            target.stats.add_break_point()

    def harry(self, target):
        self.hit(target)
        target.check()

    def roll_engagement_dice(self, target, num):

        hits = 0

        str = self.set_die_str(target)
        for i in range(num):
            roll = randint(1, str)
            if roll >= 4:
                hits += 1

        return hits

    def apply_hits(self, target, hits):
        for hit in range(hits):
            self.hit(target)

    def set_die_str(self, target):
        if target.type == self.strength:
            return 8
        elif target.type == self.weakness:
            return 4
        return 6

    def morale_check(self):
        self.needs_morale_check = False
        check = randint(1, 10)
        if check > (self.morale - self.break_points):
            # morale failure
            margin = check - (self.morale - self.break_points)
            self.set_retreat_count(margin)
            self.breaks()
            return True
        return False

    def check(self):
        self.needs_morale_check = True

    def breaks(self):
        self.owner.change_state('flee')
        self.reset_break_points()

    # archer
    @property
    def fire_strength(self):
        strength = self.cohesion/2
        if strength < 1:
            strength = 1
        return strength

    def fire(self, target):
        if self.troop_type != 'archer':
            raise Exception('Non - archer unit is firing?!?')

        hits = self.roll_engagement_dice(target, self.fire_strength)
        self.apply_hits(target, hits)
        # TODO - should firing cause supporters to break in battle?
        if target.state.name not in ('engage', 'support'):
            target.check()
