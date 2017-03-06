import os
import pygame
from source.constants import *

from source.gui.pop_up import PopUp
from source.controller.controller import Controller
from source.states.screen_layout_collection import ScreenLayoutCollection


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

    # bastardized way to simulate refreshing screen
    clear_panel = PopUp((BATTLEFIELD_FRAME_W, BATTLEFIELD_FRAME_W), BATTLEFIELD_W, BATTLEFIELD_H)
    clear_panel.image.fill(BLACK)
    clear_panel.layer = 0
    layout.add_to_draw_list(clear_panel)

    while True:

        control.handle_input()

        layout.draw(screen)

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    demo()
