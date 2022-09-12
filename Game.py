# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pygame

# import your own module


class Game:
    """
    Game class.
    """

    FPS = 30
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 400

    def __init__(self):
        pygame.init()
        self.SCREEN = None
        self.running = False

    def run(self):
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Track Switching Game")
        self.running = True

        # Game loop
        while(self.running):
            self.handle_events()

        # Game loop is over
        self.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def quit(self):
        pygame.quit()
