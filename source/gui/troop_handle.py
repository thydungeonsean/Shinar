from element import Element


class TroopHandle(Element):

    def __init__(self, troop):
        w = troop.image.w
        h = troop.image.h
        kwargs = {'visible': True}
        Element.__init__(self, (0, 0), w, h, 4, **kwargs)
        self.coord.set_owner(self)
        self.coord.toggle_auto_position_owner()
        troop.image.image_coord.bind(self.coord)
        print self.coord.get
        self.troop = troop
        self.image.set_alpha(200)

    def perform_function(self, dummy):
        print 'clicked ' + self.troop.tag

    def toggle_redraw(self):
        pass

    def set_color(self):
        return 255, 0, 0
