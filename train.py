# -*- coding: utf-8 -*-

# import built-in module
import math

# import third-party modules
import pygame as pg
from pygame.math import Vector2

# import your own module
from map import Map


class Train(pg.sprite.Sprite):
    """
    [Class docstring]
    """

    def __init__(self, *groups: pg.sprite.AbstractGroup):
        super().__init__(*groups)
        self.original_image = pg.image.load("assets/trains/ice_loc.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()

        self.speed = 0
        self.trajectory = list()
        self.nose_position_pointer = 30

    def update(self):
        self.nose_position_pointer += self.speed
        if self.nose_position_pointer >= len(self.trajectory) or self.tail_position_pointer < 0:
            # No trajectory defined, we do not move.
            self.nose_position_pointer -= self.speed
        else:
            # Axles move forward or backwards in trajectory list
            axle_1_pos = self.trajectory[self.axle_1_position_pointer]
            axle_2_pos = self.trajectory[self.axle_2_position_pointer]

            # Draw sprite based on axle position
            self.rect.centerx = (axle_1_pos.x + axle_2_pos.x) / 2
            self.rect.centery = (axle_1_pos.y + axle_2_pos.y) / 2
            diff_vector = axle_1_pos - axle_2_pos
            angle = math.atan(diff_vector.y/diff_vector.x)/math.pi*180
            self.image = pg.transform.rotate(self.original_image, -angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen: pg.surface.Surface):
        screen.blit(self.image, self.rect)

    @property
    def tail_position_pointer(self):
        return self.nose_position_pointer - 29

    @property
    def axle_1_position_pointer(self):
        return self.nose_position_pointer - 10

    @property
    def axle_2_position_pointer(self):
        return self.tail_position_pointer + 10
