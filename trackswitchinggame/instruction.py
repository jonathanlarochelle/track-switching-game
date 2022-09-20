# -*- coding: utf-8 -*-
from __future__ import annotations  # Solves circular import problem with referencing game

# import built-in module

# import third-party modules
import pygame as pg

# import your own module
import trackswitchinggame.condition as condition
import trackswitchinggame.command as command
import trackswitchinggame.train as train
import trackswitchinggame.tracktile as tracktile


class Instruction:
    """
    An Instruction contains commands which are executed when a condition is reached.
    """

    def __init__(self, condition: condition.Condition, commands: list[command.Command]):
        self._condition = condition
        self._commands = commands
        self._fulfilled = False
        self._fulfillment_time = None

    def update(self) -> bool:
        """
        If condition is met, execute commands.
        """
        if not self.fulfilled:
            if self.condition.is_met():
                self._fulfilled = True
                self._fulfillment_time = pg.time.get_ticks()
                for command in self._commands:
                    command.execute()
                return True
        return False

    @property
    def condition(self) -> condition.Condition:
        return self._condition

    @property
    def commands(self) -> list[command.Command]:
        return self._commands

    @property
    def fulfilled(self) -> bool:
        return self._fulfilled

    @property
    def fulfillment_time(self) -> int:
        # Milliseconds since pygame.init()
        return self._fulfillment_time


def create_spawn_instruction(train: train.Train, spawn_tile: tracktile.TrackTile, spawn_time: int = 0) -> Instruction:
    """
    Helper function to create a spawn instruction
    :param train:
    :param spawn_tile:
    :param spawn_time: milliseconds since pygame.init()
    """
    conditions = []
    commands = []

    # Conditions
    conditions.append(condition.ObjectAttributeCondition(train, "spawned", False))
    conditions.append(condition.TimeSinceBeginningCondition(spawn_time))

    # Commands
    commands.append(command.SpawnTrainAtPortalCommand(train, spawn_tile))

    return Instruction(condition.AndCondition(conditions), commands)


def create_platform_instruction(train: train.Train, platform_tiles: pg.sprite.Group, wait_delay: int) -> Instruction:
    """
    Helper function to create a platform Instruction.
    Train departs after wait_delay, if departure_time has been reached.
    :param train:
    :param platform_tiles:
    :param wait_delay: delay to wait at the platform (in milliseconds)
    """
    conditions = []
    commands = []

    # Conditions
    conditions.append(condition.ObjectAttributeCondition(train, "spawned", True))
    conditions.append(condition.GroupContainedInGroupCondition(train.wagons, platform_tiles))

    # Commands
    commands.append(command.WaitCommand(train, wait_delay))

    return Instruction(condition.AndCondition(conditions), commands)


def create_despawn_instruction(train: train.Train, playing_field: pg.sprite.Group) -> Instruction:
    """
    General despawn instruction.
    :param train:
    :param playing_field:
    :return:
    """
    conditions = []
    commands = []

    # Conditions
    conditions.append(condition.ObjectAttributeCondition(train, "spawned", True))
    conditions.append(condition.NotCondition(condition.GroupsCollideCondition(train.wagons, playing_field)))

    # Commands
    commands.append(command.DespawnCommand(train))

    return Instruction(condition.AndCondition(conditions), commands)
