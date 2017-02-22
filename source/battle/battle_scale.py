from ..constants import *
import pygame
from ..states.observer import Observer


class BattleScale(object):

    instance = None

    point_ref = {
        'flee': -5,
        'recover': 5,
        'hit': 1,
        'rout': -5,
        'pursue': 10
    }

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = BattleScale()
        return cls.instance

    def __init__(self):

        self.battle = None
        self.points = {'left': 0, 'right': 0}

        self.renderer = BattleScaleRenderer(self)
        self.subscribe_to_observer()

        self.scale_needs_update = True

    def init_battle(self, battle):
        self.battle = battle
        self.set_initial_points()
        self.renderer.init_battle(battle)
        self.scale_needs_update = True

    def deinit_battle(self):
        self.battle = None
        self.points['left'] = 0
        self.points['right'] = 0
        self.renderer.deinit_battle()
        self.scale_needs_update = False

    def set_initial_points(self):
        self.points['left'] = self.battle.active_left_troops * 10
        self.points['right'] = self.battle.active_right_troops * 10

    def subscribe_to_observer(self):
        observer = Observer.get_instance()
        observer.add_subscriber(self)

    @property
    def total_points(self):
        return self.points['left'] + self.points['right']

    @property
    def left_balance_factor(self):
        try:
            return self.points['left'] / float(self.total_points)
        except ZeroDivisionError:
            return .5

    def modify_points(self, side, points):
        self.points[side] += points

    def run(self):
        if self.scale_needs_update:
            self.update_bar()
            self.scale_needs_update = False

    def update_bar(self):
        self.renderer.render_bar(self.left_balance_factor)

    def draw(self, surface):
        self.renderer.draw(surface)

    def receive_report(self, report):
        if report.report_type == 'unit':
            print report.args
            side = report.args[0]
            points = BattleScale.point_ref[report.args[1]]
            self.modify_points(side, points)
        self.scale_needs_update = True


class BattleScaleRenderer(object):

    WIDTH = BATTLEGRID_SQUARE_W * BATTLEGRID_W
    BAR_HEIGHT = scale(6)
    RECT_HEIGHT = scale(10)

    rect_x = BATTLEFIELD_X_MARGIN
    rect_y = 0

    bar_x = 0
    bar_y = (RECT_HEIGHT - BAR_HEIGHT) / 2

    def __init__(self, b_scale):
        self.battle_scale = b_scale

        cls = BattleScaleRenderer

        self.image = self.set_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (cls.rect_x, cls.rect_y)

        self.bar_image = self.set_bar_image()
        self.bar_rect = self.bar_image.get_rect()
        self.bar_rect.topleft = (cls.bar_x + SCALE, cls.bar_y +SCALE)

        self.left_color = None
        self.right_color = None

    @staticmethod
    def set_image():
        cls = BattleScaleRenderer
        image = pygame.Surface((cls.WIDTH, cls.RECT_HEIGHT))
        image.fill(WHITE)
        image.set_colorkey(WHITE)

        box = pygame.Rect((cls.bar_x, cls.bar_y), (cls.WIDTH, cls.BAR_HEIGHT))

        pygame.draw.rect(image, BLACK, box, 0)

        image = image.convert()
        return image

    @staticmethod
    def set_bar_image():
        cls = BattleScaleRenderer
        image = pygame.Surface((cls.WIDTH-scale(2), cls.BAR_HEIGHT-scale(2)))
        return image.convert()

    def init_battle(self, battle):
        self.left_color = battle.left_army.color
        self.right_color = battle.right_army.color

    def deinit_battle(self):
        self.left_color = None
        self.right_color = None

    def render_bar(self, balance):

        w = self.bar_rect.w
        h = self.bar_rect.h
        mid = int(balance * self.bar_rect.w)
        left_rect = pygame.Rect((0, 0), (mid, h))
        right_rect = pygame.Rect((mid+SCALE, 0), (w-mid, h))
        pygame.draw.rect(self.bar_image, self.left_color, left_rect)
        pygame.draw.rect(self.bar_image, self.right_color, right_rect)

    def draw(self, surface):
        self.image.blit(self.bar_image, self.bar_rect)
        surface.blit(self.image, self.rect)
