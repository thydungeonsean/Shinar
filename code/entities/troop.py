from ..constants import *
from ..images.image import Image


class Troop(object):
    
    def __init__(self, location, team, type, cohesion, morale, speed, strength, weakness):
        
        self.location = location
        self.coord = self.location.get_coord(self)
        
        self.team = team
        
        self.type = type
        
        self.cohesion = cohesion
        self.morale = morale
        self.speed = speed
        self.strength = strength
        self.weakness = weakness
        
        self.x_offset, self.y_offset = self.set_image_offsets()
        self.image = self.set_image()
        
    def set_image(self):
        return TroopImage(self.type, RED, self.x_offset, self.y_offset)
        
    def set_image_offsets(self):
        return 0, 0
        
    def draw(self, surface):
        self.image.draw(surface)

    def position(self, (x, y)):
        self.image.position((x, y))
        

class Infantry(Troop):
    
    def __init__(self, location, team):
        
        type = 'infantry'
        
        cohesion = 10
        morale = 10
        speed = 2
        strength = 'chariot'
        weakness = 'archer'
        
        Troop.__init__(self, location, team, type, cohesion, morale, speed, strength, weakness)

    def set_image_offsets(self):
        return scale_tuple((-1, -4))
        
        
class Archer(Troop):
    
    def __init__(self, location, team):
        
        type = 'archer'
        
        cohesion = 5
        morale = 7
        speed = 3
        strength = 'infantry'
        weakness = 'chariot'
        
        Troop.__init__(self, location, team, type, cohesion, morale, speed, strength, weakness)
        
    def set_image_offsets(self):
        return scale_tuple((0, -4))
        
        
class Chariot(Troop):
    
    def __init__(self, location, team):
        
        type = 'chariot'
        
        cohesion = 7
        morale = 4
        speed = 5
        strength = 'archer'
        weakness = 'infantry'
        
        Troop.__init__(self, location, team, type, cohesion, morale, speed, strength, weakness)

    def set_image_offsets(self):
        return scale_tuple((-2, -8))

        
class TroopImage(Image):
    
    def __init__(self, imagename, color, x_off, y_off):
        
        Image.__init__(self, imagename=imagename, colorkey=WHITE)
        self.recolor(DK_GREY, color)
        self.x_offset = x_off
        self.y_offset = y_off
    
    def set_asset_path(self):
        return SPRITEPATH

    def position(self, (x, y)):
        self.rect.topleft = (x + self.x_offset, y + self.y_offset)