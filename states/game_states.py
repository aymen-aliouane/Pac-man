from components.game import Game
from .lost_state import LostState
import pygame


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

            player_cell = game.player.move(dt)
            ghost_cell = game.ghosts[0].move(dt)

            if not game.ghosts[0].path or game.ghosts[0].path[-1] != player_cell:
                game.ghosts[0].update_path(player_cell, game.my_map)

            game.pacgum_eaten(player_cell)
            #collision with pacgums and ghosts

        else:
            game.state = LostState()

    def render(self, game: Game, screen: pygame.Surface):
        game.layer_renderer.render(screen, game)
        game.pacman_renderer.render(screen, game.player)
        game.ghosts_renderer.render(screen, game.ghosts[0])
