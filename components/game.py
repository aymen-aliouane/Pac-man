from game_logic.pacman import PacMan
from game_logic.ghosts import Ghost
from displaying import LayerRenderer, PacManRenderer, GhostRenderer
from components.settings import DisplaySettings, Settings
from .support_class import Cheat
from dataclasses import dataclass, field
from collections import deque
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
    ghosts_renderer: GhostRenderer

    score: int = 0
    level: int = 1
    post_death_timer: float = 0.0
    post_kill_timer: float = 0.0
    kill_location: list[tuple[int, int]] = field(default_factory=list)

    def pacgum_eaten(self, cell: tuple[int, int]):
        """Function called when pacman eat a pacgum, it will update the score and the pacgums map"""
        x, y = cell

        if self.pacgums[y][x] == 0:
            return

        elif self.pacgums[y][x] == 1:
            self.score += self.settings.point_per_pacgum
        elif self.pacgums[y][x] == 2:
            self.score += self.settings.point_per_super_pacgum
            for ghost in self.ghosts:
                if ghost.alive:
                    ghost.frightened_timer = 10.0
                    if ghost.path:
                        ghost.path = deque([ghost.path[0]])
        self.pacgums[y][x] = 0
        

    def victory(self):
        if all(pacgum in {0, 2} for row in self.pacgums for pacgum in row):
            return True

    def check_ghost_collision(self):
        

        for ghost in self.ghosts:
            if self.player.cell_from == ghost.cell:

                if ghost.frightened_timer > 0.0:
                    self.post_kill_timer = 1.0
                    ghost.alive = False
                    ghost.frightened_timer = 0.0
                    self.path = deque()
                    self.score += self.settings.point_per_ghost
                    self.kill_location.append(ghost.cell)
                    return

                elif Cheat.INVINCIBLE in self.settings.cheats:
                    return

                elif ghost.alive:
                    self.player.lives -= 1
                    self.reset_game()
                    self.post_death_timer = 3.0
                    break

            
    def reset_game(self):
        pacman_pos = [len(self.my_map[0]) // 2, len(self.my_map) // 2]

        if self.my_map[pacman_pos[1]][pacman_pos[0]] == 15:
            pacman_pos[0] -= 1

        self.player.cell_from = tuple(pacman_pos)
        self.player.cell_to = tuple(pacman_pos)

        for ghost in self.ghosts:
            ghost.cell = ghost.initial_corner
            ghost.path = deque()
            ghost.move_timer = 0.0


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