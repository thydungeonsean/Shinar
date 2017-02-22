import os
import pygame
from pygame.locals import *
from source.constants import *

from source.gui.panel import Panel
from source.gui.button import Button
from source.states.screen_layout_collection import ScreenLayoutCollection

from source.controller.mouse import Mouse


def handle_input(mouse):

    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            mouse.click()


def button_push():
    print 'push!'


def set_elements():

    screen = pygame.display.get_surface()

    layout = ScreenLayoutCollection.BATTLE_LAYOUT
    layout.draw(screen)


def demo():

    pygame.init()

    os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
    pygame.display.set_mode((SCREENW, SCREENH))

    ScreenLayoutCollection.init_battle_layout()
    mouse = Mouse.get_instance()

    clock = pygame.time.Clock()

    set_elements()

    while True:

        handle_input(mouse)

        pygame.display.update()
        clock.tick(60)

    # pygame.display.update()
    # pygame.image.save(screen, 'gui.png')
    #
    # while pygame.event.wait().type != KEYDOWN:
    #     clock.tick(60)


if __name__ == '__main__':
    demo()
