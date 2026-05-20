from typing import Any, cast

from components import Game, Settings, DisplaySettings, Controls, Cheat
from displaying import PacManRenderer, LayerRenderer, GhostRenderer
from game_logic import PacMan, Ghost
from maze.pacgums import get_pacgums_map
from maze.draw_maze import build_maze_layer
from maze.maze_construct import construct_maze

import json


def load_file(file_path: str) -> dict[str, Any]:
    """Load the maze from a file, it will be called in the main file"""
    try:
        with open(file_path, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON file")
    except FileNotFoundError:
        raise ValueError("File not found")
    except PermissionError:
        raise ValueError("Permission denied")
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")

    return cast(dict[str, Any], config)


def init_game(file_path: str) -> Game:
    """Initialise the game, it will be called in the main file"""

    config = load_file(file_path)
    config = verif_settings(config)

    # init the maze and the pacgums map
    maze = construct_maze(
        cast(int, config.get("width")),
        cast(int, config.get("height")),
        cast(int, config.get("seed")),
    )
    pacgums = get_pacgums_map(maze)

    # look for a position for pacman in the middle of the maze
    # not blocked by 4 walls
    pacman_pos = [len(maze[0]) // 2, len(maze) // 2]

    if maze[pacman_pos[1]][pacman_pos[0]] == 15:
        pacman_pos[0] -= 1
    player = PacMan(pacman_pos[0], pacman_pos[1], maze)

    # init settings based on user settings file
    settings = Settings(
        seed=cast(int, config.get("seed")),
        point_per_pacgum=cast(int, config.get("point_per_pacgum")),
        point_per_ghost=cast(int, config.get("point_per_ghost")),
        point_per_super_pacgum=cast(int, config.get("point_per_super_pacgum")),
        max_time=cast(int, config.get("max_time")),
        controls=Controls(config.get("controls")),
        fps=cast(int, config.get("fps")),
        cheats=[Cheat.INCREASE_SPEED],
    )

    # the availabe size will be full size, 1600x900, 1200x700
    # the user need to be able to choose between those 3 sizes in the menue
    # as well as changing the settings of the game

    # pygame.init()
    # w, h = pygame.display.get_desktop_sizes()[0]

    display_settings = DisplaySettings(width=1200, height=700)
    display_settings.update_displaying_parameter(maze)

    # build the maze layer and the renderers
    maze_layer = build_maze_layer(display_settings, maze)
    layer_renderer = LayerRenderer(display_settings, maze_layer)
    pacman_renderer = PacManRenderer(display_settings)
    ghosts_renderer = GhostRenderer(display_settings)

    # init the main game class
    game = Game(
        my_map=maze,
        pacgums=pacgums,
        player=player,
        ghosts=[
            Ghost("blinky", (0, 0)),
            Ghost("inky", (0, len(maze) - 1)),
            Ghost("pinky", (len(maze[0]) - 1, len(maze) - 1)),
            Ghost("clyde", (len(maze[0]) - 1, 0)),
        ],
        settings=settings,
        display=display_settings,
        layer_renderer=layer_renderer,
        pacman_renderer=pacman_renderer,
        ghosts_renderer=ghosts_renderer,
        time_remaining=cast(float, config.get("max_time")),
    )

    return game


def verif_settings(settings: dict[str, Any]) -> dict[str, Any]:
    """Function to verify and clean the settings"""

    if (settings.get("point_per_pacgum") is None or
            not isinstance(settings["point_per_pacgum"], int) or
            settings["point_per_pacgum"] < 0):
        print("point_per_pacgum must be a positive integer superior to 100")
        settings["point_per_pacgum"] = 10

    if (settings.get("point_per_ghost") is None or
            not isinstance(settings["point_per_ghost"], int) or
            settings["point_per_ghost"] < 0):
        print("point_per_ghost must be a positive integer")
        settings["point_per_ghost"] = 200

    if (settings.get("point_per_super_pacgum") is None or
            not isinstance(settings["point_per_super_pacgum"], int) or
            settings["point_per_super_pacgum"] < 0):
        print("point_per_super_pacgum must be a positive integer")
        settings["point_per_super_pacgum"] = 50

    if (settings.get("max_time") is None or
            not isinstance(settings["max_time"], int) or
            settings["max_time"] <= 100):
        print("max_time must be a positive integer")
        settings["max_time"] = 300

    if (settings.get("seed") is None or
            not isinstance(settings["seed"], int) or
            settings["seed"] < 0):
        print("seed must be a positive integer")
        settings["seed"] = 0

    if (settings.get("controls") is None or
            not isinstance(settings["controls"], str) or
            settings["controls"] not in {"WASD", "ZQSD", "ARROWS"}):
        print("controls must be one of the following: WASD, ZQSD, ARROWS")
        settings["controls"] = "WASD"

    if settings["controls"] == "WASD":
        settings["controls"] = Controls.WASD
    elif settings["controls"] == "ZQSD":
        settings["controls"] = Controls.ZQSD
    elif settings["controls"] == "ARROWS":
        settings["controls"] = Controls.ARROWS

    if (settings.get("fps") is None or
            not isinstance(settings["fps"], int) or
            settings["fps"] <= 0):
        print("fps must be a positive integer")
        settings["fps"] = 60

    if (settings.get("width") is None or
            not isinstance(settings["width"], int) or
            settings["width"] < 10 or settings["width"] > 20):
        print("Width must be a number between 10 and 20")
        settings["width"] = 15

    if (settings.get("height") is None or
            not isinstance(settings["height"], int) or
            settings["height"] < 10 or settings["height"] > 20):
        print("Height must be a number between 10 and 20")
        settings["height"] = 15

    return settings
