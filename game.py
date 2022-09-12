# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pygame as pg

# import your own module
from tracktile import TrackTile
from constants import TILE_LENGTH

global TILE_LENGTH

class Game:
    """
    Game class.
    """

    FPS = 30
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 400
    TILE_LENGTH = 32

    def __init__(self):
        pg.init()
        self.screen = None
        self.running = False

    def run(self):
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pg.display.set_caption("Track Switching Game")

        # Set-up groups
        tiles = pg.sprite.Group()
        all = pg.sprite.Group()

        TrackTile.containers = all, tiles

        TrackTile((1, 3), "mm", "md")
        TrackTile((1, 3+TILE_LENGTH), "mu", "md")

        self.running = True

        # Game loop
        while self.running:
            all.update()

            self.handle_events()

            self.screen.fill(pg.Color("white"))
            all.draw(self.screen)
            pg.display.update()

        # Game loop is over
        self.quit()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def quit(self):
        pg.quit()
