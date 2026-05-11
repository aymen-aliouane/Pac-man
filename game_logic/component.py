from game_logic.characters import PacMan, Ghost
from dataclasses import dataclass, field
from enum import Enum
import pygame


class Controls(Enum):
    """Different command available for the user"""
    WASD = {
        "UP": pygame.K_w,
        "DOWN": pygame.K_s,
        "LEFT": pygame.K_a,
        "RIGHT": pygame.K_d
    }
    ZQSD = {
        "UP": pygame.K_z,
        "DOWN": pygame.K_s,
        "LEFT": pygame.K_q,
        "RIGHT": pygame.K_d
    }
    ARROWS = {
        "UP": pygame.K_UP,
        "DOWN": pygame.K_DOWN,
        "LEFT": pygame.K_LEFT,
        "RIGHT": pygame.K_RIGHT
    }


class Cheat(Enum):
    """Available cheats"""

    INVICIBLE = "invincible"
    NO_COLLISIONS = "no_collision"
    SKIP_LEVEL = "skip_level"
    INCREASE_SPEED = "increase_speed"


@dataclass
class Game:
    """
    Main base class for the game, contain all infos and settings
    """
    from states import State

    my_map: list[list[int]]
    player: PacMan
    # ghosts: list[Ghost]

    # point_per_pacgum: int
    # point_per_ghost: int
    # point_per_super_pacgum: int
    # is_alive: bool

    settings: Settings
    display: DisplaySettings
    state: State = State.GAME



@dataclass
class DisplaySettings:
    """Settings of the displaying"""
    width: int
    height: int
    offset: int = 6

    def update_displaying_parameter(self, maze_map: list[list[int]]):
        """
        Function called after object creation to construct the attributes
        cell_size, margin_left and margin_top,
        based on the height, width and the maze
        """
        self.cell_size = min(self.width / len(maze_map[0]),
                        self.height / len(maze_map)) - 2
        self.margin_left = (self.width - self.cell_size * len(maze_map[0])) // 2
        self.margin_top = (self.height - self.cell_size * len(maze_map)) // 2


@dataclass
class Settings:
    """
    Class containing the main settings of the user
    """
    max_time: int
    controls: Controls
    fps: int
    cheats: list[Cheat] = field(default_factory=list)
