from map_tools import read_map_file


class Map(object):
    
    @classmethod
    def load_map_file(cls, fname):
        map, w, h = read_map_file(fname)
        instance = cls(w, h)
        instance.map = map
        return instance
    
    def __init__(self, w, h):
    
        self.w = w
        self.h = h
        self.map = [[0 for my in range(self.h)] for mx in range(self.w)]
    
    def is_on_map(self, (x, y)):
        return 0 <= x < self.w and 0 <= y < self.h
    
    def get_adj(self, (x, y), diag=False):
        directions = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        if diag:
            diagonals = [(x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)]
            directions.extend(diagonals)
            
        adj = []
            
        for point in directions:
            if self.is_on_map(point):
                adj.append(point)
            
        return adj