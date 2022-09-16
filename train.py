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

        # Sprite
        self.original_image = pg.image.load("assets/trains/ice_loc.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()

        self.length = self.original_image.get_width()

        self.trajectory = list()
        self.nose_position_pointer = 31

        self.moving = False
        self.direction = None

        # state can be "waiting for spawn", "spawned", "despawned"
        self.state = "waiting for spawn"

    def update(self):
        if self.state == "spawned":
            self.nose_position_pointer += self.trajectory_pointer_increment
            if self.nose_position_pointer >= len(self.trajectory) or self.tail_position_pointer < 0:
                # No trajectory defined, we do not move.
                self.nose_position_pointer -= self.trajectory_pointer_increment
            else:
                # Axles move forward or backwards in trajectory list
                axle_1_pos = self.trajectory[self.axle_1_position_pointer]
                axle_2_pos = self.trajectory[self.axle_2_position_pointer]

                # Draw sprite based on axle position
                diff_vector = axle_1_pos - axle_2_pos
                angle = math.atan(diff_vector.y/diff_vector.x)/math.pi*180
                self.image = pg.transform.rotate(self.original_image, -angle)
                self.rect = self.image.get_rect()
                self.rect.centerx = (axle_1_pos.x + axle_2_pos.x) / 2
                self.rect.centery = (axle_1_pos.y + axle_2_pos.y) / 2

    def draw(self, screen: pg.surface.Surface):
        if self.state == "spawned":
            pg.draw.rect(screen, pg.color.Color("red"), self.rect, width=1)
            screen.blit(self.image, self.rect)

    def start(self, direction):
        # Sets train in movement in desired direction.
        self.direction = direction
        self.moving = True

    def stop(self):
        # Stops train
        self.moving = False

    def spawn(self):
        # Spawns train
        self.state = "spawned"
        self.start(self.direction)

    def despawn(self):
        # Despawns train
        self.state = "despawned"
        self.stop()

    @property
    def tail_position_pointer(self):
        return self.nose_position_pointer - self.length

    @tail_position_pointer.setter
    def tail_position_pointer(self, p):
        self.nose_position_pointer = p + self.length

    @property
    def axle_1_position_pointer(self):
        return self.nose_position_pointer - 10

    @property
    def axle_2_position_pointer(self):
        return self.tail_position_pointer + 10

    @property
    def trajectory_pointer_increment(self):
        if self.moving:
            if self.direction == "forward":
                return +1
            elif self.direction == "backward":
                return -1
        else:
            return 0

