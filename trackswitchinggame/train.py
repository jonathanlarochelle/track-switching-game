# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pygame as pg

# import your own module
from trackswitchinggame.wagonsprite import WagonSprite
import trackswitchinggame.instruction as instruction


class Train:
    """
    Represents a self-contained train, which is composed of wagons.
    The train's movement follow points stored in trajectory.
    """

    def __init__(self, id):
        # Set-up wagons
        self._wagons = pg.sprite.Group()
        self._wagons.add(WagonSprite("assets/trains/ice_loc.png", id))
        self._wagons.add(WagonSprite("assets/trains/ice_wagon.png", id))
        self._wagons.add(WagonSprite("assets/trains/ice_loc.png", id, True))

        self._instructions = []
        self.trajectory = list()
        self.rightmost_position_pointer = None  # Initialized when calling spawn()

        # State variables
        self._spawned = False
        self._moving = False
        self._waiting = False
        self.direction = None
        self._wait_end = 0

        # state can be "waiting for spawn", "spawned", "despawned"
        self._state = "waiting for spawn"

    def update(self):
        """
        Update position of the train
        """
        # Instruction
        for instr in self._instructions:
            if not instr.fulfilled:
                instr.update()
                # If instruction was just fulfilled, we prevent other instructions from being checked until next frame.
                if instr.fulfilled:
                    break

        if self.moving:
            # Update position
            self.rightmost_position_pointer += self.trajectory_pointer_increment
            if self.rightmost_position_pointer >= len(self.trajectory) or self.leftmost_position_pointer < 0:
                # No trajectory defined, we do not move.
                self.rightmost_position_pointer -= self.trajectory_pointer_increment
            else:
                current_offset = self.rightmost_position_pointer

                for wagon in self._wagons.sprites():
                    # Should the position of the axles be handled individually by each wagon?
                    # Do we want wagons to have a variable axle offset??
                    axle_1_pointer = current_offset - 5
                    axle_2_pointer = current_offset - 25
                    position_axle_1 = self.trajectory[axle_1_pointer]
                    position_axle_2 = self.trajectory[axle_2_pointer]
                    wagon.update(position_axle_1, position_axle_2)
                    current_offset -= wagon.length

        if self.waiting:
            if pg.time.get_ticks() > self._wait_end:
                self._waiting = False
                self.start(self.direction)

    def add_instruction(self, instruction: instruction.Instruction):
        self._instructions.append(instruction)

    def draw(self, screen: pg.surface.Surface):
        """
        Draw the train.
        """
        if self.spawned:
            self._wagons.draw(screen)

    def start(self, direction):
        """
        Sets train in movement in desired direction.
        """
        if not self.waiting:
            self.direction = direction
            self._moving = True

    def stop(self):
        """
        Train stops.
        """
        self._moving = False

    def spawn(self):
        """
        Spawn train.
        """
        self._spawned = True
        self.start(self.direction)

    def despawn(self):
        """
        Despawn train.
        """
        self._spawned = False
        self.stop()

    def wait(self, milliseconds):
        """
        Wait for number of milliseconds.
        """
        self._wait_end = pg.time.get_ticks() + milliseconds
        self.stop()
        self._waiting = True

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
        for wagon in self._wagons:
            length += wagon.length
        return length

    @property
    def rect(self):
        if self._wagons:
            rect = self._wagons.sprites()[0].rect
            return rect.unionall([wagon.rect for wagon in self._wagons.sprites()])
        else:
            return None

    @property
    def spawned(self) -> bool:
        return self._spawned

    @property
    def moving(self) -> bool:
        return self._moving

    @property
    def waiting(self) -> bool:
        return self._waiting

    @property
    def wagons(self) -> pg.sprite.Group:
        return self._wagons