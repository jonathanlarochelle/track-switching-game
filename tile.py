# -*- coding: utf-8 -*-

# import built-in module
import pygame.sprite
import pygame.image
import pygame.draw

# import third-party modules

# import your own module
from constants import TILE_LENGTH


class Tile(pygame.sprite.Sprite):
    """
    Represents a tile on the game map.
    """

    EDGE_POINTS_COORDS = {1: (0, 0),
                          2: ((TILE_LENGTH / 2) - 1, 0),
                          3: (TILE_LENGTH - 1, 0),
                          4: (TILE_LENGTH - 1, (TILE_LENGTH / 2) - 1),
                          5: (TILE_LENGTH - 1, TILE_LENGTH - 1),
                          6: ((TILE_LENGTH / 2) - 1, TILE_LENGTH - 1),
                          7: (0, TILE_LENGTH - 1),
                          8: (0, (TILE_LENGTH / 2) - 1)}

    def __init__(self, path: tuple[int]):
        # Path is a tuple of the entry and output ports (1,2)
        #  1     2   3
        #   _________
        #   |       |
        # 8 |       |  4
        #   |       |
        #   ---------
        #  7   6     5
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.path = path

        # Draw track based on specified path
        self.image = pygame.Surface((TILE_LENGTH, TILE_LENGTH))
        self.image.fill(pygame.Color("green"))
        pygame.draw.line(self.image, color=pygame.Color("black"),
                         start_pos=self.EDGE_POINTS_COORDS[path[0]],
                         end_pos=(int(TILE_LENGTH / 2) - 1, int(TILE_LENGTH / 2) - 1), width=4)
        pygame.draw.line(self.image, color=pygame.Color("black"),
                         start_pos=(int(TILE_LENGTH / 2) - 1, int(TILE_LENGTH / 2) - 1),
                         end_pos=self.EDGE_POINTS_COORDS[path[1]], width=4)

        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10
