# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pygame as pg
from pygame.math import Vector2

# import your own module
from trackswitchinggame.constants import *


class TrackTile(pg.sprite.Sprite):
    """
    Represents a track tile on the game map.
    """

    _PATH_CHAR_TO_COORDS = {"u": 0,
                            "m": (TILE_LENGTH / 2) - 1,
                            "d": TILE_LENGTH - 1}

    def __init__(self, pos: Vector2, main_path: str, alternative_path: str = None, portal: str = None,
                 platform: str = None, *groups: pg.sprite.AbstractGroup):
        super().__init__(*groups)
        self._position = pos
        self._main_path = main_path
        self._alt_path = alternative_path
        self._portal = portal
        self._platform = platform

        self._neighbours = {key: None for key in [N, E, S, W, NW, NE, SW, SE]}

        self._active_path = "main"

        self._font = pg.font.SysFont("Verdana", 30)

        self._main_path_points = [(0, self._PATH_CHAR_TO_COORDS[self._main_path[0]]),
                                  (TILE_LENGTH / 2 - 1, TILE_LENGTH / 2 - 1),
                                  (TILE_LENGTH - 1, self._PATH_CHAR_TO_COORDS[self._main_path[1]])]
        if self._alt_path:
            self._alt_path_points = [(0, self._PATH_CHAR_TO_COORDS[self._alt_path[0]]),
                                     (TILE_LENGTH / 2 - 1, TILE_LENGTH / 2 - 1),
                                     (TILE_LENGTH - 1, self._PATH_CHAR_TO_COORDS[self._alt_path[1]])]
        else:
            self._alt_path_points = list()

        self.image = pg.Surface((TILE_LENGTH, TILE_LENGTH))
        self._update_image()

    def switch_track(self):
        # Switch track if tile has more than one track
        if self._alt_path:
            if self._active_path == "main":
                self._active_path = "alt"
            elif self._active_path == "alt":
                self._active_path = "main"
            self._update_image()

    def get_trajectory(self) -> list[Vector2]:
        # Give list of points corresponding to the current track configuration
        trajectory = list()

        current_path = str()
        if self._active_path == "main":
            current_path = self._main_path
        elif self._active_path == "alt":
            current_path = self._alt_path

        if current_path[0] == "u":
            trajectory += [self._position + Vector2(i, i) for i in range(16)]
        elif current_path[0] == "m":
            trajectory += [self._position + Vector2(i, 15) for i in range(16)]
        elif current_path[0] == "d":
            trajectory += [self._position + Vector2(i, 31 - i) for i in range(16)]

        if current_path[1] == "u":
            trajectory += [self._position + Vector2(16 + i, 15 - i) for i in range(16)]
        elif current_path[1] == "m":
            trajectory += [self._position + Vector2(16 + i, 15) for i in range(16)]
        elif current_path[1] == "d":
            trajectory += [self._position + Vector2(16 + i, 16 + i) for i in range(16)]

        return trajectory

    def set_neighbour(self, compass_direction: str, tile: "TrackTile"):
        self._neighbours[compass_direction] = tile

    def get_neighbour(self, compass_direction: str) -> "TrackTile":
        return self._neighbours[compass_direction]

    def _update_image(self):
        # Portals and platforms have specific background text and colors
        if self._portal is not None:
            self.image.fill(pg.Color("lightblue"))
            text = self._font.render(self._portal, True, pg.Color("darkblue"))
            self.image.blit(text, (3, 1))
        elif self._platform is not None:
            self.image.fill(pg.Color("lightgreen"))
            text = self._font.render(self._platform, True, pg.Color("darkgreen"))
            self.image.blit(text, (6, 1))
        else:
            self.image.fill(pg.Color("white"))

        # Draw inactive path in grey
        tmp_tile = pg.surface.Surface((TILE_LENGTH, TILE_LENGTH), pg.SRCALPHA)
        if self._active_path == "alt":
            tmp_tile = pg.image.load(f"assets/tiles/{self._main_path}.png").convert_alpha()
        elif self._active_path == "main" and self._alt_path:
            tmp_tile = pg.image.load(f"assets/tiles/{self._alt_path}.png").convert_alpha()
        tmp_tile.set_alpha(128)
        self.image.blit(tmp_tile, (0, 0))

        # Draw active path in black
        if self._active_path == "main":
            tmp_tile = pg.image.load(f"assets/tiles/{self._main_path}.png").convert_alpha()
        elif self._active_path == "alt" and self._alt_path:
            tmp_tile = pg.image.load(f"assets/tiles/{self._alt_path}.png").convert_alpha()
        self.image.blit(tmp_tile, (0, 0))

        if DEBUG:
            # Draw trajectory in red on top (debug)
            for point in self.get_trajectory():
                self.image.fill(pg.Color("lightcoral"), (point - self._position, (1, 1)))

            # Draw limits in red on top (debug)
            pg.draw.rect(self.image, pg.Color("lightcoral"), self.image.get_rect(), 1)

        self.rect = self.image.get_rect()
        self.rect.x = self._position[0]
        self.rect.y = self._position[1]

    @property
    def portal(self) -> str:
        return self._portal

    @property
    def platform(self) -> str:
        return self._platform
