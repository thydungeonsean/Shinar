from ..controller.controller import Controller
from clock import Clock


class State(object):
    
    def __init__(self, main):
        self.main = main
        self.controller = Controller.get_instance()
        self.screen_layout = None

        self.clock = Clock.get_instance()

    def init_state(self):
        self.controller.bind_to_state(self)
        self.switch_screen_layout()
        raise NotImplementedError

    def deinit_state(self):
        raise NotImplementedError

    def switch_screen_layout(self):
        raise NotImplementedError

    def handle_input(self):
        self.controller.handle_input()

    def render(self):
        NotImplementedError

    def run(self):
        NotImplementedError
