from ..constants import *
import pygame
import os
from ..images.image import Image


class MapImageGenerator(object):
    
    instance = None
    
    @classmethod
    def get_instance(cls):
        if cls.instance is not None:
            return cls.instance
        else:
            cls.instance = cls()
            return cls.instance
            
    """
    The image generator will scan through a map,
    and compile dither tile / wall tile combos
    as needed. It will store them in dither_patterns
    or wall patterns to be reused. 
    dither_sets will hold recolored images based on the
    patterns as needed.
    """
            
    def __init__(self):
        
        self.tile_images = self.init_tile_images()
        
        self.dither_gen = DitherImageGenerator()
        
        self.dither_patterns = {}
        # self.wall_patterns = {}
        
        self.dither_sets = {
            1: {},
            2: {},
            3: {}
        }
        
    # init methods
    def init_tile_images(self):
        
        tile_images = {
                0: TileImage('desert'),
                1: TileImage('plain'),
                2: TileImage('fertile'),
                3: TileImage('river')
        }
        
        return tile_images
        
    def generate_image(self, map):
        
        mw = map.w * TILEW
        mh = map.h * TILEH
        map_image = pygame.Surface((mw, mh))

        for y in range(map.h):
            for x in range(map.w):
                tile_id = map.map[x][y]
                if tile_id not in self.tile_images.keys():
                    tile_id = 0
                img = self.tile_images[tile_id]
                img.position((x, y))
                img.draw(map_image)
                
        dithered_edge_maps = self.get_dithered_edges(map)
        for k in (1, 2, 3):
            edge_map = dithered_edge_maps[k]
            for x, y in edge_map.keys():
                img = self.get_dither_image(k, edge_map[(x, y)])
                img.position((x, y))
                img.draw(map_image)
                
        return map_image
        
    def get_dithered_edges(self, map):
        
        dithered_ids = (1, 2, 3)
        dither_points = {
                1: [],
                2: [],
                3: []
        }
        
        for y in range(map.h):
            for x in range(map.w):
                value = map.map[x][y]
                if value in dithered_ids:
                    dither_points[value].append((x, y))
                    
        plain_dithered_edge = self.get_dithered_edge(map, dither_points[1], 0)
        fertile_dithered_edge = self.get_dithered_edge(map, dither_points[2], 1)
        river_dithered_edge = self.get_dithered_edge(map, dither_points[3], 2)
        #river_dithered_edge = self.get_dithered_edge(map, dither_points[2], 3)
        
        return {1: plain_dithered_edge,
                2: fertile_dithered_edge,
                3: river_dithered_edge} 
        
    def get_dithered_edge(self, map, points, cover_terrain):
        
        dither = {}
        visited = set()
        
        for x, y in points:
            adj = map.get_adj((x, y), diag=True)
            for ax, ay in adj:
                if map.map[ax][ay] == cover_terrain and (ax, ay) not in visited:
                    visited.add((ax, ay))
                    dither[(ax, ay)] = self.get_dither_value(map, map.map[x][y], (ax, ay))
                    
        return dither
                    
    def get_dither_value(self, map, cover_type, (x, y)):
        edge_coords = ((x-1, y-1), (x, y-1), (x+1, y-1), (x+1, y), 
                       (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y))
        i = 0
        value = set()
        for ex, ey in edge_coords:
            if map.is_on_map((ex, ey)) and map.map[ex][ey] == cover_type:
                value.add(i)
            i += 1
        
        value = list(value)
        value.sort()
        return tuple(value)
        
    def get_dither_image(self, terrain, dither_value):
        
        dither_set = self.dither_sets[terrain]
        if dither_value in dither_set.keys():
            return dither_set[dither_value]
        if dither_value in self.dither_patterns.keys():
            img = self.dither_gen.recolor_pattern(self.dither_patterns[dither_value], terrain)
            dither_set[dither_value] = img
            return img
        else:
            pattern = self.dither_gen.generate_pattern(dither_value)
            self.dither_patterns[dither_value] = pattern
            img = self.dither_gen.recolor_pattern(pattern, terrain)
            dither_set[dither_value] = img
            return img

        
