# -*- coding: utf-8 -*-

# import built-in module
import math

# import third-party modules
import pygame as pg

# import your own module
from tracktile import TrackTile
from constants import TILE_LENGTH


class Map:
    """
    Represents a map of tiles
    """

    def __init__(self):
        map_array = [["mm+A", "mm+md", "mm", "mm", "mm", "mm+md", "mm", "mm", "mm", "mm+dm", "mm", "mm", "mm", "mm",
                      "mm+1", "mm+1", "mm+1", "mm", "mm+dm", "mm+md", "mm", "mm", "mm", "mm", "mm+dm", "mm+D"],
                     ["", "", "ud", "", "", "", "um", "mm+dm", "mm+mu", "mm", "mm", "mm", "mm", "mm", "mm+2", "mm+2",
                      "mm+2", "mm+mu", "md", "", "ud", "", "", "du", "", ""],
                     ["mm+B", "mm", "mm", "mm+um", "mm+md", "mm", "mm+mu", "mm", "mm", "mm", "mm", "mm", "mm", "mm",
                      "mm+3", "mm+3", "mm+3", "mm", "mm+dm", "mm+um", "mm", "mm+um", "mm+mu", "mm", "mm", "mm+E"],
                     ["", "", "", "", "", "um", "mm+md", "mm", "mm", "mm+dm", "mm", "mm+md", "mm", "mm", "mm+4", "mm+4",
                      "mm+4", "mm+mu", "md", "", "", "", "", "", "", ""],
                     ["mm+C", "mm", "mm", "mm", "mm", "mm", "mm", "mm+um", "mm+mu", "mm+md", "mm", "mm", "mm+um", "mm",
                      "mm+5", "mm+5", "mm+5", "md", "", "ud", "", "", "", "", "", ""],
                     ["", "", "", "", "", "", "", "", "", "", "um", "mm+md", "mm", "mm", "mm+6", "mm+6", "mm+6", "mm",
                      "mm+um", "mm", "mm+um", "mm+dm", "mm+md", "mm", "mm", "mm+F"],
                     ["", "", "", "", "", "", "", "", "", "", "", "", "um", "mm+md", "mm", "mm+7", "mm+7", "mm+7", "mm",
                      "mm+dm", "mm+mu", "mm", "mm", "mm+um", "mm", "mm+G"],
                     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "um", "mm+8", "mm+8", "mm+8", "mu", "",
                      "", "", "", "", "", ""]]

        self._parse_raw_map(map_array)

        self._tiles_list = list()
        for row in self.tiles_array:
            for tile in row:
                if tile:
                    self._tiles_list.append(tile)

        self.portals = dict()
        self.platforms = dict()
        for tile in self._tiles_list:
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

    def update(self):
        pass

    def draw(self, surf: pg.surface.Surface):
        for tile in self._tiles_list:
            surf.blit(tile.image, tile.rect)

    def set_tile(self, row: int, col: int, tile: TrackTile):
        pass

    def tile_at(self, pos: tuple[float]) -> TrackTile:
        # Get the tile at a certain position
        col = math.floor(pos[0]/TILE_LENGTH)
        row = math.floor(pos[1]/TILE_LENGTH)

        # If (col, row) are out of bounds, return None
        if -1 < row < len(self.tiles_array) and -1 < col < len(self.tiles_array[0]):
            return self.tiles_array[row][col]
        else:
            return None

    def _parse_raw_map(self, raw_map):
        self.tiles_array = list()
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

                    tile_row.append(TrackTile((col_id * TILE_LENGTH, row_id * TILE_LENGTH),
                                              tracktile_mainpath, tracktile_altpath, tracktile_portal, tracktile_platform))
            self.tiles_array.append(tile_row)
            del tile_row # Check if necessary

