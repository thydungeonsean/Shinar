import os
import pygame
from pygame.locals import *
from source.constants import *


from source.controller.controller import Controller
from source.gui.panel import Panel
from source.gui.button import Button
from source.states.screen_layout_collection import ScreenLayoutCollection

from source.controller.mouse import Mouse


class state(object):

    def __init__(self, screen):
        self.screen_layout = screen


def button_push():
    print 'push!'


def set_elements():

    screen = pygame.display.get_surface()

    layout = ScreenLayoutCollection.BATTLE_LAYOUT
    layout.draw(screen)


def demo():

    pygame.init()

    os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
    screen = pygame.display.set_mode((SCREENW, SCREENH))

    ScreenLayoutCollection.init_battle_layout()

    s = state(ScreenLayoutCollection.BATTLE_LAYOUT)
    control = Controller.get_instance()
    control.bind_to_state(s)

    clock = pygame.time.Clock()

    set_elements()

    layout = ScreenLayoutCollection.BATTLE_LAYOUT

    while True:

        control.handle_input()

        layout.draw(screen)

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    demo()
