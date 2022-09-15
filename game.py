# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pygame as pg
import pygame.time
from pygame.math import Vector2

# import your own module
from tracktile import TrackTile
from constants import TILE_LENGTH
from map import Map
from train import Train


class Game:
    """
    Game class.
    """

    FPS = 30
    SCREEN_WIDTH = 24 * TILE_LENGTH
    SCREEN_HEIGHT = 400

    def __init__(self):
        pg.init()
        self.screen = None
        self.running = False
        self.clock = None

    def run(self):
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pg.display.set_caption("Track Switching Game")

        # Initializing game entities
        self.map = Map()
        self.train = self._create_train("D")

        # Initializing game clock
        self.clock = pygame.time.Clock()

        # Ready to go
        self.running = True

        # Game loop
        while self.running:
            # Update
            self.map.update()
            self._update_trajectory()
            self.train.update()

            # User events
            self._handle_events()

            # Re-draw screen
            self.screen.fill(pg.Color("white"))
            self.map.draw(self.screen)
            self.train.draw(self.screen)
            pg.display.update()

            self.clock.tick(self.FPS)

        # Game loop is over
        self.quit()

    def _handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = pg.mouse.get_pos()
                clicked_tile = self.map.tile_at(mouse_position)

                # Clicking on train toggles between start/stop
                if self.train.rect.collidepoint(mouse_position):
                    if self.train.moving:
                        self.train.stop()
                    else:
                        self.train.start(self.train.direction)

                # Clicking on tile switches the track, if no train is currently on it.
                elif clicked_tile:
                    # Not colliding with train.rect here because for some reason the rect overlaps to next tile when
                    # train is not yet on it (sometimes).
                    # TODO: Correct this.
                    if (not clicked_tile.rect.collidepoint(self.train.trajectory[self.train.nose_position_pointer])) \
                            and (not clicked_tile.rect.collidepoint(self.train.trajectory[self.train.tail_position_pointer])):
                        clicked_tile.switch_track()

    def _update_trajectory(self):
        """
        Monitors all trains's trajectory and associated pointers to 1) add trajectories from next tile and
        2) delete trajectory from previous tile.
        """
        if self.train.moving and self.train.direction == "forward":
            if (self.train.nose_position_pointer + self.train.trajectory_pointer_increment) >= len(self.train.trajectory):
                # We need to fetch trajectory information from next tile
                train_vector = self.train.trajectory[-1] - self.train.trajectory[-2]
                next_tile_position = self.train.trajectory[-1] + train_vector
                new_trajectory = self.map.tile_at(next_tile_position).get_trajectory()
                # Check if our entry point is valid for the next tile
                if next_tile_position in new_trajectory:
                    self.train.trajectory += new_trajectory

            if (self.train.tail_position_pointer + self.train.trajectory_pointer_increment) >= TILE_LENGTH:
                # We can delete trajectory information from last tile
                self.train.trajectory = self.train.trajectory[TILE_LENGTH:]
                self.train.nose_position_pointer -= TILE_LENGTH

        elif self.train.moving and self.train.direction == "backward":
            if (self.train.tail_position_pointer + self.train.trajectory_pointer_increment) < 0:
                # We need to fetch trajectory information from previous tile
                train_vector = self.train.trajectory[0] - self.train.trajectory[1]
                next_tile_position = self.train.trajectory[0] + train_vector
                new_trajectory = self.map.tile_at(next_tile_position).get_trajectory()
                # Check if our entry point is valid for the next tile
                if next_tile_position in new_trajectory:
                    self.train.trajectory = new_trajectory + self.train.trajectory
                    self.train.nose_position_pointer += TILE_LENGTH

            if (self.train.nose_position_pointer + self.train.trajectory_pointer_increment) < (len(self.train.trajectory) - TILE_LENGTH):
                # We can delete trajectory information from last tile
                self.train.trajectory = self.train.trajectory[:-TILE_LENGTH]

    def _create_train(self, portal: str) -> Train:
        """
        Temporary factory for Train()
        """
        train = Train()
        spawn_tile = self.map.portals[portal]
        tile_traj = spawn_tile.get_trajectory()
        if portal in ["A", "B", "C"]:
            for i in range(TILE_LENGTH):
                train.trajectory.append(Vector2(-31+i, tile_traj[0].y))
            train.start("forward")
        elif portal in ["D", "E", "F", "G"]:
            for i in range(TILE_LENGTH):
                train.trajectory.append(Vector2(self.SCREEN_WIDTH + i, tile_traj[0].y))
            train.start("backward")
            train.original_image = pg.transform.flip(train.original_image, True, False)

        return train

    def quit(self):
        pg.quit()
