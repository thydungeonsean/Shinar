import pygame
from ..constants import *
import os


REL = '\\..'


class Image(object):
    
    def __init__(self, imagename=None, colorkey=None):
    
        self.x_offset = 0
        self.y_offset = 0
    
        self.asset_path = self.set_asset_path()
        self.image = self.init_image(imagename)
        if colorkey is not None:
            self.set_colorkey(colorkey)
        self.rect = self.image.get_rect()
        
    def set_asset_path(self):
        return TILEPATH
        
    def init_image(self, imagename):
    
        if imagename is None:
            img = pygame.Surface((TILEW, TILEH))
            img.fill(WHITE)
            return img
        
        path = os.path.dirname(__file__) + REL + self.asset_path + imagename + '.png'
        
        base = pygame.image.load(path)
        w = base.get_width()
        h = base.get_height()
        scaled = pygame.transform.scale(base, (scale(w), scale(h)))
        
        return scaled
    
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

    def set_asset_path(self):
        return SPRITEPATH

    def position(self, (x, y)):
        self.rect.bottomleft = (x + self.x_offset, y + self.y_offset + (BATTLEGRID_SQUARE_H * .75))

    def change_facing(self):
        if self.facing == 'left':
            self.facing = 'right'
        elif self.facing == 'right':
            self.facing = 'left'
        self.flip()

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)
        # self.x_offset *= -1
