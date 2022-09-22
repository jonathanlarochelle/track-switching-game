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

    PATH_CHAR_TO_COORDS = {"u": 0,
                           "m": (TILE_LENGTH / 2) - 1,
                           "d": TILE_LENGTH - 1}

    def __init__(self, pos: tuple, main_path: str, alternative_path: str = None, portal: str = None,
                 platform: str = None, *groups: pg.sprite.AbstractGroup):
        super().__init__(*groups)
        self.position = pos
        self.main_path = main_path
        self.alt_path = alternative_path
        self.portal = portal
        self.platform = platform

        self._neighbours = {key: None for key in [N, E, S, W, NW, NE, SW, SE]}

        self.active_path = "main"

        self._font = pg.font.SysFont("Verdana", 30)

        self._main_path_points = [(0, self.PATH_CHAR_TO_COORDS[self.main_path[0]]),
                                  (TILE_LENGTH / 2 - 1, TILE_LENGTH / 2 - 1),
                                  (TILE_LENGTH - 1, self.PATH_CHAR_TO_COORDS[self.main_path[1]])]
        if self.alt_path:
            self._alt_path_points = [(0, self.PATH_CHAR_TO_COORDS[self.alt_path[0]]),
                                     (TILE_LENGTH / 2 - 1, TILE_LENGTH / 2 - 1),
                                     (TILE_LENGTH - 1, self.PATH_CHAR_TO_COORDS[self.alt_path[1]])]
        else:
            self._alt_path_points = list()

        self.image = pg.Surface((TILE_LENGTH, TILE_LENGTH))
        self._update_image()

    def switch_track(self):
        # Switch track if tile has more than one track
        if self.alt_path:
            if self.active_path == "main":
                self.active_path = "alt"
            elif self.active_path == "alt":
                self.active_path = "main"
            self._update_image()

    def get_trajectory(self) -> list[Vector2]:
        # Give list of points corresponding to the current track configuration
        trajectory = list()

        partial_traj_diagonal_going_down = [Vector2(i, i) for i in range(16)]
        partial_traj_diagonal_going_up = [Vector2(i, 15-i) for i in range(16)]
        partial_traj_straight = [Vector2(i, 0) for i in range(16)]

        current_path = str()
        if self.active_path == "main":
            current_path = self.main_path
        elif self.active_path == "alt":
            current_path = self.alt_path

        if current_path[0] == "u":
            trajectory += [self.position + Vector2(i, i) for i in range(16)]
        elif current_path[0] == "m":
            trajectory += [self.position + Vector2(i, 15) for i in range(16)]
        elif current_path[0] == "d":
            trajectory += [self.position + Vector2(i, 31-i) for i in range(16)]

        if current_path[1] == "u":
            trajectory += [self.position + Vector2(16+i, 15-i) for i in range(16)]
        elif current_path[1] == "m":
            trajectory += [self.position + Vector2(16+i, 15) for i in range(16)]
        elif current_path[1] == "d":
            trajectory += [self.position + Vector2(16+i, 16+i) for i in range(16)]

        return trajectory

    def _update_image(self):
        # Portals and platforms have specific background text and colors
        if self.portal is not None:
            self.image.fill(pg.Color("blue"))
            text = self._font.render(self.portal, True, pg.Color("darkblue"))
            self.image.blit(text, (3, 1))
        elif self.platform is not None:
            self.image.fill(pg.Color("green"))
            text = self._font.render(self.platform, True, pg.Color("darkgreen"))
            self.image.blit(text, (6, 1))
        else:
            self.image.fill(pg.Color("white"))

        # Draw inactive path in grey
        tmp_tile = pg.surface.Surface((TILE_LENGTH, TILE_LENGTH), pg.SRCALPHA)
        if self.active_path == "alt":
            tmp_tile = pg.image.load(f"assets/tiles/{self.main_path}.png").convert_alpha()
        elif self.active_path == "main" and self.alt_path:
            tmp_tile = pg.image.load(f"assets/tiles/{self.alt_path}.png").convert_alpha()
        tmp_tile.set_alpha(128)
        self.image.blit(tmp_tile, (0, 0))

        # Draw active path in black
        if self.active_path == "main":
            tmp_tile = pg.image.load(f"assets/tiles/{self.main_path}.png").convert_alpha()
        elif self.active_path == "alt" and self.alt_path:
            tmp_tile = pg.image.load(f"assets/tiles/{self.alt_path}.png").convert_alpha()
        self.image.blit(tmp_tile, (0, 0))

        # Draw trajectory in red on top (debug)
        for point in self.get_trajectory():
            self.image.fill(pg.Color("red"), (point - self.position, (1, 1)))

        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    def set_neighbour(self, compass_direction: str, tile: "TrackTile"):
        self._neighbours[compass_direction] = tile

    def get_neighbour(self, compass_direction: str):
        return self._neighbours[compass_direction]
