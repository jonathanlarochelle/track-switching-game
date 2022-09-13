# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pygame as pg

# import your own module
from tracktile import TrackTile
from constants import TILE_LENGTH


class Map:
    """
    Represents a map of tiles
    """

    tiles: list[TrackTile]
    portals: dict[str, TrackTile]
    platforms: dict[str, TrackTile]
    rows: int
    cols: int

    def __init__(self):
        self.tiles = list()
        # Map is manually generated, row by row (for now ...)
        row = 0
        self.tiles += [TrackTile((0 * TILE_LENGTH, row * TILE_LENGTH), "mm", portal="A"),
                       TrackTile((1 * TILE_LENGTH, row * TILE_LENGTH), "mm", "md"),
                       TrackTile((2 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((3 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((4 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((5 * TILE_LENGTH, row * TILE_LENGTH), "mm", "md"),
                       TrackTile((6 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((7 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((8 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((9 * TILE_LENGTH, row * TILE_LENGTH), "mm", "dm"),
                       TrackTile((10 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((11 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((12 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((13 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((14 * TILE_LENGTH, row * TILE_LENGTH), "mm", platform="1"),
                       TrackTile((15 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((16 * TILE_LENGTH, row * TILE_LENGTH), "mm", "dm"),
                       TrackTile((17 * TILE_LENGTH, row * TILE_LENGTH), "mm", "md"),
                       TrackTile((18 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((19 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((20 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((21 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((22 * TILE_LENGTH, row * TILE_LENGTH), "mm", "dm"),
                       TrackTile((23 * TILE_LENGTH, row * TILE_LENGTH), "mm", portal="D")]
        row = 1
        self.tiles += [TrackTile((2 * TILE_LENGTH, row * TILE_LENGTH), "ud"),
                       TrackTile((6 * TILE_LENGTH, row * TILE_LENGTH), "um"),
                       TrackTile((7 * TILE_LENGTH, row * TILE_LENGTH), "mm", "dm"),
                       TrackTile((8 * TILE_LENGTH, row * TILE_LENGTH), "mm", "mu"),
                       TrackTile((9 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((10 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((11 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((12 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((13 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((14 * TILE_LENGTH, row * TILE_LENGTH), "mm", platform="2"),
                       TrackTile((15 * TILE_LENGTH, row * TILE_LENGTH), "mm", "mu"),
                       TrackTile((16 * TILE_LENGTH, row * TILE_LENGTH), "md"),
                       TrackTile((18 * TILE_LENGTH, row * TILE_LENGTH), "ud"),
                       TrackTile((21 * TILE_LENGTH, row * TILE_LENGTH), "du")]
        row = 2
        self.tiles += [TrackTile((0 * TILE_LENGTH, row * TILE_LENGTH), "mm", portal="B"),
                       TrackTile((1 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((2 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((3 * TILE_LENGTH, row * TILE_LENGTH), "mm", "um"),
                       TrackTile((4 * TILE_LENGTH, row * TILE_LENGTH), "mm", "md"),
                       TrackTile((5 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((6 * TILE_LENGTH, row * TILE_LENGTH), "mm", "mu"),
                       TrackTile((7 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((8 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((9 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((10 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((11 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((12 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((13 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((14 * TILE_LENGTH, row * TILE_LENGTH), "mm", platform="3"),
                       TrackTile((15 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((16 * TILE_LENGTH, row * TILE_LENGTH), "mm", "dm"),
                       TrackTile((17 * TILE_LENGTH, row * TILE_LENGTH), "mm", "um"),
                       TrackTile((18 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((19 * TILE_LENGTH, row * TILE_LENGTH), "mm", "um"),
                       TrackTile((20 * TILE_LENGTH, row * TILE_LENGTH), "mm", "mu"),
                       TrackTile((21 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((22 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((23 * TILE_LENGTH, row * TILE_LENGTH), "mm", portal="E")]
        row = 3
        self.tiles += [TrackTile((5 * TILE_LENGTH, row * TILE_LENGTH), "um"),
                       TrackTile((6 * TILE_LENGTH, row * TILE_LENGTH), "mm", "md"),
                       TrackTile((7 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((8 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((9 * TILE_LENGTH, row * TILE_LENGTH), "mm", "dm"),
                       TrackTile((10 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((11 * TILE_LENGTH, row * TILE_LENGTH), "mm", "md"),
                       TrackTile((12 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((13 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((14 * TILE_LENGTH, row * TILE_LENGTH), "mm", platform="4"),
                       TrackTile((15 * TILE_LENGTH, row * TILE_LENGTH), "mm", "mu"),
                       TrackTile((16 * TILE_LENGTH, row * TILE_LENGTH), "md")]
        row = 4
        self.tiles += [TrackTile((0 * TILE_LENGTH, row * TILE_LENGTH), "mm", portal="C"),
                       TrackTile((1 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((2 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((3 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((4 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((5 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((6 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((7 * TILE_LENGTH, row * TILE_LENGTH), "mm", "um"),
                       TrackTile((8 * TILE_LENGTH, row * TILE_LENGTH), "mm", "mu"),
                       TrackTile((9 * TILE_LENGTH, row * TILE_LENGTH), "mm", "md"),
                       TrackTile((10 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((11 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((12 * TILE_LENGTH, row * TILE_LENGTH), "mm", "um"),
                       TrackTile((13 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((14 * TILE_LENGTH, row * TILE_LENGTH), "mm", platform="5"),
                       TrackTile((15 * TILE_LENGTH, row * TILE_LENGTH), "md"),
                       TrackTile((17 * TILE_LENGTH, row * TILE_LENGTH), "ud")]
        row = 5
        self.tiles += [TrackTile((10 * TILE_LENGTH, row * TILE_LENGTH), "um"),
                       TrackTile((11 * TILE_LENGTH, row * TILE_LENGTH), "mm", "md"),
                       TrackTile((12 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((13 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((14 * TILE_LENGTH, row * TILE_LENGTH), "mm", platform="6"),
                       TrackTile((15 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((16 * TILE_LENGTH, row * TILE_LENGTH), "mm", "um"),
                       TrackTile((17 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((18 * TILE_LENGTH, row * TILE_LENGTH), "mm", "um"),
                       TrackTile((19 * TILE_LENGTH, row * TILE_LENGTH), "mm", "dm"),
                       TrackTile((20 * TILE_LENGTH, row * TILE_LENGTH), "mm", "md"),
                       TrackTile((21 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((22 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((23 * TILE_LENGTH, row * TILE_LENGTH), "mm", portal="F")]
        row = 6
        self.tiles += [TrackTile((12 * TILE_LENGTH, row * TILE_LENGTH), "um"),
                       TrackTile((13 * TILE_LENGTH, row * TILE_LENGTH), "mm", "md"),
                       TrackTile((14 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((15 * TILE_LENGTH, row * TILE_LENGTH), "mm", platform="7"),
                       TrackTile((16 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((17 * TILE_LENGTH, row * TILE_LENGTH), "mm", "dm"),
                       TrackTile((18 * TILE_LENGTH, row * TILE_LENGTH), "mm", "mu"),
                       TrackTile((19 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((20 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((21 * TILE_LENGTH, row * TILE_LENGTH), "mm", "um"),
                       TrackTile((22 * TILE_LENGTH, row * TILE_LENGTH), "mm"),
                       TrackTile((23 * TILE_LENGTH, row * TILE_LENGTH), "mm", portal="G")]
        row = 7
        self.tiles += [TrackTile((14 * TILE_LENGTH, row * TILE_LENGTH), "um"),
                       TrackTile((15 * TILE_LENGTH, row * TILE_LENGTH), "mm", platform="8"),
                       TrackTile((16 * TILE_LENGTH, row * TILE_LENGTH), "mu")]

        self.portals = dict()
        self.platforms = dict()
        for tile in self.tiles:
            if tile.portal is not None:
                self.portals[tile.portal] = tile
            if tile.platform is not None:
                self.platforms[tile.platform] = tile

    def update(self):
        pass

    def draw(self, surf: pg.surface.Surface):
        for tile in self.tiles:
            surf.blit(tile.image, tile.rect)

    def set_tile(self, row: int, col: int, tile: TrackTile):
        pass

    def tile_at(self, pos: tuple[float]) -> TrackTile:
        pass
