from element import Element


class TroopHandle(Element):

    def __init__(self, troop):
        w = troop.image.w
        h = troop.image.h
        kwargs = {'visible': False}
        Element.__init__(self, (0, 0), w, h, 4, **kwargs)
        troop.image.image_coord.bind(self.coord)
        self.troop = troop
