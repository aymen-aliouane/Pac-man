from states.game_states import GameState
from components.game import Settings
from initialise.init_game import init_game
import pygame
import pygame.freetype
import sys


class GameEngine:
    def __init__(self, file_path: str):
        self.path = file_path
        self.game = None
        self.main_layer = None
        self.clock = pygame.time.Clock()
        self.running = False
        self.screen = None

    def initialize(self):
        # initialize pygame
        pygame.init()
        pygame.display.set_caption("Pac-man")

        # create the game object
        self.game = init_game(self.path)

        # create the main layer
        self.game.state = GameState()
        self.screen = pygame.display.set_mode((self.game.display.width, self.game.display.height))
        self.main_layer = self.screen


    def run(self):
        self.initialize()


        self.running = True

        while self.running:
            # clock.tick() return the time in ms
            # between this frame and the last frame
            dt = self.clock.tick(self.game.settings.fps) / 1000

            # game.state is the state of the player, it can be Game, Menu or Pause
            # based on that it will handle input differently, but all of thems return
            # True if the user ask to quit
            end = self.game.state.handle_input(pygame.event.get(), self.game)
            if end:
                break

            self.game.state.update(self.game, dt)

            self.game.state.render(self.game, self.main_layer)

            # update screen to user
            pygame.display.flip()

        # quit cleanly
        pygame.quit()

