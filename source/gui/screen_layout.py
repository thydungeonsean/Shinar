

class ScreenLayout(object):

    def __init__(self):
        self.elements = []
        self.panels = []

    def draw(self, surface):
        for panel in self.panels:
            panel.draw(surface)
        for element in self.elements:
            element.draw(surface)

    def add_panel(self, panel):

        self.panels.append(panel)

    def add_panels(self, panels):
        for panel in panels:
            self.add_panel(panel)

    def add_button(self, button):
        self.elements.append(button)

    def click(self, point):
        # TODO - if we have layers of elements on screen, then we need a priority for click to
        # pass through so only the top element is clicked
        for element in self.elements:
            element.click(point)
