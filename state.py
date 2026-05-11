from typing import Any
import pygame


class MenuState():
    pass


class GameState():
    def handle_input(self, events: list[Any], game: Any) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True

                if event.key == game.settings.controls.value["UP"]:
                    game.player.update_direction("up", game.my_map)
                if event.key == game.settings.controls.value["DOWN"]:
                    game.player.update_direction("down", game.my_map)
                if event.key == game.settings.controls.value["RIGHT"]:
                    game.player.update_direction("right", game.my_map)
                if event.key == game.settings.controls.value["LEFT"]:
                    game.player.update_direction("left", game.my_map)

        return False


class PauseState():
    pass
