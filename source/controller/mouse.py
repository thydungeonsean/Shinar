import pygame
from click_subscriber import ClickObserver


class Mouse(object):

    """ Object wrapper for the pygame.mouse functions """

    instance = None

    HOVERDELAY = 40

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance
        
    def __init__(self):
        self.state = None
        self.hover_count = 0
        self.click_observer = ClickObserver()

    def bind_to_state(self, state):
        self.state = state

    def unbind(self):
        self.state = None

    @property
    def position(self):
        return pygame.mouse.get_pos()

    def click(self):
        click = self.state.screen_layout.click(self.position)
        #if click == 0:
        self.click_observer.left_click()  # TODO - maybe click always registered
        self.reset_hover()
        
    def right_click(self):
        click = self.state.screen_layout.right_click(self.position)
        #if click == 0:
        self.click_observer.right_click()
        self.reset_hover()

    def motion(self):
        self.state.screen_layout.motion(self.position)

    def button_up(self):
        self.state.screen_layout.button_up()

    def hover(self):
        self.hover_count += 1
        if self.hover_count >= Mouse.HOVERDELAY:
            self.state.screen_layout.hover(self.position)

    def reset_hover(self):
        if self.hover_count > 0:
            self.state.screen_layout.end_hover()
        self.hover_count = 0


