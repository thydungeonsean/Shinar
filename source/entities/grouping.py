

class Grouping(object):
    
    """ Grouping is a holder for troop entities - abstract class
    Rows that make up the battlefield are one location
    Stacks that make up the army are another.
    """
    
    def __init__(self):
        
        self.troops = []
        
    def add(self, troop):
        self.troops.append(troop)

    def remove(self, troop):
        try:
            self.troops.remove(troop)
        except IndexError:
            print troop + 'was not in ' + self + 'when attempting to remove'

    def get_next(self):
        return self.troops[0]

    def len(self):
        return len(self.troops)
