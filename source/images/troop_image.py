from image import Image
from ..entities.coord import Coord, TroopImageCoord
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
        self.image_coord = TroopImageCoord(self.coord, self)

    def set_asset_path(self):

        return SPRITEPATH

    def get_pixel_coords(self):
        return self.image_coord.get

    def position(self):

        self.rect.topleft = self.get_pixel_coords()

    def change_facing(self, new_facing):

        if self.facing != new_facing:
            self.facing = new_facing
            self.flip()

    def flip(self):

        self.image = pygame.transform.flip(self.image, True, False)

    def set_ani_mod(self, (x, y)):

        self.x_ani_mod = x
        self.y_ani_mod = y
        self.image_coord.update(self.coord.get)
