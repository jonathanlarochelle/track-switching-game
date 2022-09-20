# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pygame as pg
from pygame.math import Vector2

# import your own module
from trackswitchinggame.constants import TILE_LENGTH
from trackswitchinggame.map import Map
from trackswitchinggame.train import Train
from trackswitchinggame.informationboard import InformationBoard
import trackswitchinggame.instruction as instruction


class Game:
    """
    Game class. Start the game with the run() method.
    """

    FPS = 30
    SCREEN_WIDTH = 26 * TILE_LENGTH
    SCREEN_HEIGHT = (8 + 6) * TILE_LENGTH

    def __init__(self):
        pg.init()
        self.screen = None
        self.running = False
        self.clock = None
        self.map = None
        self.trains = []
        self.info_board = None

    def run(self):
        """
        Start the game.
        """
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), flags=pg.RESIZABLE | pg.SCALED)
        pg.display.set_caption("Track Switching Game")

        # Initializing game entities
        self.map = Map()
        self._init_trains()

        # Initializing game clock
        self.clock = pg.time.Clock()

        # Initializing information board
        self.info_board = InformationBoard(self.SCREEN_WIDTH, 5, self.trains)

        # Ready to go
        self.running = True

        # Game loop
        while self.running:
            # Update
            for train in self.trains:
                train.update()
            self.info_board.update()

            # User events
            self._handle_events()

            # Re-draw screen
            self.screen.fill(pg.Color("white"))
            self.map.draw(self.screen)
            for train in self.trains:
                train.draw(self.screen)
            self.info_board.draw(self.screen, (0, len(self.map.tiles_array)*TILE_LENGTH))
            pg.display.update()

            self.clock.tick(self.FPS)

        # Game loop is over
        self.quit()

    def _handle_events(self):
        """
        Handle user events
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = pg.mouse.get_pos()

                # Clicking on train toggles between start/stop
                for train in self.trains:
                    if train.rect.collidepoint(mouse_position):
                        if train.moving:
                            train.stop()
                        else:
                            train.start(train.direction)

                # Clicking on tile switches the track, if no train is currently on it.
                clicked_tile = self.map.tile_at(mouse_position)
                if clicked_tile:
                    # Not colliding with train.rect here because for some reason the rect overlaps to next tile when
                    # train is not yet on it (sometimes).
                    # TODO: Correct this.
                    for train in self.trains:
                        point_1 = train.trajectory[train.rightmost_position_pointer]
                        point_2 = train.trajectory[train.leftmost_position_pointer]
                        if clicked_tile.rect.collidepoint(point_1) or clicked_tile.rect.collidepoint(point_2):
                            break
                    else:
                        clicked_tile.switch_track()

    def _init_trains(self):
        """
        Temporary factory to create all trains in the level.
        """

        # Train 1: B > 3 > E
        train = Train("1", self.map)
        train.add_instruction(instruction.create_spawn_instruction(train, self.map.portals["B"].sprites()[0], 2000))
        train.add_instruction(instruction.create_platform_instruction(train, self.map.platforms["3"], 3000))
        train.add_instruction(instruction.create_despawn_instruction(train, self.map.tiles))
        self.trains.append(train)

        # Train 2: D > 1 > A
        train = Train("2", self.map)
        train.add_instruction(instruction.create_spawn_instruction(train, self.map.portals["D"].sprites()[0], 10000))
        train.add_instruction(instruction.create_platform_instruction(train, self.map.platforms["1"], 3000))
        train.add_instruction(instruction.create_despawn_instruction(train, self.map.tiles))
        self.trains.append(train)

    def quit(self):
        """
        Clean-up and quit the game.
        """
        pg.quit()
