from ..constants import *
from ..images.image import TroopImage


class Troop(object):
    
    def __init__(self, location, team, color, type, cohesion, morale, speed, strength, weakness):
        
        self.location = location
        self.coord = (0, 0)

        self.direction = 1

        self.team = team
        self.color = color
        
        self.type = type
        
        self.cohesion = cohesion
        self.morale = morale
        self.speed = speed
        self.strength = strength
        self.weakness = weakness

        self.state = 'advance'
        
        self.x_offset, self.y_offset = self.set_image_offsets()
        self.image = self.set_image()

    def set_image(self):
        return TroopImage(self.type, self.color, self.x_offset, self.y_offset)
        
    def set_image_offsets(self):
        return 0, 0
        
    def draw(self, surface):
        self.image.draw(surface)

    def position_image(self, (x, y)):
        self.image.position((x, y))

    def change_facing(self):
        self.image.change_facing()

    def get_pixel_coord(self, (x, y)):
        return x * BATTLEGRID_SQUARE_W + BATTLEFIELD_X_MARGIN, y * BATTLEGRID_SQUARE_H

    def move(self, coord):
        self.coord = coord


class Infantry(Troop):
    
    def __init__(self, location, team, color):
        
        type = 'infantry'
        
        cohesion = 10
        morale = 10
        speed = 2
        strength = 'chariot'
        weakness = 'archer'
        
        Troop.__init__(self, location, team, color, type, cohesion, morale, speed, strength, weakness)

    def set_image_offsets(self):
        return scale_tuple((-1, 0))
        
        
class Archer(Troop):
    
    def __init__(self, location, team, color):
        
        type = 'archer'
        
        cohesion = 5
        morale = 7
        speed = 3
        strength = 'infantry'
        weakness = 'chariot'
        
        Troop.__init__(self, location, team, color, type, cohesion, morale, speed, strength, weakness)
        
        
class Chariot(Troop):
    
    def __init__(self, location, team, color):
        
        type = 'chariot'
        
        cohesion = 7
        morale = 4
        speed = 5
        strength = 'archer'
        weakness = 'infantry'
        
        Troop.__init__(self, location, team, color, type, cohesion, morale, speed, strength, weakness)

    def set_image_offsets(self):
        return scale_tuple((-2, 0))
