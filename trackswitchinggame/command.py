# -*- coding: utf-8 -*-
from __future__ import annotations  # Solves circular import problem with referencing game

# import built-in module
import abc
import math

# import third-party modules
from pygame.math import Vector2

# import your own module
import trackswitchinggame.tracktile as tracktile
import trackswitchinggame.train as train
from trackswitchinggame.constants import TILE_LENGTH


class Command(abc.ABC):
    """
    Represents a command that can be executed.
    """

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def execute(self):
        """
        Execute the command.
        """
        pass


class SpawnTrainAtPortalCommand(Command):
    """
    Command: spawn the train at portal.
    """

    def __init__(self, train: train.Train, portal_tile: tracktile.TrackTile):
        self._train = train

        # Prepare trajectory
        spawn_tile_traj = portal_tile.get_trajectory()
        nb_padding_tiles = math.ceil(train.length / TILE_LENGTH)
        if portal_tile.portal in ["A", "B", "C"]:
            for i in range(nb_padding_tiles * TILE_LENGTH):
                self._train.trajectory.append(Vector2(-(nb_padding_tiles * TILE_LENGTH) + i, spawn_tile_traj[0].y))
            self._train.trajectory += spawn_tile_traj
            self._train.direction = "forward"
            self._train.rightmost_position_pointer = len(self._train.trajectory) - 31
        elif portal_tile.portal in ["D", "E", "F", "G"]:
            self._train.trajectory += spawn_tile_traj
            for i in range(nb_padding_tiles * TILE_LENGTH):
                self._train.trajectory.append(Vector2(spawn_tile_traj[-1].x + i, spawn_tile_traj[0].y))
            self._train.direction = "backward"
            self._train.leftmost_position_pointer = 30

    def execute(self):
        self._train.spawn()


class WaitCommand(Command):
    """
    Command: calls train.wait(milliseconds).
    """

    def __init__(self, train: train.Train, milliseconds: int):
        self._train = train
        self._milliseconds = milliseconds

    def execute(self):
        self._train.wait(self._milliseconds)


class DespawnCommand(Command):
    """
    Command: calls train.despawn()
    """

    def __init__(self, train: train.Train):
        self._train = train

    def execute(self):
        self._train.despawn()
