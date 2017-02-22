import pygame
from pygame.locals import *


class Mouse(object):

    """ Object wrapper for the pygame.mouse functions """

    instance = None
    
    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance
        
    def __init__(self):
        self.state = None

    def bind_to_state(self, state):
        self.state = state

    def unbind(self):
        self.state = None

    @property
    def position(self):
        return pygame.mouse.get_pos()

    def click(self):
        self.state.screen_layout.click(self.position)
        
    def right_click(self):
        pass

