# -*- coding: utf-8 -*-

# import built-in module
import abc
import math
from typing import Union

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
    _completion_time: Union[int, None] = None

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

    def instruction_complete(self):
        """
        Instruction is completed.
        """
        self._is_completed = True
        self._completion_time = pg.time.get_ticks()

    @property
    def is_completed(self) -> bool:
        """
        Returns True if instruction has been completed.
        """
        return self._is_completed

    @property
    def completion_time(self) -> Union[int, None]:
        """
        If .is_completed, returns the time (in milliseconds since game init()) of completion.
        Else, return None.
        """
        return self._completion_time


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
        Conditions: has the spawn_time been reached?
        """
        if not self.is_completed:
            if self.spawn_time < pg.time.get_ticks():
                self.on_conditions_met()

    def on_conditions_met(self):
        """
        Spawn the train.
        """
        self._train.spawn()
        self.instruction_complete()


class DespawnInstruction(Instruction):
    """
    Despawns the train when it is fully out of the playing field.
    """

    def __init__(self, train: train.Train, playing_field: pg.Rect):
        self._train = train
        self._playing_field = playing_field

    def check_conditions(self):
        """
        Conditions: the train is currently spawned, and is fully outside the playing field.
        """
        if not self.is_completed:
            if self._train.state == "spawned":
                if not self._playing_field.colliderect(self._train.rect):
                    self.on_conditions_met()

    def on_conditions_met(self):
        """
        Depawn the train.
        """
        self._train.despawn()
        self.instruction_complete()


class WaitAtPlatformInstruction(Instruction):
    """
    Waits for a given time at the target platform.
    """

    def __init__(self, train: train.Train, map: map.Map, platform, nb_wait_frames):
        self._train = train
        self.target_platform = platform
        self.nb_wait_frames = nb_wait_frames

        self._platform_collider = None
        for tile in map.platforms[self.target_platform].sprites():
            if not self._platform_collider:
                self._platform_collider = tile.rect
            else:
                self._platform_collider = self._platform_collider.union(tile.rect)

    def check_conditions(self):
        """
        To wait, we should be currently in movement and fully contained in the platform.
        """
        if not self.is_completed:
            if self._train.state == "spawned":
                if self._train.moving:
                    if self._platform_collider.contains(self._train.rect):
                        self.on_conditions_met()

    def on_conditions_met(self):
        """
        Train stops and waits for specified nb of frames.
        """
        self._train.wait(self.nb_wait_frames)
        self.instruction_complete()
