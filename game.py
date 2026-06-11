import pygame

from initialise.init_game import init_game
from states import GameState, MenuState, LostState, SaveScoreState


class GameEngine:
    def __init__(self, file_path: str) -> None:
        self.path = file_path
        self.game = init_game(self.path)
        self.main_layer = self.initialize()
        self.clock = pygame.time.Clock()
        self.running: bool = False

    def initialize(self) -> pygame.Surface:
        # initialize pygame
        pygame.init()
        pygame.display.set_caption("Pac-man")

        # initialize the starting state of the game
        # self.game.state = MenuState()
        self.game.state = SaveScoreState()

        # return the main layer
        return pygame.display.set_mode(
            (self.game.display.width, self.game.display.height)
        )

    def run(self) -> None:
        self.running = True

        while self.running:
            # clock.tick() return the time in ms
            # between this frame and the last frame
            dt = self.clock.tick(self.game.settings.fps) / 1000

            # game.state is the state of the player, it can be Game, Menu,
            # or Pause. Based on that it will handle input differently, but
            # all of them return True if the user asks to quit.
            end = self.game.state.handle_input(pygame.event.get(), self.game)
            if end:
                break

            self.game.state.update(self.game, dt)
            # print("state", self.game.state.__class__.__name__)

            self.game.state.render(self.game, self.main_layer)
            # print("rendered")
            # print("running", self.running)

            # update screen to user
            pygame.display.flip()

        # quit cleanly
        pygame.quit()
