from ..constants import MAPPATH
import os


REL = '\\..'


def get_line_values(line):
    line = line.rstrip('\n')
    cells = line.split(' ')
    values = []
    for str_value in cells:
        int_value = int(str_value)
        values.append(int_value)
    return values

    
def read_map_file(filename):
    path = os.path.dirname(__file__) + REL + MAPPATH + filename
    f = open(path, 'r')
    lines = f.readlines()
    f.close()

    w = len(get_line_values(lines[0]))
    h = len(lines)

    map = [[0 for my in range(h)] for mx in range(w)]

    y = 0
    x = 0
    for line in lines:
        x = 0
        line_values = get_line_values(line)
        for value in line_values:
            map[x][y] = value
            x += 1
        y += 1
        
    return map, w, h
