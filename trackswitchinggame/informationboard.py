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

        self._font = pg.font.SysFont("Verdana", 30)
        self._bold_font = pg.font.SysFont("Verdana", 30)
        self._bold_font.bold = True

        self._score_label_text = self._bold_font.render("Score", True, pg.Color("white"))
        self._speed_label_text = self._bold_font.render("Speed", True, pg.Color("white"))
        self._game_over_text = self._bold_font.render("Game over!", True, pg.Color("red"))

    def update(self, level_name: str, score: int, speed: int, game_over: bool):
        self.fill(pg.Color("darkblue"))

        # Level name
        level_name_offset = Vector2(1, 1)
        level_name_text = self._font.render(level_name, True, pg.Color("white"))
        self.blit(level_name_text, level_name_offset)

        # Score
        score_offset = Vector2(level_name_text.get_rect().width, 0) + Vector2(TILE_LENGTH, 1)
        self.blit(self._score_label_text, score_offset)
        score_text = self._font.render(str(score), True, pg.Color("white"))
        score_text_position = score_offset + Vector2(self._score_label_text.get_rect().width, 0) + Vector2(5, 0)
        self.blit(score_text, score_text_position)

        # Speed
        speed_offset = score_offset + Vector2(5*TILE_LENGTH, 0)
        self.blit(self._speed_label_text, speed_offset)
        speed_text = self._font.render(str(speed), True, pg.Color("white"))
        speed_text_position = speed_offset + Vector2(self._speed_label_text.get_rect().width, 0) + Vector2(5, 0)
        self.blit(speed_text, speed_text_position)

        # Game over text
        game_over_offset = speed_offset + Vector2(5*TILE_LENGTH, 0)
        if game_over:
            self.blit(self._game_over_text, game_over_offset)


    def draw(self, surface, position):
        surface.blit(self, position)
