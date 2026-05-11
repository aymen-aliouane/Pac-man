from mazegenerator.mazegenerator import MazeGenerator
from component import Game, Settings, DisplaySettings, Controls
from build_maze import build_maze_layer
from display_characters import Animator
from characters import PacMan

import pygame


def initialise(settings: Settings) -> pygame.Surface:
    w, h = settings.width, settings.height

    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption("Pac-man")

    return screen


def game():
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
        dt = clock.tick(settings.fps)

        main_layer.blit(maze_layer, (0, 0))
        main_layer.blit(animator.get_pacman_frame(), animator.get_pos(player.x, player.y))

        end = game.state.value.handle_input(pygame.event.get(), game)
        if end:
            break

        # player.move(maze.maze)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    game()