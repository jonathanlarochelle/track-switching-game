# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pygame as pg
from pygame.math import Vector2

# import your own module
from wagonsprite import WagonSprite


class Train:
    """
    Represents a self-contained train, which is composed of wagons.
    The train's movement follow points stored in trajectory.
    """

    def __init__(self):
        # Set-up wagons
        self.wagons = []
        self.wagons.append(WagonSprite("assets/trains/ice_loc.png"))
        self.wagons.append(WagonSprite("assets/trains/ice_wagon.png"))
        self.wagons.append(WagonSprite("assets/trains/ice_loc.png", True))

        self.goals = []
        self.trajectory = list()
        self.rightmost_position_pointer = None  # Initialized when calling spawn()

        self.moving = False
        self.direction = None

        # state can be "waiting for spawn", "spawned", "despawned"
        self.state = "waiting for spawn"

    def update(self):
        """
        Update position of the train
        """
        if self.state == "spawned":
            # Update position
            self.rightmost_position_pointer += self.trajectory_pointer_increment
            if self.rightmost_position_pointer >= len(self.trajectory) or self.leftmost_position_pointer < 0:
                # No trajectory defined, we do not move.
                self.rightmost_position_pointer -= self.trajectory_pointer_increment
            else:
                current_offset = self.rightmost_position_pointer

                for wagon in self.wagons:
                    # Should the position of the axles be handled individually by each wagon?
                    # Do we want wagons to have a variable axle offset??
                    axle_1_pointer = current_offset - 5
                    axle_2_pointer = current_offset - 25
                    position_axle_1 = self.trajectory[axle_1_pointer]
                    position_axle_2 = self.trajectory[axle_2_pointer]
                    wagon.update(position_axle_1, position_axle_2)
                    current_offset -= wagon.length

            # Check for goals
            self._update_goals()

    def draw(self, screen: pg.surface.Surface):
        """
        Draw the train.
        """
        if self.state == "spawned":
            for wagon in self.wagons:
                wagon.draw(screen)

    def start(self, direction):
        """
        Sets train in movement in desired direction.
        """
        self.direction = direction
        self.moving = True

    def stop(self):
        """
        Train stops.
        """
        self.moving = False

    def spawn(self):
        """
        Spawn train.
        """
        self._init_pointer()
        self.state = "spawned"
        self.start(self.direction)

    def despawn(self):
        """
        Despawn train.
        """
        self.state = "despawned"
        self.stop()
        self._update_goals()

    def _init_pointer(self):
        """
        Initialize the trajectory pointer.
        TODO: Do everything with just one pointer. Nose of the train should be pointed to direction of movement, always.
        """
        if self.direction == "forward":
            self.rightmost_position_pointer = len(self.trajectory) - 1
        elif self.direction == "backward":
            self.leftmost_position_pointer = 0

    def _update_goals(self):
        """
        Check the status of goals.
        """
        for goal in self.goals:
            goal.update()

    @property
    def leftmost_position_pointer(self):
        return self.rightmost_position_pointer - self.length

    @leftmost_position_pointer.setter
    def leftmost_position_pointer(self, p):
        self.rightmost_position_pointer = p + self.length

    @property
    def trajectory_pointer_increment(self):
        if self.moving:
            if self.direction == "forward":
                return +1
            elif self.direction == "backward":
                return -1
        else:
            return 0

    @property
    def length(self):
        length = 0
        for wagon in self.wagons:
            length += wagon.length
        return length

    @property
    def rect(self):
        if self.wagons:
            rect = self.wagons[0].rect
            return rect.unionall([wagon.rect for wagon in self.wagons])
        else:
            return None

