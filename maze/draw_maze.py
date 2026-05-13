import pygame
from components.game import DisplaySettings

def build_maze_tiles(settings: DisplaySettings, maze: list[list[int]]) -> list[list[pygame.Surface]]:
    """
    Build the drawing of all the tiles of the maze.

    Parameter:
        settings: DisplaySettings = settings of the display
        maze: list[list[int]] = the maze to build
    
    Return:
        A double array of surfaces, one for each tile
    """
    tiles = []
    cols = len(maze[0])
    rows = len(maze)

    for y in range(rows):
        tiles.append([])

        for x in range(cols):
            cell = maze[y][x]

            right = maze[y][x + 1] if x < cols - 1 else 15
            left = maze[y][x - 1] if x > 0 else 15
            top = maze[y - 1][x] if y > 0 else 15
            bottom = maze[y + 1][x] if y < rows - 1 else 15

            tiles[y].append(build_tiles(cell, settings, right, top, left, bottom))

    return tiles


def build_tiles(cell, settings: DisplaySettings, right: int, top, left, bottom) -> pygame.Surface:
    """
    Build a Surface object for a given tile based on it's different walls,
    with a small offset to make a pacman like double wall 

    Parameters:
        cell: int = the cell to draw and return
        settings: DisplaySettings = settings to use during the drawing
        right, top, left, bottom: int = the neighbor of the cell in each direction

    Return:
        A pygame.Surface where the cell is drawn
    """

    # initialise the surface
    surface = pygame.Surface((settings.cell_size, settings.cell_size))
    surface.fill((0,0,0))
    color = (33, 33, 222)  # Pac-Man blue

    # define the limit of the line based on the offset
    offset = settings.offset
    edge = settings.cell_size - 1
    inner_edge = edge - offset

    # Lambda to know if the cell have or not a wall for each direction
    has_left = lambda cell: cell & 8
    has_bottom = lambda cell: cell & 4
    has_right = lambda cell: cell & 2
    has_top = lambda cell: cell & 1

    # Draw the base wall based on offset and inner_edge
    if has_top(cell):
        x_start = offset if has_left(cell) else 0
        x_end = inner_edge if has_right(cell) else edge

        pygame.draw.line(surface, color, (x_start, offset), (x_end, offset), 2)

    if has_bottom(cell):
        x_start = offset if has_left(cell) else 0
        x_end = inner_edge if has_right(cell) else edge

        pygame.draw.line(surface, color, (x_start, inner_edge), (x_end, inner_edge), 2)

    if has_left(cell):
        y_start = offset if has_top(cell) else 0
        y_end = inner_edge if has_bottom(cell) else edge

        pygame.draw.line(surface, color, (offset, y_start), (offset, y_end), 2)

    if has_right(cell):
        y_start = offset if has_top(cell) else 0
        y_end = inner_edge if has_bottom(cell) else edge

        pygame.draw.line(surface, color, (inner_edge, y_start), (inner_edge, y_end), 2)

    # Handling end of a walls to link the inner lines
    if has_right(cell) and (not has_top(cell)) and (not has_right(top)) and (not has_top(right)):
        pygame.draw.line(surface, color, (inner_edge, 0), (edge, 0), 2)

    if has_left(cell) and (not has_top(cell)) and (not has_left(top)) and (not has_top(left)):
        pygame.draw.line(surface, color, (0, 0), (offset, 0), 2)
    
    if has_right(cell) and (not has_bottom(cell)) and (not has_right(bottom)) and (not has_bottom(right)):
        pygame.draw.line(surface, color, (inner_edge, edge), (edge, edge), 2)

    if has_left(cell) and (not has_bottom(cell)) and (not has_left(bottom)) and (not has_bottom(left)):
        pygame.draw.line(surface, color, (0, edge), (offset, edge), 2)


    if has_top(cell) and (not has_right(cell)) and (not has_top(right)) and (not has_right(top)):
        pygame.draw.line(surface, color, (edge, 0), (edge, offset), 2)

    if has_bottom(cell) and (not has_right(cell)) and (not has_bottom(right)) and (not has_right(bottom)):
        pygame.draw.line(surface, color, (edge, inner_edge), (edge, edge), 2)

    if has_top(cell) and (not has_left(cell)) and (not has_top(left)) and (not has_left(top)):
        pygame.draw.line(surface, color, (0, 0), (0, offset), 2)

    if has_bottom(cell) and (not has_left(cell)) and (not has_bottom(left)) and (not has_left(bottom)):
        pygame.draw.line(surface, color, (0, inner_edge), (0, edge), 2)

    # handle corners of cells like '┐' or 'L'
    if (not has_right(cell)) and (not has_bottom(cell)) and has_bottom(right) and has_right(bottom):
        pygame.draw.line(surface, color, (inner_edge, inner_edge), (inner_edge, edge), 2)
        pygame.draw.line(surface, color, (inner_edge, inner_edge), (edge, inner_edge), 2)

    if (not has_left(cell)) and (not has_top(cell)) and has_top(left) and has_left(top):
        pygame.draw.line(surface, color, (0, offset), (offset, offset), 2)
        pygame.draw.line(surface, color, (offset, 0), (offset, offset), 2)

    if (not has_right(cell)) and (not has_top(cell)) and has_top(right) and has_right(top):
        pygame.draw.line(surface, color, (inner_edge, 0), (inner_edge, offset), 2)
        pygame.draw.line(surface, color, (inner_edge, offset), (edge, offset), 2)

    if (not has_left(cell)) and (not has_bottom(cell)) and has_bottom(left) and has_left(bottom):
        pygame.draw.line(surface, color, (offset, inner_edge), (offset, edge), 2)
        pygame.draw.line(surface, color, (0, inner_edge), (offset, inner_edge), 2)

    return surface


def build_maze_layer(settings: DisplaySettings,
                     maze: list[list[int]]) -> pygame.Surface:
    """
    Main class that build the entire maze layer, it return a surface
    containing all cells drawn on it so we can blit it directly in the game
    """

    #initialise the maze layer
    maze_layer = pygame.Surface((settings.width, settings.height))

    # get a 2d array of surfaces representing each cell
    tiles = build_maze_tiles(settings, maze)

    # draw a rectangle behind to look good
    pygame.draw.rect(maze_layer, (33, 33, 222),
                     (settings.margin_left - 2,
                      settings.margin_top - 2,
                      settings.cell_size * len(maze[0]) + 4,
                      settings.cell_size * len(maze) + 4))

    # adding all the cells surfaces on top of the background surface
    # doing that we only draw one background rather that multiple ones
    for y, row in enumerate(tiles):
        for x, cell in enumerate(row):
            maze_layer.blit(cell,
                            (x * settings.cell_size + settings.margin_left,
                             y * settings.cell_size + settings.margin_top))

    return maze_layer
