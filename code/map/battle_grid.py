from ..constants import *
import pygame


class BattleGrid(object):

    w = BATTLEGRID_W
    h = BATTLEGRID_H

    square_w = BATTLEGRID_SQUARE_W
    square_h = BATTLEGRID_SQUARE_H

    topleft = (BATTLEFIELD_X_MARGIN, BATTLEFIELD_Y_MARGIN)

    rect = pygame.Rect(topleft, (w*square_w, h*square_h))

    @staticmethod
    def draw(surface):
        bg = BattleGrid
        # pygame.draw.rect(surface, WHITE, bg.rect, SCALE) - full outline

        rect = pygame.Rect((0, 0), (bg.square_w, bg.square_h))

        for y in range(bg.h):
            for x in range(bg.w):
                tl = BattleGrid.get_pixel_coord((x, y))
                rect.topleft = tl
                pygame.draw.rect(surface, YELLOW, rect, SCALE)

    @staticmethod
    def get_pixel_coord((x, y)):
        bg = BattleGrid
        return x * bg.square_w + BATTLEFIELD_X_MARGIN, y*bg.square_h+BATTLEFIELD_Y_MARGIN
