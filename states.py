from game_logic.component import Game
import pygame


class MenuState():
    """Class that handle the user events in the menue"""
    pass


class VictoryState():
    """Class that handle the user events in the menue"""
    pass

class LostState():
    """Class that handle the user events in the menue"""
    pass


class GameState():
    """Class that handle the user events during the game"""

    def handle_input(self, events: list[pygame.Event], game: Game) -> bool:
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

        return False

    def update(self, game: Game, dt: float):

        if game.player.is_alive():

            cell_to_update = game.player.move(dt)
            game.pacgum_eaten(cell_to_update)

            #collision with pacgums and ghosts
            pass

        else:
            game.state = LostState()

    def render(self, game: Game, screen: pygame.Surface):
        game.layer_renderer.render(screen, game)
        game.pacman_renderer.render(screen, game.player)


class PauseState():
    """Class that handle the user events when paused"""
    pass

