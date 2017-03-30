from pop_up import PopUp
from box_border import BoxBorder
from ..constants import scale, BLACK
import pygame


class TroopDisplay(PopUp):

    width = scale(40)
    height = scale(40)

    def __init__(self, troop):

        self.display, self.display_rect = self.set_display()
        self.border = BoxBorder.frame_dimensions(TroopDisplay.width, TroopDisplay.height)

        w = self.border.w
        h = self.border.h

        PopUp.__init__(self, (0, 0), w, h)
        self.set_mouse_pos()

        self.update_display(troop)
        self.render_display()

    def set_display(self):

        display = pygame.Surface((TroopDisplay.width, TroopDisplay.height)).convert()
        display.fill(BLACK)
        rect = display.get_rect()
        rect.topleft = BoxBorder.THIN_W, BoxBorder.THIN_W

        return display, rect

    def update_display(self, troop):
        pass

    def render_display(self):
        self.border.draw(self.image)
        self.image.blit(self.display, self.display_rect)
