import font
import pygame
from ..constants import *


class TextBox(object):

    MIN_H = scale(25)

    def __init__(self, w, text):

        self.w = w

        self.text = self.wrap_text(text)
        self.text_positions = self.set_text_positions()

        self.h = self.determine_height()

        self.image, self.rect = self.set_image()

    def set_image(self):
        image = pygame.Surface((self.w, self.h)).convert()
        rect = image.get_rect()

        image.fill(BLACK)

        self.render_text(image)

        return image, rect

    def render_text(self, surface):

        f = font.MenuFont.get_instance()

        for i in range(len(self.text)):
            pos = self.text_positions[i]
            text = self.text[i]

            f.draw(surface, pos, text, color=WHITE)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def wrap_text(self, text):

        f = font.MenuFont.get_instance()

        text_lines = []

        i = 0
        ln_start = 0
        ln_end = 0
        while i < len(text):

            if text[i] in (' ', '\n'):
                end_line = self.test_line_length(text[ln_start:i])
                if end_line:
                    text_lines.append(text[ln_start:ln_end])
                    ln_start = i+1
                    ln_end = i+1
                    i += 1
                else:
                    ln_end = i-1

            i += 1

        if len(text_lines) == 0:
            text_lines = [text]
        print text_lines
        return text_lines

    def test_line_length(self, line):

        f = font.MenuFont.get_instance()

        w = f.size(line)
        if w >= self.w:
            return True
        return False

    def set_text_positions(self):
        positions = {}
        for i in range(len(self.text)):
            positions[i] = (0, i * scale(10) - scale(4))
        return positions

    def determine_height(self):
        end = len(self.text) - 1
        last_y = self.text_positions[end][1]

        h = last_y + scale(10)
        if h < scale(TextBox.MIN_H):
            h = TextBox.MIN_H
        return h

