# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pygame as pg
import pygame.time
import pytest

# import your own module
from trackswitchinggame.condition import *


class TestCondition:

    @pytest.fixture
    def true_condition(self):
        class MockCondition(Condition):
            def __init__(self):
                pass

            def is_met(self):
                return True
        return MockCondition()

    @pytest.fixture
    def false_condition(self):
        class MockCondition(Condition):
            def __init__(self):
                pass

            def is_met(self):
                return False

        return MockCondition()

    @pytest.fixture
    def object_with_one_attr(self):
        class ObjectWithOneAttr:
            def __init__(self):
                self.my_attr = "good_value"
        return ObjectWithOneAttr()

    def test_and_condition_1(self, true_condition):
        condition = AndCondition([true_condition, true_condition])
        assert condition.is_met() is True

    def test_and_condition_2(self, true_condition, false_condition):
        condition = AndCondition([true_condition, false_condition])
        assert condition.is_met() is False

    def test_or_condition_1(self, false_condition):
        condition = OrCondition([false_condition, false_condition])
        assert condition.is_met() is False

    def test_or_condition_2(self, true_condition, false_condition):
        condition = OrCondition([true_condition, false_condition])
        assert condition.is_met() is True

    def test_not_condition_1(self, false_condition):
        condition = NotCondition(false_condition)
        assert condition.is_met() is True

    def test_not_condition_2(self, true_condition):
        condition = NotCondition(true_condition)
        assert condition.is_met() is False

    def test_time_since_beginning_condition_1(self, mocker):
        mocker.patch("pygame.time.get_ticks", return_value=0)
        condition = TimeSinceBeginningCondition(10)
        assert condition.is_met() is False

    def test_time_since_beginning_condition_2(self, mocker):
        mocker.patch("pygame.time.get_ticks", return_value=20)
        condition = TimeSinceBeginningCondition(10)
        assert condition.is_met() is True

    def test_object_attribute_condition_1(self, object_with_one_attr):
        obj = object_with_one_attr
        with pytest.raises(AttributeError):
            _ = ObjectAttributeCondition(obj, "bad_attr", "rdm_value")

    def test_object_attribute_condition_2(self, object_with_one_attr):
        obj = object_with_one_attr
        condition = ObjectAttributeCondition(obj, "my_attr", "bad_value")
        assert condition.is_met() is False

    def test_object_attribute_condition_3(self, object_with_one_attr):
        obj = object_with_one_attr
        condition = ObjectAttributeCondition(obj, "my_attr", "good_value")
        assert condition.is_met() is True

    def test_group_contained_in_group_condition_1(self):
        small_group = pg.sprite.Group()
        small_sprite = pg.sprite.Sprite(small_group)
        small_sprite.image = pg.Surface([10, 10])
        small_sprite.rect = small_sprite.image.get_rect()

        container_group = pg.sprite.Group()
        container_sprite = pg.sprite.Sprite(container_group)
        container_sprite.image = pg.Surface([100, 100])
        container_sprite.rect = container_sprite.image.get_rect()

        condition = GroupContainedInGroupCondition(small_group, container_group)
        assert condition.is_met() is True

    def test_group_contained_in_group_condition_2(self):
        small_group = pg.sprite.Group()
        small_sprite = pg.sprite.Sprite(small_group)
        small_sprite.image = pg.Surface([10, 10])
        small_sprite.rect = small_sprite.image.get_rect()

        container_group = pg.sprite.Group()
        container_sprite = pg.sprite.Sprite(container_group)
        container_sprite.image = pg.Surface([100, 100])
        container_sprite.rect = container_sprite.image.get_rect()
        container_sprite.rect.x = 5
        container_sprite.rect.y = 5

        condition = GroupContainedInGroupCondition(small_group, container_group)
        assert condition.is_met() is False

    def test_groups_collide_condition_1(self):
        group_1 = pg.sprite.Group()
        sprite_1 = pg.sprite.Sprite(group_1)
        sprite_1.image = pg.Surface([10, 10])
        sprite_1.rect = sprite_1.image.get_rect()

        group_2 = pg.sprite.Group()
        sprite_2 = pg.sprite.Sprite(group_2)
        sprite_2.image = pg.Surface([100, 100])
        sprite_2.rect = sprite_2.image.get_rect()
        sprite_2.rect.x = 5
        sprite_2.rect.y = 5

        condition = GroupsCollideCondition(group_1, group_2)
        assert condition.is_met() is True

    def test_groups_collide_condition_2(self):
        group_1 = pg.sprite.Group()
        sprite_1 = pg.sprite.Sprite(group_1)
        sprite_1.image = pg.Surface([10, 10])
        sprite_1.rect = sprite_1.image.get_rect()

        group_2 = pg.sprite.Group()
        sprite_2 = pg.sprite.Sprite(group_2)
        sprite_2.image = pg.Surface([100, 100])
        sprite_2.rect = sprite_2.image.get_rect()
        sprite_2.rect.x = 15
        sprite_2.rect.y = 15

        condition = GroupsCollideCondition(group_1, group_2)
        assert condition.is_met() is False
