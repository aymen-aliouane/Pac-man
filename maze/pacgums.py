import pygame
import random


def update_pacgum_layer(
    layer: pygame.Surface,
    pacgums: list[list[int]],
    cell_size: int,
    margin_left: int,
    margin_top: int,
) -> None:
    """display the pacgums on the screen"""

    # transparent color
    layer.fill((0, 0, 0, 0))

    for y in range(len(pacgums)):
        for x in range(len(pacgums[0])):
            cell = pacgums[y][x]
            if cell:
                # pacgum radius
                if cell == 1:
                    radius = cell_size // 18

                # super pacgum radius
                elif cell == 2:
                    radius = cell_size // 10

                pygame.draw.circle(
                    layer,
                    (222, 161, 133),
                    (
                        x * cell_size + margin_left + cell_size // 2,
                        y * cell_size + margin_top + cell_size // 2,
                    ),
                    radius,
                )


def get_pacgums_map(maze: list[list[int]]) -> list[list[int]]:
    """Get the map of pacgums.
    0 for no pacgum,
    1 for normal pacgum
    2 for super pacgum"""
    pacgums: list[list[int]] = []

    for y, row in enumerate(maze):
        pacgums.append([])

        for x, cell in enumerate(row):
            # super pacgums are placed at the corners of the maze
            if (
                (x == 0 and y == len(maze) - 1)
                or (x == 0 and y == 0)
                or (x == len(maze[0]) - 1 and y == len(maze) - 1)
                or (x == len(maze[0]) - 1 and y == 0)
            ):
                pacgums[y].append(2)

            # normal pacgums are placed on the cells not
            # blocked by 4 walls with a probability of 0.8
            elif cell != 15 and random.random() < 0.8:
                pacgums[y].append(1)

            else:
                pacgums[y].append(0)

    return pacgums
