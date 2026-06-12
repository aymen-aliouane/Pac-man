import pygame.freetype
from dataclasses import dataclass, field
from components.support_class import Controls, Cheat


@dataclass
class DisplaySettings:
    """Settings related to the display

    Attributes:
    offset: int
        The offset for the cells in pixels,
        used to display a double line wall

    (defined in update_displaying_parameter)
    cell_size: int
        The size of a cell in pixels,
        calculated based on the width, height and the maze
    margin_left: int
        The margin between the left border of the screen
        and the maze in pixels,
        calculated based on the width, height and the maze
    margin_top: int
        The margin between the top border of the screen
        and the maze in pixels,
        calculated based on the width, height and the maze
    font: pygame.freetype.Font
        The font used to display the score and the time,
        calculated based on the cell_size
    """

    pygame.freetype.init()
    width: int
    height: int
    offset: int = 6

    def update_displaying_parameter(self, maze_map: list[list[int]]) -> None:
        """
        Function called after object creation to construct the attributes
        cell_size, margin_left and margin_top,
        based on the height, width and the maze
        """
        # the -1 lets us get a little gap between the maze and the border
        # of the screen
        self.cell_size = int(
            min(
                (self.width // 1.2) / len(maze_map[0]),
                (self.height // 1.2) / len(maze_map),
            )
        )
        self.margin_left = (
            self.width - self.cell_size * len(maze_map[0])
            ) // 2
        self.margin_top = (
            self.height - self.cell_size * len(maze_map)
            ) // 2
        self.font: pygame.freetype.Font = pygame.freetype.Font(
            "sprite/other/BoldPixels.ttf",
            self.width / 60,
        )
        self.small_font: pygame.freetype.Font = pygame.freetype.Font(
            "sprite/other/BoldPixels.ttf",
            self.width / 70,
        )


@dataclass
class Settings:
    """
    Class containing the main settings of the user

    Attributes:
    max_time: int
        The maximum time of a game in seconds
    seed: int
        The seed used to generate the maze, if 0 or less the seed is random
    point_per_pacgum: int
        The points given to the player when he eats a pacgum
    point_per_ghost: int
        The points given to the player when he eats a ghost
    point_per_super_pacgum: int
        The points given to the player when he eats a super pacgum
    controls: Controls
        The controls of the player
    fps: int
        The frames per second of the game
    cheats: list[Cheat]
        The list of the cheats activated by the player
    """
    max_time: int
    seed: int

    point_per_pacgum: int
    point_per_ghost: int
    point_per_super_pacgum: int
    high_scores_file: str

    controls: Controls
    fps: int
    cheats: list[Cheat] = field(default_factory=list)
