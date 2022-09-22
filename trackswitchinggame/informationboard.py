# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pygame as pg
from pygame.math import Vector2

# import your own module
from trackswitchinggame.constants import *


class InformationBoard(pg.surface.Surface):
    """
    Handles the board containing score, etc.
    """

    def __init__(self, width, **kwargs):
        height = TILE_LENGTH
        super().__init__((width, height), **kwargs)

        self.font = pg.font.SysFont("Verdana", 30)
        self.bold_font = pg.font.SysFont("Verdana", 30)
        self.bold_font.bold = True

        self.score_label_text = self.bold_font.render("Score", True, pg.Color("white"))
        self.speed_label_text = self.bold_font.render("Speed", True, pg.Color("white"))

    def update(self, score: int, speed: int):
        self.fill(pg.Color("darkblue"))

        # Score
        score_offset = Vector2(1, 1)
        self.blit(self.score_label_text, score_offset)
        score_text = self.font.render(str(score), True, pg.Color("white"))
        score_text_position = score_offset + Vector2(self.score_label_text.get_rect().width, 0) + Vector2(5, 0)
        self.blit(score_text, score_text_position)

        # Speed
        speed_offset = Vector2(5*TILE_LENGTH, 1)
        self.blit(self.speed_label_text, Vector2(5 * TILE_LENGTH, 2))
        speed_text = self.font.render(str(speed), True, pg.Color("white"))
        speed_text_position = speed_offset + Vector2(self.speed_label_text.get_rect().width, 0) + Vector2(5, 0)
        self.blit(speed_text, speed_text_position)

    def draw(self, surface, position):
        surface.blit(self, position)
