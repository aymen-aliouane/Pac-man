import pygame

from typing import Any
from components.settings import DisplaySettings
from maze.draw_maze import build_maze_layer
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
        self.player_level: pygame.Surface = pygame.image.load(
            "sprite/other/cherry.png"
        )
        self.player_lives: pygame.Surface = pygame.image.load(
            "sprite/other/pacman_0.png"
        )
        self.player_lives = pygame.transform.scale(
            self.player_lives,
            (self.settings.cell_size // 2, self.settings.cell_size // 2),
        )
        self.player_level = pygame.transform.scale(
            self.player_level,
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

        self.additional_game_info_layer: pygame.Surface = pygame.Surface(
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

    def update_maze_layer(self, maze: list[list[int]]) -> None:
        """Update the maze layer,
        it will be called when the player change level"""
        self.maze_layer = build_maze_layer(self.settings, maze)

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

    def render_kill_points(self, game: Any) -> None:
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
                self.additional_game_info_layer,
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
            self.additional_game_info_layer,
            (self.settings.margin_left, self.settings.margin_top * 2 / 3),
            str(game.score),
            (255, 255, 255),
        )

        self.settings.font.render_to(
            self.additional_game_info_layer,
            (self.settings.width - self.settings.margin_left
             - len(str(int(game.time_remaining))) * 13,
             self.settings.margin_top * 2 / 3),
            str(int(game.time_remaining)),
            (255, 255, 255),
        )

        # Render the player lives,
        # it will be displayed at the bottom right of the screen
        for i in range(game.player.lives):
            live_size = self.player_lives.get_width() + 5
            self.additional_game_info_layer.blit(
                self.player_lives,
                (
                    self.settings.margin_left
                    + self.settings.cell_size * len(game.my_map[0])
                    - (i * live_size) - live_size,
                    self.settings.margin_top
                    + self.settings.cell_size * len(game.my_map)
                    + live_size // 2,
                ),
            )

        # display a cherry for each level, bottome left of the screen
        for i in range(game.level):
            level_size = self.player_level.get_width() + 5
            self.additional_game_info_layer.blit(
                self.player_level,
                (
                    self.settings.margin_left
                    + (i * level_size),
                    self.settings.margin_top
                    + self.settings.cell_size * len(game.my_map)
                    + level_size // 2,
                ),
            )

    def render_score_bar(self, game: Any) -> None:
        """Display the score bar, with the number of pacgums eaten
        and the total number of pacgums, it will be displayed
        in the additional info layer"""
        pygame.draw.rect(
            self.additional_game_info_layer,
            (255, 255, 0, 150),
            (self.settings.margin_left * 0.1,
             self.settings.margin_top,
             self.settings.margin_left * 0.8,
             self.settings.height - self.settings.margin_top * 2),
            border_radius=10,
            )

        self.settings.font.render_to(
            self.additional_game_info_layer,
            (self.settings.margin_left * 0.15, self.settings.height * 0.11),
            "Pacgums eaten",
            (0, 0, 0),
        )
        self.settings.font.render_to(
            self.additional_game_info_layer,
            (self.settings.margin_left * 0.15, self.settings.height * 0.17),
            f"{game.pacgums_score}/{game.pacgums_total}",
            (0, 0, 0),
        )
        pygame.draw.rect(
            self.additional_game_info_layer,
            (0, 0, 0),
            (self.settings.margin_left * 0.15,
             self.settings.height * 0.2,
             self.settings.margin_left * 0.7,
             self.settings.margin_top * 0.2), border_radius=10,
        )
        pygame.draw.rect(
            self.additional_game_info_layer,
            (33, 33, 222),
            (self.settings.margin_left * 0.16,
             self.settings.height * 0.205,
             self.settings.margin_left
             * (game.pacgums_score * 0.68 / game.pacgums_total),
             self.settings.margin_top * 0.1), border_radius=10,
        )

    def render_achievements(self, game: Any) -> None:
        """
        Render the achievements of the player, it will be displayed in the
        additional info layer
        """

        # Draw semi-transparent achievements box
        box_x = int(self.settings.margin_left * 0.15)
        box_y = int(self.settings.height * 0.3)
        box_w = int(self.settings.margin_left * 0.7)
        box_h = int(self.settings.height * 0.6)
        padding = 8

        pygame.draw.rect(
            self.additional_game_info_layer,
            (0, 0, 0, 100),
            (box_x, box_y, box_w, box_h),
            border_radius=10,
        )

        # Title
        title_x = box_x + int(box_w * 0.18)
        title_y = box_y + padding
        self.settings.font.render_to(
            self.additional_game_info_layer,
            (title_x, title_y),
            "Achievements",
            (100, 100, 252),
        )

        # Compute available vertical space and per-item height (title + desc)
        title_height = int(self.settings.font.get_sized_height(0))
        desc_height = int(self.settings.small_font.get_sized_height(0))
        item_height = title_height + desc_height + 6

        current_y = title_y + title_height + 6
        available_space = box_y + box_h - padding - current_y
        if available_space < 0:
            # No space to draw items
            return

        # Calculate how many achievement items we can draw
        max_items = max(0, available_space // item_height)

        # Convert achievements to a list for slicing
        ach_list = list(game.achievements.items())
        total = len(ach_list)

        # Render only up to max_items achievements
        for idx in range(min(max_items, total)):
            achievement, description = ach_list[idx]
            color = ((252, 150, 150)
                     if "ghost" in description.lower()
                     else (150, 150, 252))

            pygame.draw.rect(
                self.additional_game_info_layer,
                color,
                (box_x + box_w * 0.01,
                 current_y - 2,
                 box_w * 0.96,
                 item_height - 4), border_radius=2,
            )

            self.settings.font.render_to(
                self.additional_game_info_layer,
                (box_x + box_w * 0.02, current_y),
                f"{achievement}",
                (0, 0, 0),
            )
            current_y += title_height + 2
            self.settings.small_font.render_to(
                self.additional_game_info_layer,
                (box_x + box_w * 0.02, current_y),
                f"{description}",
                (0, 0, 0),
            )
            current_y += desc_height + 4

        # If there are more achievements than space,
        # show a small "+N more" indicator
        if total > max_items:
            remaining = total - max_items
            more_text = f"+{remaining} more"
            # draw at bottom-right of the box with small font
            more_x = box_x + box_w - padding
            - self.settings.small_font.get_rect(more_text).width
            more_y = box_y + box_h - padding - desc_height
            # fallback in case get_rect isn't available

            self.settings.small_font.render_to(
                self.additional_game_info_layer,
                (more_x, more_y),
                more_text,
                (200, 200, 200),
                )

    def render_ghost_status(self, game: Any) -> None:
        """Render the status of the ghosts, each one have it's
        own box with its name, a title and a description of its behavior"""

        box_size = ((self.settings.height - self.settings.margin_top * 2) / 4)
        box_padding = ((self.settings.height - self.settings.margin_top * 2)
                       - (box_size * 3.55))

        y_pos = float(self.settings.margin_top)
        x_pos = self.settings.width - self.settings.margin_left * 0.9

        for ghost in game.ghosts:
            if ghost.name == "blinky":
                color = (225, 80, 40)
                title = "The Inevitable"
                description = ["always targets Pacman", "directly."]
            elif ghost.name == "pinky":
                color = (235, 105, 180)
                title = "Already there"
                description = ["targets 2 tile ahead ", "of Pacman."]
            elif ghost.name == "inky":
                color = (0, 225, 225)
                title = "Somehow works"
                description = ["uses a complex algorithm",
                               "to determine it's targets.",
                               "(random...)"]
            elif ghost.name == "clyde":
                color = (235, 165, 0)
                title = "The weird guy"
                description = ["Flee Pacman when close",
                               "and chases when far."]
            frame = game.ghosts_renderer.get_ghost_frame(ghost.name, "normal",
                                                         (0, 0), (0, 0), 0)
            frame = pygame.transform.scale(frame, (box_size * 0.4,
                                                   box_size * 0.4))

            pygame.draw.rect(
                self.additional_game_info_layer,
                (100, 100, 100),
                (x_pos - box_size * 0.05,
                 y_pos - box_size * 0.05,
                 self.settings.margin_left * 0.74,
                 box_size - box_padding * 0.15),
                border_radius=5,
            )
            pygame.draw.rect(
                self.additional_game_info_layer,
                color,
                (x_pos,
                 y_pos,
                 self.settings.margin_left * 0.7,
                 box_size - box_padding),
                border_radius=5,
            )

            self.additional_game_info_layer.blit(
                frame,
                (x_pos + box_size * 0.15,
                 y_pos + box_size * 0.09),)

            self.settings.font.render_to(
                self.additional_game_info_layer,
                (x_pos + box_size * 0.9,
                 y_pos + box_size * 0.1),
                ghost.name,
                (255, 255, 255),
            )
            self.settings.font.render_to(
                self.additional_game_info_layer,
                (x_pos + box_size * 0.65,
                 y_pos + box_size * 0.3),
                title,
                (255, 255, 255),
            )

            for i, desc in enumerate(description):
                self.settings.small_font.render_to(
                    self.additional_game_info_layer,
                    (x_pos + box_size * 0.1,
                     y_pos + box_size * (0.6 + i * 0.1)),
                    desc,
                    (255, 255, 255),
                )

            y_pos += box_size

    def render_game_additional_info(self, main_layer: pygame.Surface,
                                    game: Any) -> None:
        """Render the additional info of the game"""
        self.additional_game_info_layer.fill((0, 0, 0, 0))

        self.render_ghost_status(game)

        self.render_score_bar(game)
        self.render_achievements(game)

        pygame.draw.rect(
            self.additional_game_info_layer,
            (255, 255, 0, 150),
            (self.settings.margin_left * 0.1,
             self.settings.margin_top * 0.1,
             self.settings.margin_left * 0.5,
             self.settings.margin_top * 0.7),
            border_radius=10,
         )
        self.settings.small_font.render_to(
            self.additional_game_info_layer,
            (self.settings.margin_left * 0.15,
             self.settings.margin_top * 0.16),
            "Press 'p' to pause",
            (0, 0, 0),
        )
        self.settings.small_font.render_to(
            self.additional_game_info_layer,
            (self.settings.margin_left * 0.15,
             self.settings.margin_top * 0.5),
            "Press 'esc' to menu",
            (0, 0, 0),
        )

        self.render_kill_points(game)

        main_layer.blit(self.additional_game_info_layer, (0, 0))

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
