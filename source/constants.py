
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
GUIPATH = '\\..\\assets\\gui\\'
FONTPATH = '\\..\\assets\\font\\'
TEXTPATH = '\\..\\assets\\data\\text\\'


SCREENW = scale(400)
SCREENH = scale(300)

TILEW = 16 * SCALE
TILEH = 16 * SCALE

# Battle Mode
BFW = 6
BATTLEFIELD_FRAME_W = scale(BFW)

BATTLEFIELD_COORD = scale_tuple((BFW, BFW))
BATTLEFIELD_W = 20 * TILEW
BATTLEFIELD_H = 18 * TILEH

BATTLEGRID_W = 9
BATTLEGRID_H = 10

BATTLEGRID_SQUARE_W = scale(32)
BATTLEGRID_SQUARE_H = scale(26)

BATTLEFIELD_X_MARGIN = (BATTLEFIELD_W - BATTLEGRID_W * BATTLEGRID_SQUARE_W)/2
BATTLEFIELD_Y_MARGIN = ((BATTLEFIELD_H - BATTLEGRID_H * BATTLEGRID_SQUARE_H)/2)

COMMAND_PANEL_W = SCREENW - (2 * BATTLEFIELD_FRAME_W + BATTLEFIELD_W)

COMMAND_PANEL_Y = scale(50)

MAIN_MENU_BUTTON_X = scale(5)
MAIN_MENU_BUTTON_Y = scale(5)
RIGHT_PANEL_X = 2 * BATTLEFIELD_FRAME_W + BATTLEFIELD_W
NEXT_TURN_BUTTON_X = scale(5) + RIGHT_PANEL_X
NEXT_TURN_BUTTON_Y = scale(30)

FRAMES_PER_TURN = 120

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

LT_GREY = (100, 100, 100)
DK_GREY = (66, 66, 66)

RED = (255, 0, 0)
YELLOW = (255, 240, 0)
BLUE = (0, 0, 255)

PLAIN_BROWN = (201, 111, 10)
FERTILE_GREEN = (117, 134, 23)
RIVER_BLUE = (84, 222, 191)
