from mazegenerator.mazegenerator import MazeGenerator


def construct_maze(width: int, height: int, seed: int) -> MazeGenerator:

    maze = MazeGenerator(
        (width, height),
        seed=seed)

    return maze
