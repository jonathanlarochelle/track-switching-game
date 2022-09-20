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


class SpawnTrainCommand(Command):
    """
    Command: spawn the train at portal.
    """

    def __init__(self, train: train.Train, portal: str):
        self._train = train
        self._portal = portal

    def execute(self):
        self._train.spawn(self._portal)


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
