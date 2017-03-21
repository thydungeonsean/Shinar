

class ScreenLayout(object):

    def __init__(self):

        self.state = None

        self.draw_list = []
        self.element_layers = {
                                0: [],
                                1: [],
                                2: [],
                                3: [],
                                4: [],
                                5: [],
                                6: []
                               }
        self.element_list = []
        self.persistent_elements = {}

    def init_state(self, state):
        self.state = state

    def deinit_state(self):
        self.state = None

    def draw(self, surface):
        for element in self.draw_list:
            element.draw(surface)

    def set_element_list(self):

        element_list = []
        keys = self.element_layers.keys()
        for layer in range(len(keys)-1, -1, -1):
            for element in self.element_layers[layer]:
                element_list.append(element)
        return element_list

    # membership methods
    def add_element(self, element, set_list=True):
        if element.visible:
            self.add_to_draw_list(element)
        self.add_to_layers(element)
        element.set_layout(self)
        if element.persistent:
            self.archive_element(element)
        if set_list:
            self.element_list = self.set_element_list()

    def add_elements(self, elements):
        for element in elements:
            self.add_element(element, set_list=False)

        self.element_list = self.set_element_list()

    def archive_element(self, element):
        # only for persistent panels
        key = element.id_key
        self.persistent_elements[key] = element

    def archive_elements(self, elements):
        for element in elements:
            self.archive_element(element)

    def close_tagged_panels(self, tag):
        tagged = filter(lambda x: x.tag == tag, self.persistent_elements.values())
        for element in tagged:
            if element in self.element_list:
                element.delete()
        self.refresh()

    def add_to_draw_list(self, new_element):
        # order not important if list empty
        if not self.draw_list:
            self.draw_list.append(new_element)
            return

        target_layer = new_element.layer

        if target_layer < self.draw_list[0].layer:  # if layer is lower than all current
            self.draw_list.insert(0, new_element)
            return

        i = 0
        for element in self.draw_list:
            if element.layer <= target_layer:
                i += 1
            if element.layer > target_layer:
                self.draw_list.insert(i, new_element)
                return
        self.draw_list.append(new_element)

    def add_to_layers(self, new_element):

        new = [new_element]
        if new_element.element_list is not None:
            for sub in new_element.element_list:
                new.append(sub)

        for element in new:
            if element.interactive:
                l = element.layer
                self.element_layers[l].append(element)

    def remove_element(self, element):
        try:
            self.draw_list.remove(element)
        except ValueError:
            pass
        l = element.layer
        self.element_layers[l].remove(element)
        self.element_list.remove(element)

    # input handling
    def click(self, point):
        # TODO - if we have layers of elements on screen, then we need a priority for click to
        # pass through so only the top element is clicked
        for element in self.element_list:
            click = element.click(point)
            if click != 0:
                return 1
        return 0  # if we return 0 on a click, nothing has been clicked

    def right_click(self, point):
        for element in self.element_list:
            click = element.right_click(point)
            if click != 0:
                return 1
        return 0

    def motion(self, point):
        for element in self.element_list:
            element.motion(point)

    def button_up(self):
        for element in self.element_list:
            element.button_up()

    def hover(self, point):
        for element in self.element_list:
            element.hover(point)

    def end_hover(self):
        for element in self.element_list:
            element.end_hover()

    # other
    def refresh(self):
        for element in self.draw_list:
            element.refresh_draw()

    def open_panel(self, id_key):
        panel = self.persistent_elements[id_key]
        self.add_element(panel)
        panel.refresh_draw()
