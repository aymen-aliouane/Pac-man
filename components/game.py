from __future__ import annotations

from collections import deque
from typing import cast
from dataclasses import dataclass, field
from maze.maze_construct import construct_maze
from maze.pacgums import get_pacgums_map

import pygame

from displaying import GhostRenderer, LayerRenderer, PacManRenderer
from game_logic.ghosts import Ghost
from game_logic.pacman import PacMan

from components.settings import DisplaySettings, Settings
from .support_class import Cheat


class State:
    """Class representing the current state of the game,
    used to handle the game loop"""

    def handle_input(self, events: list[pygame.Event], game: Game) -> bool:
        print("end game")
        return True

    def update(self, game: Game, dt: float) -> None:
        """Update the game state"""
        pass

    def render(self, game: Game, screen: pygame.Surface) -> None:
        """Render the game state"""
        pass


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

    layer_renderer: LayerRenderer
    pacman_renderer: PacManRenderer
    ghosts_renderer: GhostRenderer

    time_remaining: float

    state: State = State()

    score: int = 0
    level: int = 1
    achievements: dict[str, str] = field(default_factory=dict)
    total_kills: int = 0
    post_death_timer: float = 0.0
    post_kill_timer: float = 0.0
    kill_location: list[tuple[int, int]] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Function called after the initialization of the game,
        will initialise the pacgum eaten and remaining"""

        self.pacgums_score = 0
        self.pacgums_total = sum(pacgum for row in self.pacgums
                                 for pacgum in row if pacgum == 1)

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
            self.pacgums_score += 1
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

    def game_victory(self) -> bool:
        """True if the player win all 10 levels of the game,
        can be checked in the victory screen to display a special message
        and tell the user to go back to menu to play again"""
        return self.level >= 10

    def achievements_check(self) -> None:
        if (self.score >= 100
                and "Welcome to the game" not in self.achievements):
            self.achievements["Welcome to the game"] = "Score 100 points"
        if (self.score >= 1000
                and "Not bad" not in self.achievements):
            self.achievements["Not bad"] = "Score 1000 points"
        if (self.score >= 5000
                and "Accidental Competence" not in self.achievements):
            self.achievements["Accidental Competence"] = "Score 5000 points"
        if (self.score >= 10000
                and "The Student Has No Master" not in self.achievements):
            self.achievements[
                "The Student Has No Master"] = "Score 10000 points"
        if (self.score >= 50000
                and "Cheater" not in self.achievements):
            self.achievements["Cheater"] = "Score 50000 points"

        if (self.time_remaining <= 0
                and "Time's up!" not in self.achievements):
            self.achievements["Time's up!"] = "Lose by time out"

        if (self.total_kills >= 1
                and "First Blood" not in self.achievements):
            self.achievements["First Blood"] = "Kill your first ghost"
        if (self.total_kills >= 4
                and "It's becoming personal" not in self.achievements):
            self.achievements["It's becoming personal"] = "Kill 5 ghosts"
        if (self.total_kills >= 6
                and "Ghost Hunter" not in self.achievements):
            self.achievements["Ghost Hunter"] = "Kill 10 ghosts"
        if (self.total_kills >= 10
                and "Butcher" not in self.achievements):
            self.achievements["Butcher"] = "Kill 50 ghosts"
        if (self.total_kills >= 20
                and "Hiroshima?" not in self.achievements):
            self.achievements["Hiroshima?"] = "Kill 100 ghosts"

        if (self.player.lives == 2 and "First Time?" not in self.achievements):
            self.achievements["First Time?"] = "killed by a ghost"
        if (self.player.lives == 1 and "Pathetic" not in self.achievements):
            self.achievements["Pathetic"] = "killed by a ghost twice"

        if self.game_victory() and "Cheater" not in self.achievements:
            self.achievements["Cheater"] = "Win the game"

    def check_ghost_collision(self) -> None:
        """Check if there is a collision between the player and a ghost,
        and update the game state accordingly"""

        for ghost in self.ghosts:
            if self.player.cell_from == ghost.cell:

                if ghost.frightened_timer > 0.0:
                    # if the ghost is frightened,
                    # the player eat it and get points
                    self.score += self.settings.point_per_ghost
                    self.total_kills += 1

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

        self.player.cell_from = cast(tuple[int, int], tuple(pacman_pos))
        self.player.cell_to = cast(tuple[int, int], tuple(pacman_pos))

        for ghost in self.ghosts:
            ghost.cell = ghost.initial_corner
            ghost.path = deque()
            ghost.move_timer = 0.0

    def next_level(self) -> None:
        """Change the level, it will be called when the player win a level,
        it will reset the game and increase the difficulty by increasing the
        ghosts speed and decreasing the time remaining"""

        self.level += 1
        self.time_remaining = max(30.0, self.time_remaining - 10.0)

        for ghost in self.ghosts:
            ghost.speed += 0.5

        self.pacgums_score = 0
        self.pacgums_total = sum(pacgum for row in self.pacgums
                                 for pacgum in row if pacgum == 1)

        # give a seed of 0 if the seed is 0 to keep it random,
        # otherwise increase it by the level number
        self.my_map = construct_maze(len(self.my_map[0]),
                                     len(self.my_map),
                                     (self.settings.seed + self.level
                                      if self.settings.seed > 0 else 0))
        self.layer_renderer.update_maze_layer(self.my_map)
        self.player.maze = self.my_map
        self.pacgums = get_pacgums_map(self.my_map)

        self.reset_game()
