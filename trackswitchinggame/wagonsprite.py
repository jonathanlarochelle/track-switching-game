# -*- coding: utf-8 -*-

# import built-in module
import math

# import third-party modules
import pygame as pg

# import your own module
from trackswitchinggame.constants import *


class WagonSprite(pg.sprite.Sprite):
    """
    Representation of a wagon.
    """

    def __init__(self, image, flip_wagon=False):
        super().__init__()

        self.original_image = pg.image.load(image).convert_alpha()
        self.length = self.original_image.get_width()
        if flip_wagon:
            self.original_image = pg.transform.flip(self.original_image, True, False)

        self.image = self.original_image
        self.rect = self.image.get_rect()

    def update(self, position_axle_1, position_axle_2):
        diff_vector = position_axle_1 - position_axle_2
        angle = math.atan(diff_vector.y / diff_vector.x) / math.pi * 180
        self.image = pg.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect()

        if DEBUG:
            pg.draw.rect(self.image, pg.Color("lightcoral"), self.rect, width=1)

        self.rect.centerx = (position_axle_1.x + position_axle_2.x) / 2
        self.rect.centery = (position_axle_1.y + position_axle_2.y) / 2
