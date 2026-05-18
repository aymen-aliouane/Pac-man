import pygame

from typing import Any
from components.settings import DisplaySettings
from maze.pacgums import update_pacgum_layer


class LayerRenderer:
    """Class rendering the different layers of the game,
        ex:
            main menu
            game background
            pause menu
            game over screen
            victory screen
    """

    def __init__(self, settings: DisplaySettings,
                 maze_layer: pygame.Surface) -> None:
        """Init the class, load the different layers of the game,
        Each attribute, except the maze_layer and settings,
        are a pygame.Surface object,
        it will be used to render the different layers of the game

        Attributes:
            settings (DisplaySettings): the settings of the displaying
            maze_layer (pygame.Surface): the layer of the maze
        """
        self.settings = settings
        self.maze_layer = maze_layer

        # load the image of pacman lives,
        # and scale it to the cell size
        self.player_lives: pygame.Surface = pygame.image.load(
            "sprite/other/pacman_0.png"
        )
        self.player_lives = pygame.transform.scale(
            self.player_lives,
            (self.settings.cell_size // 2, self.settings.cell_size // 2),
        )

        # Initialize the layers of the game,
        # some are transparent, and some are not, it depends on the layer.
        self.pacgums_layer: pygame.Surface = pygame.Surface(
            (settings.width, settings.height), pygame.SRCALPHA
        )

        self.points_layer: pygame.Surface = pygame.Surface(
            (settings.width, settings.height), pygame.SRCALPHA
        )

        self.main_menue_layer: pygame.Surface = pygame.Surface(
            (settings.width, settings.height)
        )

        self.pause_layer: pygame.Surface = pygame.Surface(
            (settings.width, settings.height), pygame.SRCALPHA
        )

        self.game_over_layer: pygame.Surface = pygame.Surface(
            (settings.width, settings.height), pygame.SRCALPHA
        )

        self.victory_layer: pygame.Surface = pygame.Surface(
            (settings.width, settings.height), pygame.SRCALPHA
        )

    def render_game_background(self, main_layer: pygame.Surface,
                               game: Any) -> None:
        """render the game background"""
        update_pacgum_layer(
            self.pacgums_layer,
            game.pacgums,
            self.settings.cell_size,
            self.settings.margin_left,
            self.settings.margin_top,
        )

        main_layer.blit(self.maze_layer, (0, 0))
        main_layer.blit(self.pacgums_layer, (0, 0))

    def render_kill_points(self, main_layer: pygame.Surface,
                           game: Any) -> None:
        """
        render the points when a ghost is killed, the score, time remaining
        and the player lives
        """
        if game.kill_location:
            # display the points at the location of the killed ghost,
            # it will be displayed for 1 second
            # before being removed from the list
            cell = game.kill_location[0]

            self.settings.font.render_to(
                main_layer,
                (
                    (cell[0] * self.settings.cell_size)
                    + self.settings.margin_left
                    - 4,
                    (cell[1] * self.settings.cell_size)
                    + self.settings.margin_top
                    - 4,
                ),
                str(game.settings.point_per_ghost),
                (255, 255, 255),
            )

        # Write the score and time remaining
        self.settings.font.render_to(
            main_layer,
            (10, 10),
            str(game.score),
            (255, 255, 255),
        )

        self.settings.font.render_to(
            main_layer,
            (self.settings.width - 100, 10),
            str(int(game.time_remaining)),
            (255, 255, 255),
        )

        # Render the player lives,
        # it will be displayed at the bottom right of the screen
        for i in range(game.player.lives):
            live_size = self.player_lives.get_width() + 5
            main_layer.blit(
                self.player_lives,
                (
                    self.settings.width - (i * live_size) - live_size,
                    self.settings.height - live_size,
                ),
            )

    def render_pause_background(
        self,
        main_layer: pygame.Surface,
        options: list[str],
        user_choice: int,
    ) -> None:
        """Render the pause menu background,
        with the options and the user choice"""
        self.pause_layer.fill((0, 0, 0, 0))
        pygame.draw.rect(
            self.pause_layer,
            (0, 0, 0, 0),
            (
                self.settings.width // 4,
                self.settings.height // 4,
                self.settings.width // 2,
                self.settings.height // 2,
            ),
        )

        main_layer.blit(self.pause_layer, (0, 0))
