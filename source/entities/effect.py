from random import *
from ..constants import *
import pygame
from ..map.battle_grid import BattleGrid


class Effect(object):

    def __init__(self):
        self.manager = EffectManager.get_instance()

    def run(self):
        pass

    def draw(self, surface):
        pass

    def end(self):
        self.manager.remove(self)

    def create(self):
        self.manager.add(self)


class Arrow(Effect):

    def __init__(self, origin, (dx, dy)):
        self.origin = origin
        self.destination = (dx+randint(0, 15), dy+randint(0, 15))
        self.rect = pygame.Rect((0, 0), (SCALE*4, SCALE))
        self.rect.topleft = self.origin

        self.duration = 25
        self.tick = 0

        Effect.__init__(self)

    def run(self):
        if self.tick > self.duration:
            self.end()

        self.move_arrow()

        self.increment_tick()

    def increment_tick(self):
        self.tick += 1

    def draw(self, surface):
        pygame.draw.rect(surface.image, WHITE, self.rect)

    def move_arrow(self):
        ax, ay = self.origin
        bx, by = self.destination
        x = ax + self.lerp(ax, bx) + BATTLEGRID_SQUARE_W/2  # TODO what's goin on here
        y = ay + self.lerp(ay, by) + BATTLEGRID_SQUARE_H
        self.rect.topleft = (x, y)

    def lerp(self, a, b):
        diff = float(b - a)
        prog = float(self.tick) / float(self.duration)
        return int(diff * prog)


class EffectManager(object):

    instance = None

    @classmethod
    def get_instance(cls):
        if EffectManager.instance is None:
            EffectManager.instance = cls()
            return EffectManager.instance
        else:
            return EffectManager.instance

    def __init__(self):

        self.effects = []

    def remove(self, effect):

        self.effects.remove(effect)

    def draw(self, surface):

        for effect in self.effects:
            effect.draw(surface)

    def run(self):
        for effect in self.effects:
            effect.run()

    def add(self, effect):
        self.effects.append(effect)
