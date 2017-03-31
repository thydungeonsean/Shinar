from pop_up import PopUp
from box_border import BoxBorder
from ..constants import *
from ..images.image import GUIImage
from font import MenuFont
from position_grid import PositionGrid
import pygame


class TroopDisplay(PopUp):

    width = scale(40)
    height = scale(40)

    coh = GUIImage('cohesion')
    mor = GUIImage('morale')
    brk = GUIImage('break', colorkey=WHITE)

    icon_x = scale(2)
    coh_y = scale(2)
    mor_y = scale(10)
    break_y = scale(19)

    coh.position((icon_x, coh_y))
    mor.position((icon_x, mor_y))
    brk.position((icon_x, break_y))

    coh_stat_coord = (scale(14), coh_y-scale(5))
    mor_stat_coord = (scale(14), mor_y-scale(5))

    break_scale_w = scale(30)
    break_scale_x = scale(5)
    break_scale_y = scale(24)

    break_icon_inc = break_scale_w / 10

    def __init__(self, troop):

        self.grid = PositionGrid(scale(7), scale(7), rows=3, columns=3, gap=scale(2), x=0, y=0)

        self.display, self.display_rect = self.set_display()
        self.border = BoxBorder.frame_dimensions(TroopDisplay.width, TroopDisplay.height)

        self.icons = self.set_icons()

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

    def set_icons(self):

        td = TroopDisplay

        h = td.height
        w = scale(10)
        icons = pygame.Surface((w, h)).convert()
        icons.fill(BLACK)

        td.coh.draw(icons)
        td.mor.draw(icons)

        return icons

    def update_stats(self, troop):
        f = MenuFont.get_instance()
        coh = str(troop.stats.cohesion)
        f.draw(self.display, TroopDisplay.coh_stat_coord, coh, color=PURPLE)
        mor = str(troop.stats.morale)
        f.draw(self.display, TroopDisplay.mor_stat_coord, mor, color=MORALE_RED)

        self.update_break_scale(troop)

    def update_break_scale(self, troop):

        td = TroopDisplay

        w = int(td.break_scale_w * troop.stats.morale_per)

        r = pygame.Rect((td.break_scale_x, td.break_scale_y), (w, scale(2)))

        if troop.stats.morale_per > .7:
            c = MORALE_GREEN
        elif troop.stats.morale_per > .4:
            c = MORALE_YELLOW
        else:
            c = MORALE_RED
        pygame.draw.rect(self.display, c, r)

        break_x = td.break_icon_inc * troop.stats.break_points + td.icon_x
        td.brk.position((break_x, td.break_y))
        td.brk.draw(self.display)

    def update_display(self, troop):
        self.display.fill(BLACK)
        self.display.blit(self.icons, self.icons.get_rect())
        self.update_stats(troop)

    def render_display(self):
        self.border.draw(self.image)
        self.image.blit(self.display, self.display_rect)
