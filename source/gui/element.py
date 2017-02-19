from ..entities.coord import Coord
import pygame


class Element(object):

    def __init__(self, (x, y), w, h):
    
        self.coord = Coord((x, y))
        self.w = w
        self.h = h
        
        