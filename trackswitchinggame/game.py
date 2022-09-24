# -*- coding: utf-8 -*-

# import built-in module
import random
import json

# import third-party modules
import pygame as pg
from pygame.math import Vector2

# import your own module
from trackswitchinggame.constants import *
from trackswitchinggame.levelmap import LevelMap
from trackswitchinggame.train import Train
from trackswitchinggame.informationboard import InformationBoard


class Game:
    """
    Game class. Start the game with the run() method.
    """

    # Speed & amount of trains
    # Score | Nb of trains | Speed
    # 0       1-2            1
    # 6       3              1
    # 12      4              1
    # 18      5              1
    # 25      1-2            2
    # ...

    FPS = 30

    # Average time on screen of each trains will depend on the map size, but for now we do "one size fits all"
    GAME_PARAMETERS = {0: {"train_speed": 1, "min_time_between_spawn": 25000, "max_spawned_trains": 2, "platform_wait_delay": 3000, "portal_wait_delay": 5000},
                       2: {"train_speed": 1, "min_time_between_spawn": 15000, "max_spawned_trains": 3, "platform_wait_delay": 3000, "portal_wait_delay": 5000},
                       6: {"train_speed": 1, "min_time_between_spawn": 7000, "max_spawned_trains": 4, "platform_wait_delay": 3000, "portal_wait_delay": 5000},
                       10: {"train_speed": 1, "min_time_between_spawn": 1000, "max_spawned_trains": 5, "platform_wait_delay": 3000, "portal_wait_delay": 5000}}

    def __init__(self):
        pg.init()
        self.screen = None
        self.running = False
        self.clock = None
        self.map = None
        self.trains = []
        self.info_board = None
        self.score = 0
        self.SCREEN_WIDTH = None
        self.SCREEN_HEIGHT = None
        self.game_over = False
        self.game_parameters = self.GAME_PARAMETERS[0]
        self.nb_spawned_trains = 0

    def run(self, level_file: str):
        """
        Start the game.
        """
        # We look for the map's nb of cols and rows before loading it, because the loading operation (via the loading
        # of the tiles) requires the display video mode to be set.
        with open(level_file) as f:
            data = json.load(f)
            nb_rows = len(data["track_tiles"])
            nb_cols = len(data["track_tiles"][0])
        self.SCREEN_WIDTH = nb_cols * TILE_LENGTH
        self.SCREEN_HEIGHT = (nb_rows + 1) * TILE_LENGTH
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), flags=pg.RESIZABLE | pg.SCALED)
        pg.display.set_caption("Track Switching Game")

        # Initializing game entities
        self.map = LevelMap(level_file)
        self.trains = []
        self._spawn_new_train()

        # Initializing game clock
        self.clock = pg.time.Clock()

        # Initializing information board
        self.info_board = InformationBoard(self.SCREEN_WIDTH)
        self.score = 0

        # Ready to go
        self.running = True

        # Game loop
        while self.running:
            # User events
            self._handle_events()

            # Update
            self._update_game_progression()
            if not self.game_over:
                self._update_trains()
            self.info_board.update(self.map.level_name, self.score, self.game_parameters["train_speed"], self.game_over)

            # Re-draw screen
            self.screen.fill(pg.Color("white"))
            self.map.draw(self.screen)
            for train in self.trains:
                train.draw(self.screen)
            self.info_board.draw(self.screen, (0, 8*TILE_LENGTH))
            pg.display.update()

            self.clock.tick(self.FPS)

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

                # Clicking on tile switches the track, if no train is currently on it.
                clicked_tile = self.map.tile_at(Vector2(mouse_position))
                if clicked_tile:
                    for train in self.trains:
                        if train.colliderect(clicked_tile.rect):
                            break
                    else:
                        clicked_tile.switch_track()
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                # Debug key to break execution
                pass

    def _update_game_progression(self):
        """
        Update game progression based on current score.
        """
        new_game_parameters = None
        for score_threshold, game_parameters in self.GAME_PARAMETERS.items():
            if self.score < score_threshold:
                break
            else:
                new_game_parameters = game_parameters

        # If we have passed a new speed threshold.
        if new_game_parameters != self.game_parameters:
            self.game_parameters = new_game_parameters

    def _update_trains(self):
        """
        Handles all updates for trains:
        - spawn new trains
        - calls .update() for all trains
        - handles despawning and score counting
        """
        # Spawn new train if delay has passed and if nb of spawned trains is currently below the max. allowed number.
        if pg.time.get_ticks() > self._last_train_spawned + self.game_parameters["min_time_between_spawn"]:
            if self.nb_spawned_trains < self.game_parameters["max_spawned_trains"]:
                self._spawn_new_train()

        for train in self.trains:
            if train.spawned:
                # Despawn trains outside of playing field
                if not train.platform_status == PENDING and not train.exit_portal_status == PENDING:
                    if not train.rect.colliderect(self.map.get_playing_field_rect()):
                        train.despawn()
                        self.nb_spawned_trains -= 1
                        if train.platform_status == SUCCEEDED:
                            self.score += 1
                        if train.exit_portal_status == SUCCEEDED:
                            self.score += 1

                # Update
                train.update()

        # Check for collisions
        all_trajectory_points_list = []
        for train in self.trains:
            if train.spawned:
                new_trajectory_points = train.trajectory[train.leftmost_position_pointer:train.rightmost_position_pointer]
                for p in new_trajectory_points:
                    if p in all_trajectory_points_list:
                        self.game_over = True
                        break
                all_trajectory_points_list += new_trajectory_points
                if self.game_over:
                    break

    def _spawn_new_train(self):
        """
        Spawns a new randomly-generated train if the time increment has been reached.
        """
        # Randomly generate an entry portal, a platform, and an exit portal for a train, with the following rules:
        # Entry portal should not be the exit portal for any train currently generated
        # Target platform should not be a platform TO BE reached for any current train.

        legal_entry_portals = self.map.entry_portals
        legal_platforms = list(self.map.platforms.keys())
        legal_exit_portals = self.map.exit_portals

        platform = random.choice(legal_platforms)
        entry_portal = random.choice(list(set(legal_entry_portals) &
                                          set(self.map.platform_portal_connections[platform])))
        exit_portal = random.choice(list(set(legal_exit_portals) &
                                         set(self.map.platform_portal_connections[platform])))

        # If train is invalid, try again later.
        train_is_valid = True
        for train in self.trains:
            if train.spawned and train_is_valid:
                # If a train is still on the portal, do not spawn there.
                if train.entry_portal == entry_portal:
                    if train.colliderect(self.map.portals[train.entry_portal].sprites()[0].rect):
                        train_is_valid = False
                # If an existing train is headed to the portal, do not spawn there.
                if train.exit_portal == exit_portal:
                    train_is_valid = False
                # If an existing train is headed to the platform, do not select this platform.
                if train.platform == platform and train.platform_status == PENDING:
                    train_is_valid = False

        if train_is_valid:
            new_train = Train(self.map, entry_portal, self.game_parameters["portal_wait_delay"], platform,
                              self.game_parameters["platform_wait_delay"], exit_portal, self.game_parameters["train_speed"])
            new_train.spawn()
            self.trains.append(new_train)
            self._last_train_spawned = pg.time.get_ticks()
            self.nb_spawned_trains += 1

    def quit(self):
        """
        Clean-up and quit the game.
        """
        pg.quit()
