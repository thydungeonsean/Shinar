import pygame
from ..constants import *


class BoxBorder(object):

    THIN_W = scale(3)
    THIN_X = scale(2)

    @classmethod
    def frame_box(cls, box):
        box.move((cls.THIN_W, cls.THIN_W))
        w = box.w + BoxBorder.THIN_W * 2
        h = box.h + BoxBorder.THIN_W * 2
        border = cls(w, h)
        return border

    @classmethod
    def frame_dimensions(cls, w, h):
        bw = w + BoxBorder.THIN_W * 2
        bh = h + BoxBorder.THIN_W * 2
        border = cls(w, h)
        return border

    def __init__(self, w, h):

        self.w = w
        self.h = h

        self.image, self.rect = self.set_image()

    def set_image(self):

        image = pygame.Surface((self.w, self.h)).convert()
        image.fill(BLACK)

        self.draw_border(image)

        rect = image.get_rect()

        return image, rect

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def draw_border(self, image):

        bx = BoxBorder.THIN_X
        fx = BoxBorder.THIN_W

        border = pygame.Rect((bx, bx), (self.w-bx*2, self.h-bx*2))
        fill = pygame.Rect((fx, fx), (self.w-fx*2, self.h-fx*2))
        pygame.draw.rect(image, WHITE, border)
        pygame.draw.rect(image, BLACK, fill)
