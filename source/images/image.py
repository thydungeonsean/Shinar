import pygame
from ..constants import *
import os
from ..map.battle_grid import BattleGrid


REL = '\\..'


class Image(object):

    @classmethod
    def get_sized_image(cls, w, h):
        instance = cls()
        instance.image = pygame.Surface((w, h))
        instance.rect = instance.set_dims()
        return instance

    def __init__(self, imagename=None, colorkey=None):
    
        self.x_offset = 0
        self.y_offset = 0
    
        self.asset_path = self.set_asset_path()
        self.image = self.init_image(imagename)
        if colorkey is not None:
            self.set_colorkey(colorkey)
        self.rect = self.set_dims()

    def set_dims(self):

        rect = self.image.get_rect()
        return rect

    def set_asset_path(self):

        return TILEPATH
        
    def init_image(self, imagename):
    
        if imagename is None:
            img = pygame.Surface((TILEW, TILEH))
            img.fill(WHITE)
            return img
        base = self.load_image(imagename)
        w = base.get_width()
        h = base.get_height()
        scaled = pygame.transform.scale(base, (scale(w), scale(h)))
        
        return scaled

    def load_image(self, imagename):

        path = os.path.dirname(__file__) + REL + self.asset_path + imagename + '.png'
        try:
            return pygame.image.load(path)
        except pygame.error:
            alt_path = os.path.dirname(__file__) + REL + self.asset_path + imagename + '_placeholder.png'
            return pygame.image.load(alt_path)

    def position(self, (x, y)):
    
        self.rect.topleft = ((x*TILEW)+self.x_offset, (y*TILEH)+self.y_offset)
        
    def draw(self, surface):
        
        surface.blit(self.image, self.rect)
        
    def blit(self, image, rect):

        self.image.blit(image, rect)
        
    def recolor(self, color_a, color_b):
    
        pix_array = pygame.PixelArray(self.image)
        pix_array.replace(color_a, color_b, 0.01)
        
    def set_colorkey(self, color=WHITE):

        self.image.set_colorkey(color)


class TroopImage(Image):

    def __init__(self, imagename, color, x_off, y_off):

        Image.__init__(self, imagename=imagename, colorkey=WHITE)
        self.recolor(DK_GREY, color)
        self.x_offset = x_off
        self.y_offset = y_off
        self.facing = 'left'

        self.x_ani_mod = 0
        self.y_ani_mod = 0

    def set_asset_path(self):

        return SPRITEPATH

    def get_pixel_coords(self, (x, y)):

         return (x * BATTLEGRID_SQUARE_W + self.x_offset + BATTLEFIELD_X_MARGIN + self.x_ani_mod,
         y * BATTLEGRID_SQUARE_H + self.y_offset + BATTLEFIELD_Y_MARGIN + self.y_ani_mod
         + (BATTLEGRID_SQUARE_H * .75))

    def position(self, (x, y)):

        self.rect.bottomleft = self.get_pixel_coords((x, y))

    def change_facing(self, new_facing):

        if self.facing != new_facing:
            self.facing = new_facing
            self.flip()

    def flip(self):

        self.image = pygame.transform.flip(self.image, True, False)
        # self.x_offset *= -1

    def set_ani_mod(self, (x, y)):

        self.x_ani_mod = x
        self.y_ani_mod = y
