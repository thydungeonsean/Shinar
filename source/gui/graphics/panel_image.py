import pygame
from ...constants import scale, scale_tuple, PANEL_BROWN, PANEL_DK_BROWN
from ...images.image import GUIImage


class PanelImage(object):

    min = scale(4)

    element_w = scale(2)
    element_dim = (element_w, element_w)
    element_pos = {
        'tl': scale_tuple((0, 0)),
        'tr': scale_tuple((4, 0)),
        'bl': scale_tuple((0, 4)),
        'br': scale_tuple((4, 4)),
        't': scale_tuple((2, 0)),
        'b': scale_tuple((2, 4)),
        'l': scale_tuple((0, 2)),
        'r': scale_tuple((4, 2))
    }

    style_mod = {
        1: (0, 0),
        2: scale_tuple((0, 6))
    }

    style_fill = {
        1: PANEL_BROWN,
        2: PANEL_DK_BROWN
    }

    def __init__(self, w, h, style=1):
        if w < PanelImage.min:
            w = PanelImage.min
        if h < PanelImage.min:
            h = PanelImage.min
        self.style = style
        self.image = self.set_image(w, h)

    def draw(self, surface):
        surface.blit(self.image, self.image.get_rect())

    def set_image(self, w, h):

        panel_tile = GUIImage('panel')

        image = pygame.Surface((w, h)).convert()
        image.fill(PanelImage.style_fill[self.style])

        # draw_edges
        if w - PanelImage.min != 0:
            self.draw_horizontal_edges(image, panel_tile, w, h)
        if h - PanelImage.min != 0:
            self.draw_vertical_edges(image, panel_tile, w, h)

        # set corners

        i = self.get_element(panel_tile, 'tl')
        r = i.get_rect()
        image.blit(i, r)

        i = self.get_element(panel_tile, 'tr')
        r = i.get_rect()
        r.topright = (w, 0)
        image.blit(i, r)

        i = self.get_element(panel_tile, 'bl')
        r = i.get_rect()
        r.bottomleft = (0, h)
        image.blit(i, r)

        i = self.get_element(panel_tile, 'br')
        r = i.get_rect()
        r.bottomright = (w, h)
        image.blit(i, r)

        return image

    def get_element(self, panel, key):
        sx, sy = PanelImage.style_mod[self.style]
        i = pygame.Surface(PanelImage.element_dim).convert()
        x, y = PanelImage.element_pos[key]
        i.blit(panel.image, (0, 0), (x+sx, y+sy, PanelImage.element_w, PanelImage.element_w))

        return i

    def draw_horizontal_edges(self, image, panel_tile, w, h):

        diff = w - PanelImage.min
        mod = PanelImage.element_w
        top_i = self.get_element(panel_tile, 't')
        bot_i = self.get_element(panel_tile, 'b')
        r = top_i.get_rect()

        if diff % PanelImage.element_w != 0:
            r.topleft = (PanelImage.element_w, 0)
            image.blit(top_i, r)
            r.bottomleft = (PanelImage.element_w, h)
            image.blit(bot_i, r)
            mod += diff % PanelImage.element_w

        for x in range(mod, diff+1, PanelImage.element_w):
            r.topleft = (x, 0)
            image.blit(top_i, r)
            r.bottomleft = (x, h)
            image.blit(bot_i, r)

    def draw_vertical_edges(self, image, panel_tile, w, h):

        diff = h - PanelImage.min
        mod = PanelImage.element_w
        left_i = self.get_element(panel_tile, 'l')
        right_i = self.get_element(panel_tile, 'r')
        r = left_i.get_rect()

        if diff % PanelImage.element_w != 0:
            r.topleft = (0, PanelImage.element_w)
            image.blit(left_i, r)
            r.topright = (w, PanelImage.element_w)
            image.blit(right_i, r)
            mod += diff % PanelImage.element_w

        for y in range(mod, diff+1, PanelImage.element_w):
            r.topleft = (0, y)
            image.blit(left_i, r)
            r.topright = (w, y)
            image.blit(right_i, r)

