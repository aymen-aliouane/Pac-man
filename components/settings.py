from components.support_class import Controls, Cheat
from dataclasses import dataclass, field
import pygame.freetype


@dataclass
class DisplaySettings:
    """Settings of the displaying"""
    pygame.freetype.init()
    width: int
    height: int
    offset: int = 6

    def update_displaying_parameter(self, maze_map: list[list[int]]):
        """
        Function called after object creation to construct the attributes
        cell_size, margin_left and margin_top,
        based on the height, width and the maze
        """
        # -1 let us get a little gap between the the maze and the border of the screen
        self.cell_size = int(min(self.width / len(maze_map[0]) - 1,
                             self.height / len(maze_map) - 1))
        self.margin_left = (self.width - self.cell_size * len(maze_map[0])) // 2
        self.margin_top = (self.height - self.cell_size * len(maze_map)) // 2
        self.font: pygame.freetype.Font = pygame.freetype.Font("sprite/other/BoldPixels.ttf", self.cell_size // 2)


@dataclass
class Settings:
    """
    Class containing the main settings of the user
    """
    max_time: int
    seed: int

    point_per_pacgum: int
    point_per_ghost: int
    point_per_super_pacgum: int

    controls: Controls
    fps: int
    cheats: list[Cheat] = field(default_factory=list)