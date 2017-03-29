import pygame
from ..states.state import State
from ..states.observer import Observer, ReporterComponent
from ..map.battlefield import BattleField
from ..entities.army import Army
from ..images.image import Image
from battle_scheduler import BattleScheduler
from ..entities.effect import EffectManager
from engagement_manager import EngagementManager
from battle_scale import BattleScale
from ..constants import BATTLEFIELD_COORD, BATTLEFIELD_W, BATTLEFIELD_H
from ..states.screen_layout_collection import ScreenLayoutCollection
from ..gui.troop_handle import TroopHandle
from ..gui.panel import Panel


class Battle(State):

    def __init__(self, main, left_army, right_army):

        State.__init__(self, main)

        self.battlefield = BattleField()
        self.battle_view = self.set_battle_view()
        self.battlefield_ui_panel = self.set_ui_panel()

        self.left_army = left_army
        self.left_army.set_side('left')
        self.right_army = right_army
        self.right_army.set_side('right')

        self.engagements = EngagementManager.get_instance()

        self.scheduler = BattleScheduler.get_instance()
        self.turn_ready = True

        self.effects = EffectManager.get_instance()

        self.battle_scale = BattleScale.get_instance()

        self.autoassign()

        self.init_state()

    def init_state(self):
        self.switch_screen_layout()
        self.init_battle()
        self.controller.bind_to_state(self)

    def deinit_state(self):
        self.screen_layout.deinit_state()

    def init_battle(self):
        self.engagements.init_battle(self)
        self.scheduler.init_battle(self)
        self.battle_scale.init_battle(self)

        # temporary - will be triggered by end of deployment phase
        self.add_troop_handles()

    def switch_screen_layout(self):

        self.screen_layout = ScreenLayoutCollection.BATTLE_LAYOUT
        ScreenLayoutCollection.init_battle_layout()
        self.screen_layout.init_state(self)

    def set_battle_view(self):

        w = self.battlefield.map_image_rect.w
        h = self.battlefield.map_image_rect.h
        view = Image.get_sized_image(w, h)
        view.position(BATTLEFIELD_COORD)
        return view

    def set_ui_panel(self):
        return Panel(BATTLEFIELD_COORD, BATTLEFIELD_W, BATTLEFIELD_H, 0, visible=False).parent()

    def render(self):

        screen = pygame.display.get_surface()

        self.battlefield.draw(self.battle_view)
        self.battle_scale.draw(self.battle_view)
        self.effects.draw(self.battle_view)
        self.battle_view.draw(screen)

        self.screen_layout.draw(screen)

    def add_troop_handles(self):

        for troop in self.active_troops:
            troop_handle = TroopHandle(troop)
            self.battlefield_ui_panel.attach_element(troop_handle)
            self.screen_layout.add_element(troop_handle)

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
                self.assign_troop(troop, row)

                troop.set_reporter_component(ReporterComponent(Observer.get_instance()))

        for type in Army.troop_types:
            roster = self.right_army.stacks[type]
            for i in range(roster.len()):
                troop = self.right_army.get_troop(type)
                row = self.battlefield.get_empty_row('right')
                self.assign_troop(troop, row)

                troop.set_reporter_component(ReporterComponent(Observer.get_instance()))

    def assign_troop(self, troop, row):
        row.assign_to_row(troop, troop.side)
        troop.activate()

    @property
    def active_left_troops_count(self):
        count = 0
        for troop in self.left_army.troops:
            if troop.active:
                count += 1
        return count

    @property
    def active_right_troops_count(self):
        count = 0
        for troop in self.right_army.troops:
            if troop.active:
                count += 1
        return count

    @property
    def active_troops(self):
        active = []
        for troop in self.left_army.troops:
            if troop.active:
                active.append(troop)
        for troop in self.right_army.troops:
            if troop.active:
                active.append(troop)
        return active

    def run(self):
        self.scheduler.run()
        self.effects.run()
        self.battle_scale.run()
