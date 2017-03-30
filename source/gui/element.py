from panel import Panel


class Element(Panel):

    """
    Element is visible to controller and can be interacted with
    """

    def __init__(self, pos, w, h, layer, **kwargs):
        Panel.__init__(self, pos, w, h, layer, **kwargs)
        self.interactive = True
        self.hover_component = None

    def set_hover_component(self, hover):
        self.hover_component = hover

    def click(self, point):
        if self.point_is_over(point):
            if self.owner is None:
                self.perform_function(self)
            elif self.owner.point_is_over(point):
                self.perform_function(self)
            else:
                return 0
        else:
            return 0

    def right_click(self, point):
        return 0

    def motion(self, point):
        pass

    def button_up(self):
        pass

    def hover(self, point):
        if self.hover_component is not None and self.point_is_over(point):
                self.hover_component.hovering()

    def end_hover(self):
        if self.hover_component is not None:
            self.hover_component.end_hover()

    def perform_function(self, dummy):
        raise NotImplementedError
