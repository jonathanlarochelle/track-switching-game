# -*- coding: utf-8 -*-

# import built-in module
from enum import Enum

# import third-party modules

# import your own module

"""
Constants shared by all modules of the application.
"""

TILE_LENGTH = 32


class Compass(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"
    NW = "NW"
    NE = "NE"
    SW = "SW"
    SE = "SE"
