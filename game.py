# -*- coding: utf-8 -*-

# import built-in module
import math

# import third-party modules
import pygame as pg
from pygame.math import Vector2

# import your own module
from constants import TILE_LENGTH
from map import Map
from train import Train
from goal import PlatformGoal, ExitPortalGoal


class Game:
    """
    Game class. Start the game with the run() method.
    """

    FPS = 30
    SCREEN_WIDTH = 26 * TILE_LENGTH
    SCREEN_HEIGHT = 400

    def __init__(self):
        pg.init()
        self.screen = None
        self.running = False
        self.clock = None
        self.map = None
        self.trains = []

    def run(self):
        """
        Start the game.
        """
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), flags=pg.RESIZABLE | pg.SCALED)
        pg.display.set_caption("Track Switching Game")

        # Initializing game entities
        self.map = Map()
        self.trains.append(self._create_train("B", "3", "E"))
        # self.trains.append(self._create_train("D", "1", "A"))

        # Initializing game clock
        self.clock = pg.time.Clock()

        # Ready to go
        self.running = True

        # Game loop
        while self.running:
            # Update
            self._update_trajectory()
            for train in self.trains:
                train.update()
            self._check_for_despawn()

            # User events
            self._handle_events()

            # Re-draw screen
            self.screen.fill(pg.Color("white"))
            self.map.draw(self.screen)
            for train in self.trains:
                train.draw(self.screen)
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

    def _update_trajectory(self):
        """
        Monitors all trains's trajectory and associated pointers to 1) add trajectories from next tile and
        2) delete trajectory from previous tile.
        Note: These operations should be somewhere else, not sure where yet.
        """
        for train in self.trains:
            if train.moving and train.direction == "forward":
                if (train.rightmost_position_pointer + train.trajectory_pointer_increment) >= len(train.trajectory):
                    # We need to fetch trajectory information from next tile
                    train_vector = train.trajectory[-1] - train.trajectory[-2]
                    next_tile_position = train.trajectory[-1] + train_vector
                    next_tile = self.map.tile_at(next_tile_position)
                    if next_tile:
                        new_trajectory = next_tile.get_trajectory()
                        # Check if our entry point is valid for the next tile
                        if next_tile_position in new_trajectory:
                            train.trajectory += new_trajectory
                    else:
                        # No next tile, which means we are headed out of playing field.
                        # Padding with a straight trajectory for now.
                        last_point = train.trajectory[-1]
                        train.trajectory += [last_point + Vector2(i, 0) for i in range(TILE_LENGTH)]

                if (train.leftmost_position_pointer + train.trajectory_pointer_increment) >= TILE_LENGTH:
                    # We can delete trajectory information from last tile
                    train.trajectory = train.trajectory[TILE_LENGTH:]
                    train.rightmost_position_pointer -= TILE_LENGTH

            elif train.moving and train.direction == "backward":
                if (train.leftmost_position_pointer + train.trajectory_pointer_increment) < 0:
                    # We need to fetch trajectory information from previous tile
                    train_vector = train.trajectory[0] - train.trajectory[1]
                    next_tile_position = train.trajectory[0] + train_vector
                    next_tile = self.map.tile_at(next_tile_position)
                    if next_tile:
                        new_trajectory = self.map.tile_at(next_tile_position).get_trajectory()
                        # Check if our entry point is valid for the next tile
                        if next_tile_position in new_trajectory:
                            train.trajectory = new_trajectory + train.trajectory
                            train.rightmost_position_pointer += TILE_LENGTH
                    else:
                        # No next tile, which means we are headed out of playing field.
                        # Padding with a straight trajectory for now.
                        last_point = train.trajectory[0]
                        train.trajectory = [last_point + Vector2(-TILE_LENGTH+i, 0) for i in range(TILE_LENGTH)] + train.trajectory
                        train.rightmost_position_pointer += TILE_LENGTH

                if (train.rightmost_position_pointer + train.trajectory_pointer_increment) < (len(train.trajectory) - TILE_LENGTH):
                    # We can delete trajectory information from last tile
                    train.trajectory = train.trajectory[:-TILE_LENGTH]

    def _check_for_despawn(self):
        """
        Note: These operations should be somewhere else, not sure where yet.
        """
        for train in self.trains:
            if train.state == "spawned":
                if not self.screen.get_rect().colliderect(train.rect):
                    # Train is out of the game surface
                    train.despawn()

    def _create_train(self, portal: str, platform_goal: str, portal_goal: str) -> Train:
        """
        Temporary factory for Train()
        Note: These operations should be somewhere else, not sure where yet.
        """
        train = Train()
        train.goals.append(PlatformGoal(self, train, platform_goal))
        train.goals.append(ExitPortalGoal(self, train, portal_goal))
        spawn_tile = self.map.portals[portal].sprites()[0]
        tile_traj = spawn_tile.get_trajectory()

        # We pad the trajectory with "phantom" tiles to the left or right of the screen,
        # depending on where the train is coming from
        nb_padding_tiles = math.ceil(train.length / TILE_LENGTH)
        if portal in ["A", "B", "C"]:
            for i in range(nb_padding_tiles * TILE_LENGTH):
                train.trajectory.append(Vector2(-(nb_padding_tiles*TILE_LENGTH)+i, tile_traj[0].y))
            train.trajectory += tile_traj
            train.direction = "forward"
        elif portal in ["D", "E", "F", "G"]:
            train.trajectory += tile_traj
            for i in range(nb_padding_tiles * TILE_LENGTH):
                train.trajectory.append(Vector2(self.SCREEN_WIDTH + i, tile_traj[0].y))
            train.direction = "backward"
        train.spawn()
        return train

    def quit(self):
        """
        Clean-up and quit the game.
        """
        pg.quit()
