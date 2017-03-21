import font
import pygame
from ..constants import *


class TextBox(object):

    MIN_H = scale(30)

    def __init__(self, w, text):

        self.w = w

        self.line_dimensions = []
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

    def move(self, (x, y)):
        self.rect.topleft = (x, y)

    def render_text(self, surface):

        f = font.MenuFont.get_instance()

        for i in range(len(self.text)):
            pos = self.text_positions[i]
            text = self.text[i]

            f.draw(surface, pos, text, color=WHITE)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def wrap_text(self, text):

        text, breaks = self.format_text(text)

        f = font.MenuFont.get_instance()

        text_lines = ['']

        i = 0
        ln_start = 0
        ln_end = 0
        while i < len(text):

            if i in breaks:

                if len(text[ln_start:i]) == 0:
                    text_lines.append('')
                else:
                    line = text[ln_start:i+1]
                    text_lines.append(line)
                    self.line_dimensions.append(f.size(line))

                    ln_start = i+2
                    ln_end = i+2
                    i += 2

            elif text[i] == ' ':
                end_line = self.test_line_length(text[ln_start:i+1])
                if end_line:

                    line = text[ln_start:ln_end+1]
                    text_lines.append(line)
                    self.line_dimensions.append(f.size(line))

                    ln_start = ln_end + 2
                    ln_end = i

                else:
                    ln_end = i-1

            i += 1

        if len(text_lines) == 0:
            text_lines = [text]
            self.line_dimensions.append(f.size(text))
        elif len(text[ln_start:]) > 0:
            text_lines.append(text[ln_start:])
            self.line_dimensions.append(f.size(text[ln_start:]))

        text_lines.append('')

        return text_lines

    def format_text(self, text):
        i = 0
        breaks = []
        if text[-1] == '\n':
            breaks.append(-1)
            text = text[:-2]
        while i < len(text):
            if text[i] == '\n':
                breaks.append(i)
                text = text[0:i] + text[i+1:]
            i += 1
        return text, breaks

    def test_line_length(self, line):
        f = font.MenuFont.get_instance()

        w, h = f.size(line)
        if w >= self.w:
            return True
        return False

    def set_text_positions(self):
        positions = {}

        width_offset = self.get_width_offset()

        for i in range(len(self.text)):
            positions[i] = (width_offset, i * scale(10) - scale(4))
        return positions

    def get_width_offset(self):
        largest = 0
        for w, h in self.line_dimensions:
            if w > largest:
                largest = w
        return (self.w - largest) / 2

    def determine_height(self):
        end = len(self.text) - 1
        last_y = self.text_positions[end][1]

        h = last_y + scale(14)
        if h < TextBox.MIN_H:
            h = TextBox.MIN_H
        return h

