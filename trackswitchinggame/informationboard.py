# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pygame as pg
from pygame.math import Vector2

# import your own module
from trackswitchinggame.constants import *


class InformationBoard(pg.surface.Surface):
    """
    Handles the board containing all information of current and upcoming trains.
    """

    def __init__(self, width, nb_trains, trains, **kwargs):
        height = (nb_trains + 1) * TILE_LENGTH
        super().__init__((width, height), **kwargs)

        self.trains = trains

        self.title_font = pg.font.SysFont("Verdana", 30)
        self.title_font.bold = True
        self.table_header_font = pg.font.SysFont("Verdana", 25)
        self.table_content_font = pg.font.SysFont("Verdana", 20)

    def update(self):
        self.fill(pg.Color("darkblue"))

        # Title line
        title_offset = Vector2(2, 2)
        self.blit(self.title_font.render("Upcoming trains", True, pg.Color("white")),
                  title_offset)
        self.blit(self.table_header_font.render(str(int(pg.time.get_ticks()/1000)), True, pg.Color("white")),
                  title_offset + Vector2(12*TILE_LENGTH, 0))

        # Table header
        table_header_offset = title_offset + Vector2(0, 32)
        self.blit(self.table_header_font.render("Time", True, pg.Color("white")),
                  table_header_offset + Vector2(0, 0))
        self.blit(self.table_header_font.render("Train", True, pg.Color("white")),
                  table_header_offset + Vector2(2 * TILE_LENGTH, 0))
        self.blit(self.table_header_font.render("From", True, pg.Color("white")),
                  table_header_offset + Vector2(4 * TILE_LENGTH, 0))
        self.blit(self.table_header_font.render("Platform", True, pg.Color("white")),
                  table_header_offset + Vector2(6 * TILE_LENGTH, 0))
        self.blit(self.table_header_font.render("To", True, pg.Color("white")),
                  table_header_offset + Vector2(10 * TILE_LENGTH, 0))

        # Table rows (one row per train)
        rows_offset = table_header_offset + Vector2(0, 32)
        for train in self.trains:
            self.blit(train.wagons.sprites()[0].original_image, rows_offset + Vector2(2 * TILE_LENGTH, 0))
            # for instr in train._instructions:
            #     if isinstance(instr, SpawnInstruction):
            #         self.blit(self.table_content_font.render(str(int(instr.spawn_time/1000)), True, pg.Color("white")),
            #                   rows_offset)
            #
            #         self.blit(self.table_content_font.render(instr.spawn_portal, True, pg.Color("white")),
            #                   rows_offset + Vector2(4 * TILE_LENGTH, 0))
            #         if instr.is_completed:
            #             self.blit(self.table_content_font.render("o", True, pg.Color("green")),
            #                       rows_offset + Vector2(4.5 * TILE_LENGTH, 0))
            #         else:
            #             self.blit(self.table_content_font.render("x", True, pg.Color("red")),
            #                       rows_offset + Vector2(4.5 * TILE_LENGTH, 0))
            #
            #     if isinstance(instr, WaitAtPlatformInstruction):
            #         self.blit(self.table_content_font.render(instr.target_platform, True, pg.Color("white")),
            #                   rows_offset + Vector2(6 * TILE_LENGTH, 0))
            #         if instr.is_completed:
            #             self.blit(self.table_content_font.render("o", True, pg.Color("green")),
            #                       rows_offset + Vector2(6.5 * TILE_LENGTH, 0))
            #         else:
            #             self.blit(self.table_content_font.render("x", True, pg.Color("red")),
            #                       rows_offset + Vector2(6.5 * TILE_LENGTH, 0))

            # for goal in train.goals:
            #     if isinstance(goal, ExitPortalGoal):
            #         self.blit(self.table_content_font.render(goal.target_portal, True, pg.Color("white")),
            #                   rows_offset + Vector2(10 * TILE_LENGTH, 0))
            #         if goal.is_achieved:
            #             self.blit(self.table_content_font.render("o", True, pg.Color("green")),
            #                       rows_offset + Vector2(10.5 * TILE_LENGTH, 0))
            #         else:
            #             self.blit(self.table_content_font.render("x", True, pg.Color("red")),
            #                       rows_offset + Vector2(10.5 * TILE_LENGTH, 0))
            rows_offset += Vector2(0, 32)

    def draw(self, surface, position):
        surface.blit(self, position)
