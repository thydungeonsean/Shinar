from image import Image
from ..entities.coord import Coord
import pygame
from ..constants import *


class TroopImage(Image):

    def __init__(self, imagename, color, x_off, y_off):

        Image.__init__(self, imagename=imagename, colorkey=WHITE)
        self.recolor(DK_GREY, color)
        self.x_offset = x_off
        self.y_offset = y_off
        self.facing = 'left'

        self.x_ani_mod = 0
        self.y_ani_mod = 0

        self.coord = Coord()

    def set_asset_path(self):

        return SPRITEPATH

    def get_pixel_coords(self):
        x, y = self.coord.get
        return (x * BATTLEGRID_SQUARE_W + self.x_offset + BATTLEFIELD_X_MARGIN + self.x_ani_mod,
         y * BATTLEGRID_SQUARE_H + self.y_offset + BATTLEFIELD_Y_MARGIN + self.y_ani_mod
         + (BATTLEGRID_SQUARE_H * .95))

    def position(self):

        self.rect.bottomleft = self.get_pixel_coords()

    def change_facing(self, new_facing):

        if self.facing != new_facing:
            self.facing = new_facing
            self.flip()

    def flip(self):

        self.image = pygame.transform.flip(self.image, True, False)

    def set_ani_mod(self, (x, y)):

        self.x_ani_mod = x
        self.y_ani_mod = y
