from game_logic.pacman import PacMan
from game_logic.ghosts import Ghost
from displaying import LayerRenderer, PacManRenderer, GhostRenderer
from components.settings import DisplaySettings, Settings
from dataclasses import dataclass
import pygame


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