from element import Element
from ..constants import FERTILE_GREEN, scale
from font import MenuFont
from ..controller.mouse import Mouse


class DragBox(Element):

    def __init__(self, pos, w, h):
        Element.__init__(self, pos, w, h, 4)
        self.parent()
        self.state = 0
        self.anchor_x = 0
        self.anchor_y = 0

    def set_color(self):
        return FERTILE_GREEN

    def perform_function(self, dummy):
        mx, my = Mouse.get_instance().position
        if self.state == 0:
            self.state = 1
            self.anchor_x = self.x - mx
            self.anchor_y = self.y - my

    def button_up(self):
        if self.state == 1:
            self.state = 0
            self.anchor_x = 0
            self.anchor_y = 0

    def motion(self, pos):
        if self.state == 1:
            self.coord.set(self.anchored_coord(pos))
            self.reset_pos()
            self.layout.refresh()  # TODO - might be too inefficient if redrawing all GUI is slow

    def anchored_coord(self, (x, y)):
        return x + self.anchor_x, y + self.anchor_y

    def toggle_redraw(self):
        pass


class FPSBox(DragBox):

    def __init__(self, pos, w, h):
        DragBox.__init__(self, pos, w, h)
        self.fps = 0

    def draw(self, surface):
        if self.needs_redraw:
            draw = self.check_fps()
            if draw:
                self.draw_fps()
            surface.blit(self.image, self.rect)
            self.toggle_redraw()

    def check_fps(self):
        old_fps = self.fps
        self.fps = self.layout.state.clock.get_fps()
        if old_fps == self.fps:
            return False
        return True

    def draw_fps(self):
        self.image.fill(self.color)
        self.draw_text(str(self.fps))

    def draw_text(self, text):
        f = MenuFont.get_instance()
        f.draw(self.image, (scale(2), scale(-4)), text)

