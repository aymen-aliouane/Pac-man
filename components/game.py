from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

import pygame

from displaying import GhostRenderer, LayerRenderer, PacManRenderer
from game_logic.ghosts import Ghost
from game_logic.pacman import PacMan

from components.settings import DisplaySettings, Settings
from .support_class import Cheat


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
    time_remaining: float = 9.0
    post_death_timer: float = 0.0
    post_kill_timer: float = 0.0
    kill_location: list[tuple[int, int]] = field(default_factory=list)

    def pacgum_eaten(self, cell: tuple[int, int]) -> None:
        """Function called when pacman eat a pacgum,
        will update the score and the pacgums map

        Parameters:
        cell: tuple[int, int]
            Pacman's cell where the pacgum is eaten
        """
        x, y = cell

        if self.pacgums[y][x] == 0:
            return
        elif self.pacgums[y][x] == 1:
            self.score += self.settings.point_per_pacgum
        elif self.pacgums[y][x] == 2:
            # when a super pacgum is eaten,
            # all the ghosts become frightened for 7 seconds
            self.score += self.settings.point_per_super_pacgum
            for ghost in self.ghosts:
                if ghost.alive:
                    ghost.frightened_timer = 7.0
                    if ghost.path:
                        ghost.path = deque([ghost.path[0]])
        self.pacgums[y][x] = 0

    def victory(self) -> bool:
        """True if the player win"""
        return all(pacgum in {0, 2} for row in self.pacgums for pacgum in row)

    def check_ghost_collision(self) -> None:
        """Check if there is a collision between the player and a ghost,
        and update the game state accordingly"""

        for ghost in self.ghosts:
            if self.player.cell_from == ghost.cell:

                if ghost.frightened_timer > 0.0:
                    # if the ghost is frightened,
                    # the player eat it and get points
                    self.score += self.settings.point_per_ghost

                    # the ghost will be dead and will
                    # return to its initial corner
                    ghost.alive = False
                    ghost.frightened_timer = 0.0
                    ghost.path = (deque([ghost.path[0]])
                                  if ghost.path else deque())
                    # we save the location of the kill to
                    # display the kill effect for a short time
                    # and we set a timer to remove it after 1 second
                    self.post_kill_timer = 1.0
                    self.kill_location.append(ghost.cell)
                    return

                elif Cheat.INVINCIBLE in self.settings.cheats:
                    # if the invincible cheat is activated,
                    # the player eat the ghost but ghosts
                    # can't kill the player
                    return

                elif ghost.alive:
                    # if the ghost is alive during the collision
                    # the player lose a life and the game is reset
                    self.player.lives -= 1
                    self.reset_game()

                    # timer after the death
                    self.post_death_timer = 2.0
                    break

    def reset_game(self) -> None:
        """
        Reset the game after a death,
        the player and the ghosts return to their initial positions
        and the ghosts become alive
        """
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
    """Class representing the current state of the game,
    used to handle the game loop"""

    def handle_input(self, events: list[pygame.Event], game: Game) -> bool:
        print("end game")
        return True

    def update(self, game: Game, dt: float):
        """Update the game state"""
        pass

    def render(self, game: Game, screen: pygame.Surface):
        """Render the game state"""
        pass
