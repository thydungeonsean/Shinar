import pygame
from ..states.state import State
from ..map.battlefield import BattleField
from ..entities.army import Army
from ..images.image import Image
from battle_scheduler import BattleScheduler
from ..entities.effect import EffectManager
from engagement_manager import EngagementManager


class Battle(State):

    def __init__(self, main, left_army, right_army):

        State.__init__(self, main)

        self.battlefield = BattleField()
        self.battle_view = self.set_battle_view()

        self.left_army = left_army
        self.left_army.set_side('left')
        self.right_army = right_army
        self.right_army.set_side('right')

        self.engagements = EngagementManager.get_instance()
        self.engagements.init_battle(self)

        self.scheduler = BattleScheduler.get_instance()
        self.scheduler.init_battle(self)
        self.turn_ready = True

        self.effects = EffectManager.get_instance()

        self.autoassign()
        #self.assign_troops()

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
                row = self.battlefield.get_empty_row('left')
                row.assign_to_row(troop, 'left')

        for type in Army.troop_types:
            roster = self.right_army.stacks[type]
            for i in range(roster.len()):
                troop = self.right_army.get_troop(type)
                row = self.battlefield.get_empty_row('right')
                row.assign_to_row(troop, 'right')

    # testing
    def assign_troops(self):

        t = self.left_army.get_troop('infantry')
        row = self.battlefield.rows[0]
        row.assign_to_row(t, 'left')
        t = self.right_army.get_troop('chariot')
        row = self.battlefield.rows[0]
        row.assign_to_row(t, 'right')

    def run(self):
        self.scheduler.run()
        self.effects.run()
