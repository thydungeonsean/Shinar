from ..controller.controller import Controller


class State(object):
    
    def __init__(self, main):
        self.main = main
        self.controller = Controller.get_instance()
        self.screen_layout = None

    def init_state(self):
        raise NotImplementedError

    def deinit_state(self):
        raise NotImplementedError

    def handle_input(self):
        pass

    def render(self):
        NotImplementedError

    def run(self):
        NotImplementedError
