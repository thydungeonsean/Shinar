import os
from ..constants import TEXTPATH


REL = '\\..'

path = os.path.dirname(__file__) + REL + TEXTPATH


def get_ui_text(key):

    f = open(path + 'ui_text.txt', 'r')
    text = None
    for line in f:
        tag, ln_end = parse_tag(line)
        if tag == key:
            text = parse_text(line, ln_end)
            break

    f.close()

    if text is None:
        raise Exception("Bad key for ui_text file")

    return text


def parse_tag(line):

    if line[0] == '[':

        for i in range(1, len(line)):
            if line[i] == ':':
                return line[1:i].strip(), i
    elif line[0] == '#':
        return False, 0
    elif line == '\n':
        return False, 0

    raise Exception("data file formatted incorrectly - no :")


def parse_text(line, start):

    return line [start+1:-2]
