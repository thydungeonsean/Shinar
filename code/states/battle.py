import pygame
from state import State
from ..map.battlefield import BattleField


class Battle(State):

    def __init__(self, main):

        State.__init__(self, main)

        self.battlefield = BattleField()

    def render(self):

        screen = pygame.display.get_surface()

        self.battlefield.draw(screen)
