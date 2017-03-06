import pygame.font as pg_font
import pygame.transform
from os import path
from ..constants import *


class MenuFont(object):

    instance = None

    PATH = path.dirname(__file__) + '\\..' + FONTPATH

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):

        self.font = pg_font.Font(MenuFont.PATH + 'oryxtype.ttf', 16)

    def draw(self, surface, pos, text, color=BLACK):

        font_image = self.font.render(text, False, color)

        font_image = self.scale_image(font_image)
        font_rect = font_image.get_rect()
        font_rect.topleft = pos

        surface.blit(font_image, font_rect)

    @staticmethod
    def scale_image(image):

        w = image.get_width()
        h = image.get_height()

        new = pygame.transform.scale(image, scale_tuple((w, h)))

        return new
