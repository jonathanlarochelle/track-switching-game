# -*- coding: utf-8 -*-

# import built-in module
import abc
import math

# import third-party modules
import pygame as pg
from pygame.math import Vector2

# import your own module
import train
import map
from constants import TILE_LENGTH


class Instruction(abc.ABC):
    """
    Abstract class representing an instruction that trains can have. An instruction is a command waiting to happen.
    On the fulfillment of condition(s), a series of change will happen.
    Instructions can be seen, in a sense, as the "plan" for a given train during its lifetime.
    TODO: Should that be merge with Goal? Come back to this question after some further developments.
    """

    _is_completed = False

    @abc.abstractmethod
    def __init__(self, train: train.Train):
        pass

    @abc.abstractmethod
    def check_conditions(self):
        """
        Check if conditions are met. If so, call .on_conditions_met().
        """
        pass

    @abc.abstractmethod
    def on_conditions_met(self):
        """
        Operations to be done when the conditions are met.
        """
        pass

    @property
    def is_completed(self) -> bool:
        """
        Returns True if instruction has been completed.
        """
        return self._is_completed


class SpawnInstruction(Instruction):
    """
    Spawns the train at a specific portal when the time is reached.
    """

    def __init__(self, train: train.Train, map: map.Map, portal: str, time: int):
        self._train = train
        self._map = map
        self.spawn_portal = portal
        self.spawn_time = time

        # Prepare trajectory
        spawn_tile_traj = self._map.portals[self.spawn_portal].sprites()[0].get_trajectory()
        nb_padding_tiles = math.ceil(train.length / TILE_LENGTH)
        if self.spawn_portal in ["A", "B", "C"]:
            for i in range(nb_padding_tiles * TILE_LENGTH):
                self._train.trajectory.append(Vector2(-(nb_padding_tiles*TILE_LENGTH)+i, spawn_tile_traj[0].y))
            self._train.trajectory += spawn_tile_traj
            self._train.direction = "forward"
            self._train.rightmost_position_pointer = len(self._train.trajectory) - 31
        elif self.spawn_portal in ["D", "E", "F", "G"]:
            self._train.trajectory += spawn_tile_traj
            for i in range(nb_padding_tiles * TILE_LENGTH):
                self._train.trajectory.append(Vector2(spawn_tile_traj[-1].x + i, spawn_tile_traj[0].y))
            self._train.direction = "backward"
            self._train.leftmost_position_pointer = 30

    def check_conditions(self):
        """
        Check if conditions are met. If so, call .on_conditions_met().
        """
        if not self.is_completed:
            if self.spawn_time < pg.time.get_ticks():
                self.on_conditions_met()

    def on_conditions_met(self):
        """
        Operations to be done when the conditions are met.
        """
        self._train.spawn()
        self._is_completed = True