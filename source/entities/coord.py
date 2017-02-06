

class Coord(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.bound = None
        
    @property
    def get(self):
        return self.x, self.y
        
    def set(self, (x, y)):
        self.x = x
        self.y = y
        if self.bound is not None:
            self.bound.set((x, y))

    def bind(self, coord):
        self.bound = coord
        self.bound.set(self.get)

    def unbind(self):
        self.bound = None
