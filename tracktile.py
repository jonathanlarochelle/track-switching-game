# -*- coding: utf-8 -*-

# import built-in module
import pygame.sprite
import pygame.image
import pygame.draw

# import third-party modules

# import your own module
from constants import TILE_LENGTH


class TrackTile(pygame.sprite.Sprite):
    """
    Represents a tile on the game map.
    """

    position: tuple[float]
    main_path: str
    alt_path: str
    portal: str
    platform: str

    active_path: str

    PATH_CHAR_TO_COORDS = {"u": 0,
                           "m": (TILE_LENGTH / 2) - 1,
                           "d": TILE_LENGTH - 1}

    def __init__(self, pos: tuple[float], main_path: str, alternative_path: str = None, portal: str = None,
                 platform: str = None):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.position = pos
        self.main_path = main_path
        self.alt_path = alternative_path
        self.portal = portal
        self.platform = platform

        self.active_path = "main"

        self._main_path_points = [(0, self.PATH_CHAR_TO_COORDS[self.main_path[0]]),
                                  (TILE_LENGTH / 2 - 1, TILE_LENGTH / 2 - 1),
                                  (TILE_LENGTH - 1, self.PATH_CHAR_TO_COORDS[self.main_path[1]])]
        if self.alt_path:
            self._alt_path_points = [(0, self.PATH_CHAR_TO_COORDS[self.alt_path[0]]),
                                     (TILE_LENGTH / 2 - 1, TILE_LENGTH / 2 - 1),
                                     (TILE_LENGTH - 1, self.PATH_CHAR_TO_COORDS[self.alt_path[1]])]
        else:
            self._alt_path_points = list()

        self.image = pygame.Surface((TILE_LENGTH, TILE_LENGTH))
        self._update_image()

    def _update_image(self):
        # Draw track based on current active exit
        self.image.fill(pygame.Color("white"))

        # Draw inactive path in grey
        tmp_tile = pygame.surface.Surface((TILE_LENGTH, TILE_LENGTH))
        if self.active_path == "alt":
            tmp_tile = pygame.image.load(f"assets/tiles/{self.main_path}.png").convert_alpha()
        elif self.active_path == "main" and self.alt_path:
            tmp_tile = pygame.image.load(f"assets/tiles/{self.alt_path}.png").convert_alpha()
        tmp_tile.set_alpha(128)
        self.image.blit(tmp_tile, (0, 0))

        # Draw inactive path in grey
        if self.active_path == "main":
            tmp_tile = pygame.image.load(f"assets/tiles/{self.main_path}.png").convert_alpha()
        elif self.active_path == "alt" and self.alt_path:
            tmp_tile = pygame.image.load(f"assets/tiles/{self.alt_path}.png").convert_alpha()
        tmp_tile.set_alpha(256)
        self.image.blit(tmp_tile, (0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]