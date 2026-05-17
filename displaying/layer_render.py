from maze.pacgums import update_pacgum_layer
import pygame
import pygame.sysfont



class LayerRenderer:
    """Class handeling the rendering of the layers (maze, pacgums, etc)"""
    def __init__(self, settings, maze_layer):
        self.settings = settings
        self.maze_layer = maze_layer

        self.pacgums_layer: pygame.Surface = pygame.Surface((settings.width,
                                                             settings.height),
                                                             pygame.SRCALPHA)
        self.points_layer: pygame.Surface = pygame.Surface((settings.width,
                                                            settings.height),
                                                            pygame.SRCALPHA)

        self.main_menue_layer: pygame.Surface = None
        self.pause_layer: pygame.Surface = None
        self.game_over_layer: pygame.Surface = None
        self.victory_layer: pygame.Surface = None

    def render_background(self, main_layer, game):
        """render the layers on the screen"""
        update_pacgum_layer(self.pacgums_layer,
                            game.pacgums,
                            self.settings.cell_size,
                            self.settings.margin_left,
                            self.settings.margin_top)

        main_layer.blit(self.maze_layer, (0, 0))
        main_layer.blit(self.pacgums_layer, (0, 0))

    def render_points(self, main_layer, game):
        for ind, cell in enumerate(game.kill_location, start=1):
            self.settings.font.render_to(
                main_layer,
                ((cell[0] * self.settings.cell_size) + self.settings.margin_left - ind * 4,
                 (cell[1] * self.settings.cell_size) + self.settings.margin_top - ind * 4),
                 str(game.settings.point_per_ghost), (255, 255, 255))
