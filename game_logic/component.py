from game_logic.characters import PacMan, Ghost
from displaying import LayerRenderer, PacManRenderer, GhostRenderer
from dataclasses import dataclass, field
from enum import Enum
import pygame


class State:
    """Class that handle the user events during the game"""

    def handle_input(self, events: list[pygame.Event], game: Game) -> bool:
        """Handle user inputs"""
        pass

    def update(self, game: Game, dt: float):
        """Update the game state"""
        pass

    def render(self, game: Game, screen: pygame.Surface):
        """Render the game state"""
        pass


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

    my_map: list[list[int]]
    pacgums: list[list[int]]
    player: PacMan
    ghosts: list[Ghost]

    settings: Settings
    display: DisplaySettings
    state: State
    layer_renderer: LayerRenderer

    pacman_renderer: PacManRenderer
    ghosts_renderer: GhostRenderer = None

    score: int = 0
    level: int = 1

    def pacgum_eaten(self, cell: tuple[int, int]):
        """Function called when pacman eat a pacgum, it will update the score and the pacgums map"""
        x, y = cell

        if self.pacgums[y][x] == 0:
            return

        elif self.pacgums[y][x] == 1:
            self.score += self.settings.point_per_pacgum
        elif self.pacgums[y][x] == 2:
            self.score += self.settings.point_per_super_pacgum

        self.pacgums[y][x] = 0


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
        # -1 let us get a little gap between the the maze and the border of the screen
        self.cell_size = int(min(self.width / len(maze_map[0]) - 1,
                             self.height / len(maze_map) - 1))
        self.margin_left = (self.width - self.cell_size * len(maze_map[0])) // 2
        self.margin_top = (self.height - self.cell_size * len(maze_map)) // 2

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

