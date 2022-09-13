# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pygame as pg

# import your own module
import pygame.time

from tracktile import TrackTile
from constants import TILE_LENGTH
from map import Map

global TILE_LENGTH

class Game:
    """
    Game class.
    """

    FPS = 30
    SCREEN_WIDTH = 768
    SCREEN_HEIGHT = 400
    TILE_LENGTH = 32

    def __init__(self):
        pg.init()
        self.screen = None
        self.running = False
        self.clock = None

    def run(self):
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pg.display.set_caption("Track Switching Game")

        # Initializing game entities
        map = Map()

        # Initializing game clock
        self.clock = pygame.time.Clock()

        # Ready to go
        self.running = True

        # Game loop
        while self.running:
            map.update()

            self.handle_events()

            self.screen.fill(pg.Color("white"))
            map.draw(self.screen)
            pg.display.update()

            self.clock.tick(self.FPS)

        # Game loop is over
        self.quit()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def quit(self):
        pg.quit()
