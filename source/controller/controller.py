import pygame
import sys
from mouse import Mouse
from pygame.locals import *


class Controller(object):

    key_bind = {
        'esc': K_ESCAPE,
        'ret': K_RETURN
    }




    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):

        self.mouse = Mouse.get_instance()
        self.state = None

    def bind_to_state(self, state):
        self.state = state
        self.mouse.bind_to_state(state)

    def unbind(self):
        self.state = None
        self.mouse.unbind()

    def handle_input(self):

        for event in pygame.event.get():

            if event.type == QUIT:
                self.end_program()

            elif event.type == KEYDOWN:
                if event.key == self.key('esc'):
                    self.end_program()

                elif event.key == self.key('ret'):
                    pass

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    print event
                    self.mouse.click()
                elif event.button == 3:
                    print event
                    self.mouse.right_click()

    def key(self, k):
        cls = Controller
        return cls.key_bind[k]

    def end_program(self):
        pygame.quit()
        sys.exit()
        quit()