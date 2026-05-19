from typing import cast

from mazegenerator.mazegenerator import MazeGenerator  # type: ignore


def construct_maze(width: int, height: int, seed: int) -> list[list[int]]:
    """Construct a maze using the MazeGenerator class
    from the mazegenerator package."""
    maze = MazeGenerator(
        (width, height),
        seed=seed)

    return cast(list[list[int]], maze.maze)
