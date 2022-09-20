# -*- coding: utf-8 -*-

# import built-in module
import abc

# import third-party modules
import pygame as pg

# import your own module


class Condition(abc.ABC):
    """
    Helper class for instructions, that contains a single condition that can be true or false about the current state
    of the game.
    """

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def is_met(self) -> bool:
        """
        Return True is the condition is met.
        """
        pass


class AndCondition(Condition):
    """
    Condition: All of the provided conditions are true.
    """

    def __init__(self, conditions: list[Condition]):
        self._conditions = conditions

    def is_met(self) -> bool:
        for cond in self._conditions:
            if not cond.is_met():
                return False
        return True


class OrCondition(Condition):
    """
    Condition: One or more of the provided conditions is/are true.
    """

    def __init__(self, conditions: list[Condition]):
        self._conditions = conditions

    def is_met(self) -> bool:
        for cond in self._conditions:
            if cond.is_met():
                return True
        return False


class NotCondition(Condition):
    """
    Condition: Provided condition is False.
    """

    def __init__(self, condition: Condition):
        self._condition = condition

    def is_met(self) -> bool:
        if not self._condition.is_met():
            return True
        else:
            return False


class TimeSinceBeginningCondition(Condition):
    """
    Condition: Specified time (in milliseconds since pygame.init()( is reached.
    """

    def __init__(self, milliseconds: int):
        self._milliseconds = milliseconds

    def is_met(self) -> bool:
        if pg.time.get_ticks() >= self._milliseconds:
            return True
        else:
            return False


class ObjectAttributeCondition(Condition):
    """
    Condition: Object.attribute has specified value.
    """

    def __init__(self, object, attribute: str, value):
        # Check if attribute actually exists
        getattr(object, attribute)

        self._object = object
        self._attr = attribute
        self._value = value

    def is_met(self) -> bool:
        if getattr(self._object, self._attr) == self._value:
            return True
        else:
            return False


class GroupContainedInGroupCondition(Condition):
    """
    Condition: Moving group is fully contained in fixed group.
    """

    def __init__(self, moving_group: pg.sprite.Group, fixed_group: pg.sprite.Group):
        self._moving_group = moving_group
        self._fixed_group_rect = self._get_group_rect(fixed_group)

    def is_met(self) -> bool:
        if self._fixed_group_rect.contains(self._get_group_rect(self._moving_group)):
            return True
        else:
            return False

    def _get_group_rect(self, group: pg.sprite.Group) -> pg.Rect:
        rect = None
        for s in group.sprites():
            if not rect:
                rect = s.rect
            else:
                rect = rect.union(s.rect)
        return rect


class GroupsCollideCondition(Condition):
    """
    Condition: Group 1 collides with Group 2.
    """

    def __init__(self, group1: pg.sprite.Group, group2: pg.sprite.Group):
        self._group1 = group1
        self._group2 = group2

    def is_met(self) -> bool:
        if pg.sprite.groupcollide(self._group1, self._group2, False, False):
            return True
        else:
            return False
