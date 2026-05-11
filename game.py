from mazegenerator.mazegenerator import MazeGenerator
from game_logic.component import Game, Settings, DisplaySettings, Controls
from displaying.build_maze import build_maze_layer
from displaying.display_characters import Animator
from game_logic.characters import PacMan

import pygame


def initialise(settings: Settings) -> pygame.Surface:
    """Initialise the main layer of the game"""

    screen = pygame.display.set_mode((settings.width, settings.height))
    pygame.display.set_caption("Pac-man")

    return screen


def game():
    """The game loop, we initialise the variables in it and run the game"""
    pygame.init()
    maze = MazeGenerator((17, 15))

    # initialise settings and display settings that will be part
    # of the main game class
    settings = Settings(max_time=120, controls=Controls.WASD, fps=60)
    display_settings = DisplaySettings(width=1900, height=900)

    # update the settings to adatpt to the maze size
    display_settings.update_displaying_parameter(maze.maze)
    player = PacMan(0, 0)

    game = Game(maze.maze, player, settings, display_settings)

    animator  = Animator(display_settings)

    # main layer is the main page, maze is the map
    # and character is the player and mobs
    main_layer = initialise(display_settings)
    maze_layer = build_maze_layer(display_settings, maze.maze)

    run = True
    clock = pygame.time.Clock()

    while run:
        # clock.tick() return the time in ms
        # between this frame and the last frame
        dt = clock.tick(settings.fps) / 1000

        # each frame we draw the image of the maze, then the player on top of it
        # no need to iterate over all cells we have now maze_layer
        main_layer.blit(maze_layer, (0, 0))
        main_layer.blit(animator.get_pacman_frame(), animator.get_pos(player.x, player.y))

        # game.state is the state of the player, it can be Game, Menu or Pause
        # based on that it will handle input differently, but all of thems return
        # True if the user ask to quit
        end = game.state.value.handle_input(pygame.event.get(), game, dt)
        if end:
            break

        # function to make, then maybe putting it in the game state part
        # player.move(maze.maze)

        # update screen to user
        pygame.display.flip()

    # quit cleanly
    pygame.quit()


if __name__ == "__main__":
    game()