from ..constants import *
from ..map.battle_grid import BattleGrid as bg
from ..entities.effect import Arrow
from random import randint


class Action(object):
    """ Action takes a troop arg as actor to carry out the action"""

    def __init__(self, scheduler, actor):

        self.scheduler = scheduler
        self.actor = actor
        self.tick = 0
        self.end_tick = self.set_end_tick()

        self.instant_effect()

    def set_end_tick(self):

        speed = self.actor.speed
        return FRAMES_PER_TURN / speed

    def increment_tick(self):

        self.tick += 1

    def check_for_completion(self):

        if self.tick >= self.end_tick:
            self.complete()

    def complete(self):

        self.final_effect()
        self.scheduler.complete_action(self)

    def run(self):

        self.perform_action()
        self.increment_tick()
        self.check_for_completion()

    def perform_action(self):
        pass

    def instant_effect(self):
        pass

    def final_effect(self):
        pass


class Hold(Action):

    def __init__(self, scheduler, actor):
        Action.__init__(self, scheduler, actor)


class Move(Action):

    def __init__(self, scheduler, actor, (ax, ay), (bx, by)):

        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by

        self.coord_mod = self.set_coord_mod()

        Action.__init__(self, scheduler, actor)

    def instant_effect(self):

        self.actor.move((self.bx, self.by))

    def set_coord_mod(self):

        start = bg.get_pixel_coord((self.ax, self.ay))
        end = bg.get_pixel_coord((self.bx, self.by))
        return start[0] - end[0]

    def perform_action(self):

        mod_x = self.lerp_x(self.ax, self.bx) + self.coord_mod
        mod_y = self.lerp_y(self.ay, self.by)
        self.actor.image.set_ani_mod((mod_x, mod_y))
        self.actor.update_pos()

    def lerp(self, a, b):

        diff = float(b - a)
        prog = float(self.tick) / float(self.end_tick)
        return diff * prog

    def lerp_x(self, a, b):

        mod = self.lerp(a, b)
        return int(mod * BATTLEGRID_SQUARE_W)

    def lerp_y(self, a, b):

        mod = self.lerp(a, b)
        return int(mod * BATTLEGRID_SQUARE_H)


class Advance(Move):

    def __init__(self, scheduler, actor):

        actor.set_image_to_advance()
        ax, ay = actor.coord.get
        bx = ax + actor.dir_mod
        by = ay
        Move.__init__(self, scheduler, actor, (ax, ay), (bx, by))

    def final_effect(self):
        if 0 > self.actor.coord.x or self.actor.coord.x > BATTLEGRID_W-1:
            self.actor.change_state('pursue')


class Pursue(Advance):

    def __init__(self, scheduler, actor):
        Advance.__init__(self, scheduler, actor)

    def complete(self):
        self.final_effect()
        self.scheduler.complete_action(self, ready=False)
        self.actor.pursue()


class Retreat(Move):

    def __init__(self, scheduler, actor):
        actor.set_image_to_retreat()
        ax, ay = actor.coord.get
        bx = ax + actor.dir_mod
        by = ay
        Move.__init__(self, scheduler, actor, (ax, ay), (bx, by))

    def instant_effect(self):
        self.actor.coord.unbind()
        self.actor.image.coord.set((self.bx, self.by))

    def final_effect(self):
        self.actor.move((self.bx, self.by))
        self.actor.coord.bind(self.actor.image.coord)
        if 0 > self.actor.coord.x or self.actor.coord.x >= BATTLEGRID_W:  # unit is off map
            self.actor.change_state('rout')
        else:
            self.actor.decrement_retreat()


class AftermathRetreat(Retreat):

    def __init__(self, scheduler, actor):
        Retreat.__init__(self, scheduler, actor)

    def complete(self):

        self.final_effect()
        self.scheduler.complete_action(self, ready=False)


class Rout(Retreat):

    def __init__(self, scheduler, actor):
        Retreat.__init__(self, scheduler, actor)

    def complete(self):
        self.final_effect()
        self.scheduler.complete_action(self, ready=False)
        self.actor.rout()


class Fire(Action):

    def __init__(self, scheduler, actor, target):
        self.target = target

        Action.__init__(self, scheduler, actor)
        self.trigger = self.set_trigger()

    def instant_effect(self):
        self.fire_arrow()

    def fire_arrow(self):
        effect = Arrow(self.actor.pixel_coord, self.target.pixel_coord)
        effect.create()

    def perform_action(self):
        if self.tick == self.trigger:
            self.fire_arrow()

    def set_trigger(self):
        trigger = self.end_tick / 4 + randint(-3, 3)
        return trigger


class Melee(Action):

    seq = (2, 3, -1, -2, -2)

    def __init__(self, scheduler, actor, target):

        Action.__init__(self, scheduler, actor)
        self.y_mod = self.set_y_mod(target)
        self.animation = self.set_animation()

    def set_animation(self):

        bumps = self.set_bumps()

        animation = {'x': [0 for i in range(self.end_tick)],
                     'y': [0 for i in range(self.end_tick)]}

        for bump in bumps:
            self.add_bump(bump, animation)
        return animation

    def set_y_mod(self, target):
        if target.coord.y > self.actor.coord.y:
            return 1
        elif target.coord.y < self.actor.coord.y:
            return -1
        return 0

    def set_bumps(self):

        if self.actor.type == 'chariot':
            bumps = [randint(0, self.end_tick - 5)]
        else:
            bumps = [randint(0, 5), self.end_tick / 2 + randint(-5, 5)]

        return bumps

    @classmethod
    def add_bump(cls, bump, animation):

        i = 0
        for mod in cls.seq:
            animation['x'][i + bump] = mod
            animation['y'][i + bump] = mod
            i += 1

    def get_animation_mod(self, axis):
        if axis == 'x':
            dir_mod = self.actor.dir_mod
        else:
            dir_mod = self.y_mod
        mod = self.animation[axis][self.tick] * dir_mod
        return mod

    def perform_action(self):

        self.actor.image.set_ani_mod((self.get_animation_mod('x'), self.get_animation_mod('y')))
        self.actor.update_pos()


class EngagementMelee(Melee):

    def __init__(self, scheduler, actor, target):

        Melee.__init__(self, scheduler, actor, target)

    def set_end_tick(self):

        speed = 2
        return FRAMES_PER_TURN / speed

    def set_bumps(self):

        return [randint(0, 5), self.end_tick / 2 + randint(-5, 5)]

    def complete(self):

        self.final_effect()
        self.scheduler.complete_action(self, ready=False)
