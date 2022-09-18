# -*- coding: utf-8 -*-

from __future__ import annotations  # Solves circular import problem with referencing game

# import built-in module
import abc

# import third-party modules

# import your own module
import game
import train


class Goal(abc.ABC):
    """
    Abstract class representing a goal that trains can have.
    At each tick, the conditions are checked. If they are met, the goal is achieved.
    Once achieved, a goal cannot be "unachieved".
    """

    @abc.abstractmethod
    def __init__(self, game: game.Game, train: train.Train):
        pass

    @abc.abstractmethod
    def update(self):
        """
        Update status of goal based on current game conditions.
        """
        pass

    @property
    def is_achieved(self) -> bool:
        return self._goal_achieved


class PlatformGoal(Goal):
    """
    Goal to reach a specific platform.
    """

    def __init__(self, game: game.Game, train: train.Train, target_platform: str):
        self._game = game
        self._train = train
        self._goal_achieved = False

        self.target_platform = target_platform
        self._platform_collider = None
        for tile in self._game.map.platforms[self.target_platform].sprites():
            if not self._platform_collider:
                self._platform_collider = tile.rect
            else:
                self._platform_collider = self._platform_collider.union(tile.rect)

    def update(self):
        """
        Platform goal is achieved when
            1) full length of the train is at the platform
            2) (train is stopped)
        """
        if not self.is_achieved:
            if self._train.state == "spawned":
                if self._platform_collider.contains(self._train.rect):
                    self._goal_achieved = True


class ExitPortalGoal(Goal):
    """
    Goal to exit the map using a certain portal.
    """

    def __init__(self, game: game.Game, train: train.Train, target_portal: str):
        self._game = game
        self._train = train
        self._goal_achieved = False

        self.target_portal = target_portal
        self._portal_collider = None
        for tile in self._game.map.portals[self.target_portal].sprites():
            if not self._portal_collider:
                self._portal_collider = tile.rect
            else:
                self._portal_collider = self._portal_collider.union(tile.rect)
        self._good_portal = False

    def update(self):
        """
        ExitPortal goal is achieved when
            1) train is despawned
            2) last portal it saw was the target portal
        """
        if not self.is_achieved:
            if self._portal_collider.colliderect(self._train.rect):
                self._good_portal = True
            if self._train.state == "despawned":
                if self._good_portal:
                    self._goal_achieved = True


class EntryPortalGoal(Goal):
    """
    Goal to enter the map using a certain portal.
    """

    def __init__(self, game: game.Game, train: train.Train, target_portal: str):
        self._game = game
        self._train = train
        self._goal_achieved = False

        self.target_portal = target_portal
        self._portal_collider = None
        for tile in self._game.map.portals[self.target_portal].sprites():
            if not self._portal_collider:
                self._portal_collider = tile.rect
            else:
                self._portal_collider = self._portal_collider.union(tile.rect)
        self._good_portal = False

    def update(self):
        """
        Goal is achieved when
            1) train is spawned
            2) first portal it saw was the target portal
        """
        if not self.is_achieved:
            if self._train.state == "spawned":
                if self._portal_collider.colliderect(self._train.rect):
                    self._goal_achieved = True
