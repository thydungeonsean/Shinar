from ...images.image import GUIImage
import pygame
from ...constants import scale, scale_tuple


class MainBorder(object):

    c_w = scale(6)

    ver_w = scale(6)
    ver_h = scale(4)

    hor_w = scale(4)
    hor_h = scale(6)

    dim_dict = {
        'corner': 'corner',
        'top': 'hor',
        'top_left': 'hor',
        'top_right': 'hor',
        'bot': 'hor',
        'bot_left': 'hor',
        'bot_right': 'hor',
        'left': 'ver',
        'left_top': 'ver',
        'left_bot': 'ver',
        'right': 'ver',
        'right_top': 'ver',
        'right_bot': 'ver'
    }

    dimensions = {
        'ver': (ver_w, ver_h),
        'hor': (hor_w, hor_h),
        'corner': (c_w, c_w)
    }

    element_pos = {
        'left_top': scale_tuple((0, 0)),
        'left': scale_tuple((0, 4)),
        'left_bot': scale_tuple((0, 8)),
        'right_top': scale_tuple((6, 0)),
        'right': scale_tuple((6, 4)),
        'right_bot': scale_tuple((6, 8)),
        'top_left': scale_tuple((12, 0)),
        'top': scale_tuple((16, 0)),
        'top_right': scale_tuple((20, 0)),
        'bot_left': scale_tuple((12, 6)),
        'bot': scale_tuple((16, 6)),
        'bot_right': scale_tuple((20, 6)),
        'corner': scale_tuple((24, 0))
    }

    def __init__(self, w, h, side):

        if side in ('top', 'bot'):
            w = self.round_off_side(w)
        else:
            h = self.round_off_side(h)
        self.image = self.set_image(w, h, side)

    def round_off_side(self, s):
        MB = MainBorder
        remainder = (s - MB.c_w*2) % MB.hor_w
        return s - remainder

    def draw(self, surface):
        surface.blit(self.image, self.image.get_rect())

    def set_image(self, w, h, side):

        base_sheet = GUIImage('border')

        image = pygame.Surface((w, h)).convert()

        if side in ('top', 'bot'):
            self.draw_corners(image, base_sheet, w)
            self.draw_horizontal(image, side, base_sheet, w, h)
        else:
            self.draw_vertical(image, side, base_sheet, w, h)

        return image

    def draw_corners(self, image, base_sheet, w):
        # corners
        el = self.get_element(base_sheet, 'corner')
        r = el.get_rect()
        image.blit(el, r)
        r.topright = (w, 0)
        image.blit(el, r)

    def get_element(self, sheet, key):

        MB = MainBorder

        i = pygame.Surface(MB.dimensions[MB.dim_dict[key]]).convert()
        x, y = MainBorder.element_pos[key]
        w, h = MB.dimensions[MB.dim_dict[key]]
        i.blit(sheet.image, (0, 0), (x, y, w, h))

        return i

    def draw_horizontal(self, image, side, base_sheet, w, h):

        MB = MainBorder
        start_w = MB.c_w + MB.hor_w
        end_w = w - MB.c_w - MB.hor_w
        border = self.get_element(base_sheet, side)
        r = border.get_rect()
        for x in range(start_w, end_w, MB.hor_w):
            r.topleft = (x, 0)
            image.blit(border, r)

        left = self.get_element(base_sheet, ''.join((side, '_left')))
        r.topleft = (MB.c_w, 0)
        image.blit(left, r)

        right = self.get_element(base_sheet, ''.join((side, '_right')))
        r.topleft = (end_w, 0)
        image.blit(right, r)

    def draw_vertical(self, image, side, base_sheet, w, h):

        MB = MainBorder
        start_h = MB.ver_h
        end_h = h - MB.ver_h

        border = self.get_element(base_sheet, side)
        r = border.get_rect()
        for y in range(start_h, end_h, MB.ver_h):
            r.topleft = (0, y)
            image.blit(border, r)

        top = self.get_element(base_sheet, ''.join((side, '_top')))
        r.topleft = (0, 0)
        image.blit(top, r)

        bot = self.get_element(base_sheet, ''.join((side, '_bot')))
        r.topleft = (0, end_h)
        image.blit(bot, r)

