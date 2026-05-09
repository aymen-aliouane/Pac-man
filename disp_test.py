from mazegenerator.mazegenerator import MazeGenerator
from component import Settings, Controls
import pygame
import time


def initialise(settings: Settings) -> pygame.Surface:
    pygame.init()
    w, h = settings.width, settings.height

    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption("Pac-man")

    return screen


def build_maze_tiles(maze: list[list[int]], size=40):
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

            tiles[y].append(build_tiles(cell, right, top, left, bottom, size))

    return tiles


def build_tiles(cell, right, top, left, bottom, cell_size=40, offset=3):
    """
    Build a Surface object for a given tile based on it's different walls.
    this cell is normally containing inner and outer line, but we reduced
    that to only the inner one, it looks better.
    
    right, top, left, bottom: the neighbor of the cell in each direction
    cell_size: the size of a dispplayed cell
    offset: the marge between the inner and outer line
    """

    # initialise the surface
    surface = pygame.surface.Surface((cell_size, cell_size))
    surface.fill((0,0,0))
    color = (33, 33, 222)  # Pac-Man blue

    # define the limit of the inner line based on the offset
    edge = cell_size - 1
    inner_edge = edge - offset

    # Lambda to know if the cell have or not a wall for each direction
    has_left = lambda cell: cell & 8
    has_bottom = lambda cell: cell & 4
    has_right = lambda cell: cell & 2
    has_top = lambda cell: cell & 1

    # draw the base walls and limiting the x and y based on the neighbors
    # so we don't get some + intersections in the maze
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



def game():
    settings = Settings(width=1900, height=900, max_time=120, controls=Controls.WASD)
    background = initialise(settings)
    player_surface = pygame.Surface((settings.width, settings.height), pygame.SRCALPHA)
    maze = MazeGenerator((17, 15))
    run = True
    clock = pygame.time.Clock()
    past_time = time.time()
    FPS = 60

    size = min(settings.width / len(maze.maze[0]), settings.height / len(maze.maze)) - 2
    margin_left = (settings.width - size * len(maze.maze[0])) // 2
    margin_top = (settings.height - size * len(maze.maze)) // 2
    tiles = build_maze_tiles(maze.maze, size)

    # adding all the cells surfaces on top of the background surface, so we only draw one
    # background rather that multiple ones
    pygame.draw.rect(background, (33, 33, 222), (margin_left - 2, margin_top - 2, size * len(maze.maze[0]) + 4, size * len(maze.maze) + 4) )
    for y, row in enumerate(tiles):
        for x, cell in enumerate(row):
            background.blit(cell, (x * size + margin_left, y * size + margin_top))


    while run:
        clock.tick(FPS)

        actual_time = time.time()
        dt = actual_time - past_time
        past_time = actual_time
        
        background.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False


        pygame.display.flip()
        # replace it later with pygame.display.update() for optimisation
    pygame.quit()


if __name__ == "__main__":
    game()