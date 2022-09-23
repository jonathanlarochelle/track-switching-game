# -*- coding: utf-8 -*-

# import built-in module
from typing import Union
import json

# import third-party modules
import pygame as pg
from pygame import Vector2

# import your own module
from trackswitchinggame.tracktile import TrackTile
from trackswitchinggame.constants import *


class LevelMap:
    """
    Represents a map of tiles.
    """

    def __init__(self, level_file: str):
        self._tiles = pg.sprite.Group()
        self._nb_rows = 0
        self._nb_cols = 0

        # Load level from file
        with open(level_file) as f:
            data = json.load(f)
            self._entry_portals = data["entry_portals"]
            self._exit_portals = data["exit_portals"]
            self._platform_portal_connections = data["platform_portal_connections"]
            self._parse_raw_map(data["track_tiles"])
            self._level_name = data["name"]

        self._portals = dict()
        self._platforms = dict()
        for tile in self.tiles.sprites():
            if tile.portal is not None:
                try:
                    self._portals[tile.portal].add(tile)
                except KeyError:
                    self._portals[tile.portal] = pg.sprite.Group(tile)
            if tile.platform is not None:
                try:
                    self._platforms[tile.platform].add(tile)
                except KeyError:
                    self._platforms[tile.platform] = pg.sprite.Group(tile)

    def draw(self, surf: pg.surface.Surface):
        for tile in self.tiles.sprites():
            surf.blit(tile.image, tile.rect)

    def tile_at(self, pos: Vector2) -> Union[TrackTile, None]:
        for tile in self.tiles.sprites():
            if tile.rect.collidepoint(pos.x, pos.y):
                return tile
        return None

    def get_playing_field_rect(self) -> pg.Rect:
        pf_rect = None
        for tile in self.tiles.sprites():
            if not pf_rect:
                pf_rect = tile.rect
            else:
                pf_rect = pf_rect.union(tile.rect)
        return pf_rect

    def _parse_raw_map(self, raw_map):
        self._nb_rows = len(raw_map)
        self._nb_cols = len(raw_map[0])
        # create a TrackTile for each non-empty strings in raw_map
        # place these TrackTile objects in a temporary array, as well as a permanent Group()
        tiles_array = list()
        for row_id, row in enumerate(raw_map):
            tile_row = list()
            for col_id, el in enumerate(row):
                if el == "":
                    tile_row.append(None)
                else:
                    tracktile_mainpath = None
                    tracktile_altpath = None
                    tracktile_portal = None
                    tracktile_platform = None

                    params = el.split("+")

                    for param in params:
                        if len(param) == 2:
                            if not tracktile_mainpath:
                                tracktile_mainpath = param
                            else:
                                tracktile_altpath = param
                        elif len(param) == 1:
                            if param.isdigit():
                                tracktile_platform = param
                            else:
                                tracktile_portal = param
                        else:
                            pass
                    new_tile = TrackTile(Vector2(col_id * TILE_LENGTH, row_id * TILE_LENGTH), tracktile_mainpath,
                                         tracktile_altpath, tracktile_portal, tracktile_platform)
                    tile_row.append(new_tile)
                    self._tiles.add(new_tile)
            tiles_array.append(tile_row)
            del tile_row  # Check if necessary

        # Find neighbours
        neighbours_offset_map = {NW: Vector2(-TILE_LENGTH, -TILE_LENGTH),
                                 N: Vector2(0, -TILE_LENGTH),
                                 NE: Vector2(+TILE_LENGTH, -TILE_LENGTH),
                                 W: Vector2(-TILE_LENGTH, 0),
                                 E: Vector2(+TILE_LENGTH, 0),
                                 SW: Vector2(-TILE_LENGTH, +TILE_LENGTH),
                                 S: Vector2(0, +TILE_LENGTH),
                                 SE: Vector2(+TILE_LENGTH, +TILE_LENGTH)}
        for tile in self.tiles:
            for compass_dir, offset in neighbours_offset_map.items():
                tile_pos = Vector2(tile.rect.x, tile.rect.y)
                neighbour_tile = self.tile_at(tile_pos + offset)
                if neighbour_tile:
                    tile.set_neighbour(compass_dir, neighbour_tile)

    @property
    def tiles(self) -> pg.sprite.Group:
        return self._tiles

    @property
    def portals(self) -> dict:
        return self._portals

    @property
    def platforms(self) -> dict:
        return self._platforms

    @property
    def nb_rows(self) -> int:
        return self._nb_rows

    @property
    def nb_cols(self) -> int:
        return self._nb_cols

    @property
    def entry_portals(self) -> list[str]:
        return self._entry_portals

    @property
    def exit_portals(self) -> list[str]:
        return self._exit_portals

    @property
    def platform_portal_connections(self) -> dict[str]:
        return self._platform_portal_connections

    @property
    def level_name(self) -> str:
        return self._level_name
