from typing import Any
from enum import Enum
import pygame


class MenuState():
    """Class that handle the user events in the menue"""
    pass


class GameState():
    """Class that handle the user events during the game"""

    def handle_input(self, events: list[Any], game: Any, dt) -> bool:
        """Handle user inputs"""

        # game is the class Game in the module component
        for event in events:
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True

                if event.key == game.settings.controls.value["UP"]:
                    game.player.update_direction("up")
                if event.key == game.settings.controls.value["DOWN"]:
                    game.player.update_direction("down")
                if event.key == game.settings.controls.value["RIGHT"]:
                    game.player.update_direction("right")
                if event.key == game.settings.controls.value["LEFT"]:
                    game.player.update_direction("left")

        game.player.move(game.my_map, dt)

        return False


class PauseState():
    """Class that handle the user events when paused"""
    pass


class State(Enum):
    """
    The state where the user is in,
    it is an object that will handle the inputs
    based on witch state the user is in
    """
    MENU = MenuState()
    GAME = GameState()
    PAUSE = PauseState()