class DitherImageGenerator(object):
    
    color_key = {
                 1: PLAIN_BROWN,
                 2: FERTILE_GREEN,
                 3: RIVER_BLUE
                 #3: PLAIN_BROWN
                # 1: RED, 2: RED, 3: RED
                }
    
    dither_key = {
            'a': (0, 0),
            'b': (TILEW, 0),
            'c': (TILEW*2, 0),
            'd': (0, TILEH),
            'e': (TILEW, TILEH),
            'f': (TILEW*2, TILEH),
            'g': (0, TILEH*2),
            'h': (TILEW, TILEH*2)
            }
    
    def __init__(self):
        self.dither_tileset = Image('dither', colorkey=WHITE)
    
    def generate_pattern(self, d_value):
        
        d_img = Image(colorkey=WHITE)
        image_instructions = self.parse_dither_value(d_value)

        for d_id, pos in image_instructions:        
            self.add_dither_segment(d_img, d_id, pos)
    
        return d_img
    
    def recolor_pattern(self, pattern, terrain):
        img = Image(colorkey=WHITE)
        pattern.draw(img)
        color = DitherImageGenerator.color_key[terrain]
        img.recolor(BLACK, color)
        return img
    
    def parse_dither_value(self, value):
        
        parsed = set()
        
        card = set([1, 3, 5, 7])
        diag = set([0, 2, 4, 6])
        
        cardinals = []
        for e in value: 
            if e in card:
                cardinals.append(e)
        if len(cardinals) < 3:
            for e in value:  # checking for outer diagonal corners
                if e in diag and self.corner_is_isolate(value, e):
                    parsed.add(('b', e))
        elif len(cardinals) == 4:
            parsed = [('d', 1), ('d', 3), ('d', 5), ('d', 7),
                      ('c', 0), ('c', 2), ('c', 4), ('c', 6)]
            return parsed
                    
        for e in cardinals:  # check for solid edges
            if self.edge_is_isolate(value, e):
                parsed.add(('a', e))
            else:
                parsed.add(('d', e))
                if self.edge_has_one_adj(value, e, 2):
                    end, connector = self.get_corner_values(value, e)
                    parsed.add(('e', end))
                    parsed.add(('c', connector))
                else:
                    adj = self.get_adj_edges(e, 1)
                    for ae in adj:
                        parsed.add(('c', ae))
           
        return list(parsed)
                    
    def get_adj_edges(self, e, step):
        raw_adj = (e + step, e - step)
        adj = []
        for ae in raw_adj:
            if ae < 0:
                adj.append(ae + 8)
            elif ae > 7:
                adj.append(ae - 8)
            else:
                adj.append(ae)
                
        return adj
                
    def get_corner_values(self, value, e):
        corners = self.get_adj_edges(e, 1)
        end = None
        connector = None
        for corner in corners:
            if self.edge_has_one_adj(value, corner, 1):
                end = corner
            else:
                connector = corner
        return end, connector
                
    def corner_is_isolate(self, value, e):
        
        adj = self.get_adj_edges(e, 1)
        for ae in adj:
            if ae in value:
                return False
        return True
        
    def edge_is_isolate(self, value, e):
        
        adj = self.get_adj_edges(e, 2)
        for ae in adj:
            if ae in value:
                return False
        return True
    
    def edge_has_one_adj(self, value, e, step):
        adj = self.get_adj_edges(e, step)
        num = 0
        for ae in adj:
            if ae in value:
                num += 1
        if num < 2:
            return True
        else:
            return False
    
    def add_dither_segment(self, d_img, d_id, pos):
        
        if d_id in ('a', 'b', 'c', 'd'):
            self.add_rotated_img(d_img, d_id, pos)
        else:  # d_id is 'e'
            if pos == 0:
                self.add_rotated_img(d_img, 'e', 0)
            elif pos == 2:
                self.add_rotated_img(d_img, 'f', 0)
            elif pos == 4:
                self.add_rotated_img(d_img, 'g', 0)
            elif pos == 6:
                self.add_rotated_img(d_img, 'h', 0)
        
    def add_rotated_img(self, d_img, d_id, pos):
        
        ang_dict = {0: 0, 1: 0, 2: -90, 3: -90, 4: 180, 5: 180, 6: 90, 7: 90}
    
        img = pygame.Surface((TILEW, TILEH))
        img.fill(WHITE)
        img.set_colorkey(WHITE)
        x, y = DitherImageGenerator.dither_key[d_id] 
        img.blit(self.dither_tileset.image, (0,0), (x, y, TILEW, TILEH))
        img = pygame.transform.rotate(img, ang_dict[pos])
        d_img.blit(img, img.get_rect())
        

class TileImage(Image):
    
    def __init__(self, imagename=None):
        Image.__init__(self, imagename)
        
    
    