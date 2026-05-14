from components.game import Settings
from initialise.init_game import init_game
import pygame
import sys


def initialise(settings: Settings) -> pygame.Surface:
    """Initialise the main layer of the game"""

    screen = pygame.display.set_mode((settings.width, settings.height))
    pygame.display.set_caption("Pac-man")

    return screen


def game_loop():
    """The game loop, we initialise the variables in it and run the game"""
    from states.states import GameState
    pygame.init()

    if len(sys.argv) != 2:
        print("Usage: python3 game.py <config_file>")
        sys.exit(1)
    print(sys.argv[1])
    game = init_game(sys.argv[1])
    game.state = GameState()

    # main layer is the main page, maze is the map
    # and character is the player and mobs
    main_layer = initialise(game.display)

    run = True
    clock = pygame.time.Clock()

    while run:
        # clock.tick() return the time in ms
        # between this frame and the last frame
        dt = clock.tick(game.settings.fps) / 1000

        # game.state is the state of the player, it can be Game, Menu or Pause
        # based on that it will handle input differently, but all of thems return
        # True if the user ask to quit
        end = game.state.handle_input(pygame.event.get(), game)
        if end:
            break

        game.state.update(game, dt)

        game.state.render(game, main_layer)

        # update screen to user
        pygame.display.flip()

    # quit cleanly
    pygame.quit()


if __name__ == "__main__":
    game_loop()