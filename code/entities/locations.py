

class Location(object):
    
    """ Location is a holder for troop entities - abstract class
    Rows that make up the battlefield are one location
    Stacks that make up the army are another.
    """
    
    def __init__(self):
        
        self.items = []
        
    def get_coord(self, item):
        return None
        
    def add(self, item):
        self.items.append(item)
