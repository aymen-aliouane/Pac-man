from components.game import Game
from .lost_state import LostState
from .victory_state import VictoryState
from .pause_state import PauseState
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
                    game.state = PauseState()

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
        if game.post_death_timer > 0.0:
            game.post_death_timer -= dt
            return

        if game.post_kill_timer > 0.0:
            game.post_kill_timer -= dt
            if game.post_kill_timer <= 0.0:
                game.kill_location.clear()
            return

        if game.player.is_alive():

            player_cell = game.player.move(dt)
            game.check_ghost_collision()

            if not game.player.is_alive():
                game.state = LostState()
                return

            for ghost in game.ghosts:
                ghost.move(dt)

                game.check_ghost_collision()

                if not game.player.is_alive():
                    game.state = LostState()
                    return

                if not ghost.path or ghost.path[-1] != player_cell:
                    ghost.update_path(player_cell, game.player.direction ,game.my_map)

            game.pacgum_eaten(player_cell)

            if game.victory():
                game.state = VictoryState()

        else:
            game.state = LostState()

    def render(self, game: Game, screen: pygame.Surface):
        game.layer_renderer.render_background(screen, game)
        
        game.pacman_renderer.render(screen, game.player)
        for ghost in game.ghosts:
            game.ghosts_renderer.render(screen, ghost)

        game.layer_renderer.render_points(screen, game)
