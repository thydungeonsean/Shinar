import pygame
from state import State
from ..map.battlefield import BattleField
from ..entities.army import Army
from random import *


class Battle(State):

    def __init__(self, main, left_army, right_army):

        State.__init__(self, main)

        self.battlefield = BattleField()

        self.left_army = left_army
        self.left_army.set_side('left')
        self.right_army = right_army
        self.right_army.set_side('right')

        self.autoassign()

    def render(self):

        screen = pygame.display.get_surface()

        self.battlefield.draw(screen)

    # for testing - auto assign troops to rows in battlefield
    def autoassign(self):

        for type in Army.troop_types:
            roster = self.left_army.stacks[type]
            for i in range(roster.len()):
                troop = self.left_army.get_troop(type)
                row = self.battlefield.get_empty_row('left')
                row.assign_to_row(troop, 'left')

        for type in Army.troop_types:
            roster = self.right_army.stacks[type]
            for i in range(roster.len()):
                troop = self.right_army.get_troop(type)
                troop.change_facing()
                troop.direction = -1
                row = self.battlefield.get_empty_row('right')
                row.assign_to_row(troop, 'right')
