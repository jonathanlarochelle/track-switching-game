# -*- coding: utf-8 -*-

# import built-in module
import random

# import third-party modules
import pygame as pg
from pygame.math import Vector2

# import your own module
from trackswitchinggame.constants import *
from trackswitchinggame.map import Map
from trackswitchinggame.train import Train
from trackswitchinggame.informationboard import InformationBoard


class Game:
    """
    Game class. Start the game with the run() method.
    """

    FPS = 30
    SCREEN_WIDTH = 27 * TILE_LENGTH
    # SCREEN_HEIGHT = (8 + 6) * TILE_LENGTH
    SCREEN_HEIGHT = 8 * TILE_LENGTH

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
        self.trains = []
        self._spawn_new_train()

        # Initializing game clock
        self.clock = pg.time.Clock()

        # Initializing information board
        # self.info_board = InformationBoard(self.SCREEN_WIDTH, 5, self.trains)
        self.score = 0

        # Ready to go
        self.running = True

        # Game loop
        while self.running:
            # Update
            self._update_trains()
            # self.info_board.update()

            # User events
            self._handle_events()

            # Re-draw screen
            self.screen.fill(pg.Color("white"))
            self.map.draw(self.screen)
            for train in self.trains:
                train.draw(self.screen)
            # self.info_board.draw(self.screen, (0, 8*TILE_LENGTH))
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
                # for train in self.trains:
                #     if train.rect.collidepoint(mouse_position):
                #         if train.moving:
                #             train.stop()
                #         else:
                #             train.start(train.direction)

                # Clicking on tile switches the track, if no train is currently on it.
                clicked_tile = self.map.tile_at(Vector2(mouse_position))
                if clicked_tile:
                    # Not colliding with train.rect here because for some reason the rect overlaps to next tile when
                    # train is not yet on it (sometimes).
                    # TODO: Correct this.
                    for train in self.trains:
                        if train.spawned:
                            point_1 = train.trajectory[train.rightmost_position_pointer]
                            point_2 = train.trajectory[train.leftmost_position_pointer]
                            if clicked_tile.rect.collidepoint(point_1) or clicked_tile.rect.collidepoint(point_2):
                                break
                    else:
                        clicked_tile.switch_track()

    def _update_trains(self):
        """
        Handles all updates for trains:
        - spawn new trains
        - calls .update() for all trains
        - handles despawning and score counting
        """
        # Spawn new train
        if pg.time.get_ticks() > self._last_train_spawned + 15000:
            self._spawn_new_train()

        for train in self.trains:
            if train.spawned:
                # Despawn trains outside of playing field
                if not train.platform_status == PENDING and not train.exit_portal_status == PENDING:
                    if not train.rect.colliderect(self.map.get_playing_field_rect()):
                        train.despawn()
                        if train.platform_status == SUCCEEDED:
                            self.score += 1
                        if train.exit_portal_status == SUCCEEDED:
                            self.score += 1
                        print(f"Score: {self.score}")

                # Check for collisions

                # Update
                train.update()

    def _spawn_new_train(self):
        """
        Spawns a new randomly-generated train if the time increment has been reached.
        """
        # Randomly generate a entry portal, a platform, and an exit portal for a train, with the following rules:
        # Entry portal should not be the exit portal for any train currently generated
        # Target platform should not be a platform TO BE reached for any current train.

        legal_entry_portals = self.map.input_portals
        legal_platforms = list(self.map.platforms.keys())
        legal_exit_portals = self.map.output_portals
        legal_palettes = {"ICE": [3]}

        for train in self.trains:
            if train.spawned:
                if train.exit_portal in legal_entry_portals:
                    legal_entry_portals.remove(train.exit_portal)
                if train.platform in legal_platforms and \
                        train.platform_status == PENDING and \
                        train.moving:
                    legal_platforms.remove(train.platform)

        platform = random.choice(legal_platforms)
        entry_portal = random.choice(list(set(legal_entry_portals) &
                                          set(self.map.platforms_connecting_portals[platform])))
        exit_portal = random.choice(list(set(legal_exit_portals) &
                                         set(self.map.platforms_connecting_portals[platform])))
        palette = random.choice(list(legal_palettes.keys()))
        nb_wagons = random.choice(legal_palettes[palette])

        new_train = Train(self.map, entry_portal, platform, exit_portal,
                          nb_wagons, palette)
        new_train.spawn()
        self.trains.append(new_train)
        self._last_train_spawned = pg.time.get_ticks()


    def quit(self):
        """
        Clean-up and quit the game.
        """
        pg.quit()
