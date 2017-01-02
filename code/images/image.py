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
        scaled = pygame.transform.scale(base, (w*SCALE, h*SCALE))
        
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
        