
SCALE = 2


def scale(value):
    return int(value*SCALE)

    
def descale(value):
    return int(float(value) / SCALE)
    
    
def scale_tuple((x, y)):
    return scale(x), scale(y)
    
    
MAPPATH = '\\..\\assets\\maps\\'
TILEPATH = '\\..\\assets\\tiles\\'
SPRITEPATH = '\\..\\assets\\sprites\\'


SCREENW = 400 * SCALE
SCREENH = 300 * SCALE

TILEW = 16 * SCALE
TILEH = 16 * SCALE

BATTLEFIELD_MARGIN = 75

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

DK_GREY = (66, 66, 66)

RED = (255, 0, 0)

PLAIN_BROWN = (201, 111, 10)
FERTILE_GREEN = (117, 134, 23)
RIVER_BLUE = (84, 222, 191)
