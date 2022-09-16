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
        self.map = None
        self.trains = []

    def run(self):
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), flags=pg.RESIZABLE | pg.SCALED)
        pg.display.set_caption("Track Switching Game")

        # Initializing game entities
        self.map = Map()
        self.trains.append(self._create_train("B"))
        self.trains.append(self._create_train("D"))

        # Initializing game clock
        self.clock = pygame.time.Clock()

        # Ready to go
        self.running = True

        # Game loop
        while self.running:
            # Update
            self.map.update()
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
                        point_1 = train.trajectory[train.nose_position_pointer]
                        point_2 = train.trajectory[train.tail_position_pointer]
                        if clicked_tile.rect.collidepoint(point_1) or clicked_tile.rect.collidepoint(point_2):
                            break
                    else:
                        clicked_tile.switch_track()

    def _update_trajectory(self):
        """
        Monitors all trains's trajectory and associated pointers to 1) add trajectories from next tile and
        2) delete trajectory from previous tile.
        """
        for train in self.trains:
            if train.moving and train.direction == "forward":
                if (train.nose_position_pointer + train.trajectory_pointer_increment) >= len(train.trajectory):
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

                if (train.tail_position_pointer + train.trajectory_pointer_increment) >= TILE_LENGTH:
                    # We can delete trajectory information from last tile
                    train.trajectory = train.trajectory[TILE_LENGTH:]
                    train.nose_position_pointer -= TILE_LENGTH

            elif train.moving and train.direction == "backward":
                if (train.tail_position_pointer + train.trajectory_pointer_increment) < 0:
                    # We need to fetch trajectory information from previous tile
                    train_vector = train.trajectory[0] - train.trajectory[1]
                    next_tile_position = train.trajectory[0] + train_vector
                    next_tile = self.map.tile_at(next_tile_position)
                    if next_tile:
                        new_trajectory = self.map.tile_at(next_tile_position).get_trajectory()
                        # Check if our entry point is valid for the next tile
                        if next_tile_position in new_trajectory:
                            train.trajectory = new_trajectory + train.trajectory
                            train.nose_position_pointer += TILE_LENGTH
                    else:
                        # No next tile, which means we are headed out of playing field.
                        # Padding with a straight trajectory for now.
                        last_point = train.trajectory[0]
                        train.trajectory = [last_point + Vector2(-TILE_LENGTH+i, 0) for i in range(TILE_LENGTH)] + train.trajectory
                        train.nose_position_pointer += TILE_LENGTH

                if (train.nose_position_pointer + train.trajectory_pointer_increment) < (len(train.trajectory) - TILE_LENGTH):
                    # We can delete trajectory information from last tile
                    train.trajectory = train.trajectory[:-TILE_LENGTH]

    def _check_for_despawn(self):
        for train in self.trains:
            if train.state == "spawned":
                if not self.screen.get_rect().colliderect(train.rect):
                    # Train is out of the game surface
                    train.despawn()

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
            train.trajectory += tile_traj
            train.direction = "forward"
            train.nose_position_pointer = 32
        elif portal in ["D", "E", "F", "G"]:
            train.trajectory += tile_traj
            for i in range(TILE_LENGTH):
                train.trajectory.append(Vector2(self.SCREEN_WIDTH + i, tile_traj[0].y))
            train.direction = "backward"
            train.original_image = pg.transform.flip(train.original_image, True, False)
            train.tail_position_pointer = 31
        train.spawn()
        return train

    def quit(self):
        pg.quit()
