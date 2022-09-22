# -*- coding: utf-8 -*-

# import built-in module
from typing import Union

# import third-party modules
import pygame as pg
from pygame import Vector2

# import your own module
from trackswitchinggame.tracktile import TrackTile
from trackswitchinggame.constants import *


class LevelMap:
    """
    Represents a map of tiles
    """

    def __init__(self):
        map_array = [["mm+A", "mm+md", "mm", "mm", "mm", "mm+md", "mm", "mm", "mm", "mm+dm", "mm", "mm", "mm", "mm",
                      "mm+1", "mm+1", "mm+1", "mm", "mm+dm", "mm+md", "mm", "mm", "mm", "mm", "mm+dm", "mm", "mm+D"],
                     ["", "", "ud", "", "", "", "um", "mm+dm", "mm+mu", "mm", "mm", "mm", "mm", "mm", "mm+2", "mm+2",
                      "mm+2", "mm+mu", "md", "", "ud", "", "", "du", "", "", ""],
                     ["mm+B", "mm", "mm", "mm+um", "mm+md", "mm", "mm+mu", "mm", "mm", "mm", "mm", "mm", "mm", "mm",
                      "mm+3", "mm+3", "mm+3", "mm", "mm+dm", "mm+um", "mm", "mm+um", "mm+mu", "mm", "mm", "mm", "mm+E"],
                     ["", "", "", "", "", "um", "mm+md", "mm", "mm", "mm+dm", "mm", "mm+md", "mm", "mm", "mm+4", "mm+4",
                      "mm+4", "mm+mu", "md", "", "", "", "", "", "", "", ""],
                     ["mm+C", "mm", "mm", "mm", "mm", "mm", "mm", "mm+um", "mm+mu", "mm+md", "mm", "mm", "mm+um", "mm",
                      "mm+5", "mm+5", "mm+5", "md", "", "ud", "", "", "", "", "", "", ""],
                     ["", "", "", "", "", "", "", "", "", "", "um", "mm+md", "mm", "mm", "mm+6", "mm+6", "mm+6", "mm",
                      "mm+um", "mm", "mm+um", "mm+dm", "mm+md", "mm", "mm", "mm", "mm+F"],
                     ["", "", "", "", "", "", "", "", "", "", "", "", "um", "mm+md", "mm", "mm+7", "mm+7", "mm+7", "mm",
                      "mm+dm", "mm+mu", "mm", "mm", "mm+um", "mm", "mm", "mm+G"],
                     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "um", "mm+8", "mm+8", "mm+8", "mu", "",
                      "", "", "", "", "", "", ""]]
        self._tiles = pg.sprite.Group()
        self._nb_rows = 0
        self._nb_cols = 0
        self._parse_raw_map(map_array)

        self.portals = dict()
        self.platforms = dict()
        for tile in self.tiles.sprites():
            if tile.portal is not None:
                try:
                    self.portals[tile.portal].add(tile)
                except KeyError:
                    self.portals[tile.portal] = pg.sprite.Group(tile)
            if tile.platform is not None:
                try:
                    self.platforms[tile.platform].add(tile)
                except KeyError:
                    self.platforms[tile.platform] = pg.sprite.Group(tile)

        self.input_portals = ["B", "C", "D", "F"]
        self.output_portals = ["A", "C", "E", "G"]
        self.platforms_connecting_portals = {"1": ["A", "B", "D", "E"],
                                             "2": ["A", "B", "D", "E"],
                                             "3": ["A", "B", "D", "E"],
                                             "4": ["A", "B", "C", "D", "E", "F", "G"],
                                             "5": ["A", "B", "C", "F", "G"],
                                             "6": ["A", "B", "C", "F", "G"],
                                             "7": ["A", "B", "C", "F", "G"],
                                             "8": ["A", "B", "C", "F", "G"]}

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
                    new_tile = TrackTile((col_id * TILE_LENGTH, row_id * TILE_LENGTH), tracktile_mainpath,
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
    def nb_rows(self) -> int:
        return self._nb_rows

    @property
    def nb_cols(self) -> int:
        return self._nb_cols

