from ..constants import *
from ..map.battle_grid import BattleGrid as bg
from effect import Arrow
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
            self.scheduler.complete_action(self)

    def run(self):
        self.increment_tick()
        self.perform_action()
        self.check_for_completion()

    def perform_action(self):
        pass

    def instant_effect(self):
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

        self.start_x, self.start_y = bg.get_pixel_coord((ax, ay))
        self.end_x, self.end_y = bg.get_pixel_coord((bx, by))

        Action.__init__(self, scheduler, actor)

    def instant_effect(self):
        self.actor.move((self.bx, self.by))

    def perform_action(self):
        imgx = self.lerp_x(self.ax, self.bx)
        imgy = self.lerp_y(self.ay, self.by)
        x = self.start_x + imgx
        y = self.start_y + imgy
        self.actor.position_image((x, y))

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
        ax, ay = actor.coord
        bx = ax + actor.direction
        by = ay
        Move.__init__(self, scheduler, actor, (ax, ay), (bx, by))


class Retreat(Move):

    def __init__(self, scheduler, actor):
        ax, ay = actor.coord
        bx = ax - actor.direction
        by = ay
        Move.__init__(self, scheduler, actor, (ax, ay), (bx, by))

    def instant_effect(self):
        self.actor.move((self.bx, self.by))
        self.actor.change_facing()


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
        trigger = self.end_tick/4 + randint(-3, 3)
        return trigger


class Engage(Action):

    def __init__(self, scheduler, actor, target):

        self.x_mod = 0
        self.y_mod = 0

        Action.__init__(self, scheduler, actor)
        self.triggers = self.set_triggers()

    def set_triggers(self):

        triggers = [randint(0, 8), self.end_tick/2+randint(-5, 5)]

        return triggers

    def perform_action(self):

        if self.tick in self.triggers:
            x, y = self.actor.image.rect.topleft
            self.actor.position_image((x+10 , y))
