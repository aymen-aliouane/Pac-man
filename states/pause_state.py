from components import Game, State
from .game_state import GameState
from .menu_state import MenuState

import pygame


class PauseState(State):
    """Class that handle the user events when paused"""
    # The options of the pause menu, and the index of the user choice
    options = ["Resume", "Quit"]
    choice = 0

    # True when user click enter to validate the choice
    validate_choice = False

    def handle_input(self, events: list[pygame.Event], game: Game) -> bool:
        """Handle user inputs in the pause menu,
        return True if the user want to quit the game"""

        # Handle the events
        for event in events:
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                # if the user press escape, it will resume the game
                if event.key == pygame.K_ESCAPE:
                    game.state = GameState()

                # Move up in the menu
                if event.key == game.settings.controls.value["UP"]:
                    self.choice -= 1 % len(self.options)

                # Move down in the menu
                if event.key == game.settings.controls.value["DOWN"]:
                    self.choice += 1 % len(self.options)

                # if the user press enter,
                # it will validate the choice
                # and execute actions in update method
                if event.key == pygame.K_RETURN:
                    self.validate_choice = True

        return False

    def update(self, game: Game, dt: float):
        """Update the game state when paused,
        execute the actions of the user choice"""

        # If the user validate the choice, execute the actions
        if self.validate_choice:
            user_choice = self.options[self.choice]

            if user_choice == "Resume":
                game.state = GameState()
            elif user_choice == "Quit":
                game.state = MenuState()

    def render(self, game: Game, screen: pygame.Surface):
        """Render the pause menu background, with the options and the user
        choice"""
        game.layer_renderer.render_pause_background(
            screen, self.options, self.choice
            )
