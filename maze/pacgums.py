import pygame


def pacgums_displayer(pacgums: list[list[int]],
                      width: int, height: int,
                      cell_size: int,
                      margin_left: int, margin_top: int) -> pygame.Surface:
    """display the pacgums on the screen"""
    gums = pygame.Surface((width, height), pygame.SRCALPHA)

    for y in range(len(pacgums)):
        for x in range(len(pacgums[0])):
            cell = pacgums[y][x]
            if cell:
                if cell == 1:
                    radius = 3
                elif cell == 2:
                    radius = 4
                pygame.draw.circle(gums, (255,255,255),
                                   (x * cell_size + margin_left + cell_size // 2,
                                    y * cell_size + margin_top + cell_size // 2),
                                    radius)

    return gums

def get_pacgums_map(maze: list[list[int]]) -> list[list[int]]:
    """Get the map of pacgums, 0 for no pacgum, 1 for normal pacgum and 2 for super pacgum"""
    pacgums = []

    for y, row in enumerate(maze):
        pacgums.append([])

        for x, cell in enumerate(row):
            if ((x == 0 and y == len(maze) - 1) or
                    (x == 0 and y == 0) or
                    (x == len(maze[0]) - 1 and y == len(maze) - 1) or
                    (x == len(maze[0]) - 1 and y == 0)):
                pacgums[y].append(2)

            elif cell != 15:
                pacgums[y].append(1)

            else:
                pacgums[y].append(0)

    return pacgums