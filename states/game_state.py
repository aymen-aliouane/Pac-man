from components import Game, Cheat, State
from .lost_state import LostState
from .victory_state import VictoryState

import pygame


class GameState(State):
    """Class that handle the user events during the game"""

    def handle_input(self, events: list[pygame.Event], game: Game) -> bool:
        """Handle user inputs in the game,
        return True if the user want to quit the game"""

        # Handle the events
        for event in events:
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                # if the user press escape, it will pause the game
                if event.key == pygame.K_ESCAPE:
                    from .pause_state import PauseState
                    game.state = PauseState()

                # if the user press up, down, right or left,
                # it will update the player direction
                if event.key == game.settings.controls.value["UP"]:
                    game.player.update_direction("up")

                if event.key == game.settings.controls.value["DOWN"]:
                    game.player.update_direction("down")

                if event.key == game.settings.controls.value["RIGHT"]:
                    game.player.update_direction("right")

                if event.key == game.settings.controls.value["LEFT"]:
                    game.player.update_direction("left")

        return False

    def handle_cheats(self, game: Game) -> None:
        """Handle the cheats activated by the user"""
        if Cheat.EXTRA_LIVES in game.settings.cheats:
            game.player.lives = 999

        if Cheat.INCREASE_SPEED in game.settings.cheats:
            game.player.speed = 8.0

        # if Cheat.SKIP_LEVEL in game.settings.cheats:
        #     pass

    def update(self, game: Game, dt: float) -> None:
        """Update the game state, check for collisions,
        update the player and the ghosts"""
        # If the player is dead,
        # it will wait for the post death timer to end
        # before resuming the player
        if game.post_death_timer > 0.0:
            game.post_death_timer -= dt
            return

        # if the player made a kill,
        # it will wait for the post kill timer to end
        # before resuming the game
        if game.post_kill_timer > 0.0:
            game.post_kill_timer -= dt
            if game.post_kill_timer <= 0.0:
                game.kill_location.clear()
            return

        # if the player is alive and there is still time remaining,
        # it will update the player and the ghosts
        if game.player.is_alive() and game.time_remaining > 0.0:
            game.time_remaining -= dt

            self.handle_cheats(game)

            # no_collision will allow the player to move through
            # walls if the cheat is activated
            no_collision = (True
                            if Cheat.NO_COLLISIONS in game.settings.cheats
                            else False)

            # move player and check for collisions
            player_cell = game.player.move(dt, no_collision)
            game.check_ghost_collision()

            # verif if player is still alive
            if not game.player.is_alive():
                game.state = LostState()
                return

            for ghost in game.ghosts:
                # move each ghost
                ghost.move(dt)

                # check for collisions with the player
                game.check_ghost_collision()

                # verif if player is still alive
                if not game.player.is_alive():
                    game.state = LostState()
                    return

                # update ghost path if the player changed cell
                if not ghost.path or ghost.path[-1] != player_cell:
                    ghost.update_path(
                        player_cell,
                        game.player.direction,
                        game.my_map,
                    )

            # check if the player eat a pacgum
            game.pacgum_eaten(player_cell)

            # check if the player won the game
            if game.victory():
                game.state = VictoryState()

        else:
            game.state = LostState()

    def render(self, game: Game, screen: pygame.Surface) -> None:
        """Render the game background, the player, the ghosts and the points"""
        game.layer_renderer.render_game_background(screen, game)

        game.pacman_renderer.render(screen, game.player)
        for ghost in game.ghosts:
            game.ghosts_renderer.render(screen, ghost)

        game.layer_renderer.render_kill_points(screen, game)
