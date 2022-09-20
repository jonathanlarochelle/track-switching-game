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


class SpawnInstruction(Instruction):
    """
    Instruction used to spawn the train.
    """

    def __init__(self, train: train.Train, spawn_time: int, spawn_portal: str):
        self._spawn_time = spawn_time
        self._spawn_portal = spawn_portal

        conditions = []
        commands = []

        # Conditions
        conditions.append(condition.ObjectAttributeCondition(train, "spawned", False))
        conditions.append(condition.TimeSinceBeginningCondition(spawn_time))

        # Commands
        commands.append(command.SpawnTrainCommand(train, spawn_portal))

        super().__init__(condition.AndCondition(conditions), commands)

    @property
    def spawn_time(self) -> int:
        return self._spawn_time

    @property
    def spawn_portal(self) -> str:
        return self._spawn_portal


class DespawnInstruction(Instruction):
    """
    Instruction used to despawn the train.
    """

    def __init__(self, train: train.Train, despawn_portal: str):
        self._despawn_portal = despawn_portal

        conditions = []
        commands = []

        # Conditions
        conditions.append(condition.ObjectAttributeCondition(train, "spawned", True))
        conditions.append(condition.NotCondition(condition.GroupsCollideCondition(train.wagons, train._map.tiles)))

        # Commands
        commands.append(command.DespawnCommand(train))

        super().__init__(condition.AndCondition(conditions), commands)

    @property
    def despawn_portal(self) -> str:
        return self._despawn_portal


class PlatformStopInstruction(Instruction):
    """
    Instruction used to stop at a platform.
    """

    def __init__(self, train: train.Train, platform: str, wait_duration: int):
        self._platform = platform

        conditions = []
        commands = []

        # Conditions
        conditions.append(condition.ObjectAttributeCondition(train, "spawned", True))
        conditions.append(condition.GroupContainedInGroupCondition(train.wagons, train._map.platforms[platform]))

        # Commands
        commands.append(command.WaitCommand(train, wait_duration))

        super().__init__(condition.AndCondition(conditions), commands)

    @property
    def platform(self) -> str:
        return self._platform
