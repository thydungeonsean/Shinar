import pygame
from state import State
from ..map.battlefield import BattleField
from ..entities.army import Army
from random import *
from ..images.image import Image
from battle_scheduler import BattleScheduler
from ..entities.effect import EffectManager


class Battle(State):

    def __init__(self, main, left_army, right_army):

        State.__init__(self, main)

        self.battlefield = BattleField()
        self.battle_view = self.set_battle_view()

        self.left_army = left_army
        self.left_army.set_side('left')
        self.right_army = right_army
        self.right_army.set_side('right')

        self.scheduler = BattleScheduler.get_instance()
        self.scheduler.init_battle(self)

        self.effects = EffectManager.get_instance()

        self.autoassign()

    def set_battle_view(self):
        w = self.battlefield.map_image_rect.w
        h = self.battlefield.map_image_rect.h
        view = Image.get_sized_image(w, h)
        return view

    def render(self):

        screen = pygame.display.get_surface()

        self.battlefield.draw(self.battle_view)
        self.effects.draw(self.battle_view)
        self.battle_view.draw(screen)

    def get_opposing_army(self, troop):
        if troop.side == 'left':
            return self.right_army
        elif troop.side == 'right':
            return self.left_army

    # for testing - auto assign troops to rows in battlefield
    def autoassign(self):

        for type in Army.troop_types:
            roster = self.left_army.stacks[type]
            for i in range(roster.len()):
                troop = self.left_army.get_troop(type)
                troop.set_side('left')
                row = self.battlefield.get_empty_row('left')
                row.assign_to_row(troop, 'left')

        for type in Army.troop_types:
            roster = self.right_army.stacks[type]
            for i in range(roster.len()):
                troop = self.right_army.get_troop(type)
                troop.set_side('right')
                troop.change_facing()
                troop.direction = -1
                row = self.battlefield.get_empty_row('right')
                row.assign_to_row(troop, 'right')

    def run(self):
        self.scheduler.run()
        self.effects.run()
