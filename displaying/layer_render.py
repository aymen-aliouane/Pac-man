from maze.pacgums import pacgums_displayer
import pygame



class LayerRenderer:
    """Class handeling the rendering of the layers (maze, pacgums, etc)"""
    def __init__(self, settings, maze_layer):
        self.settings = settings
        self.maze_layer = maze_layer

        self.pacgums_layer: pygame.Surface = None
        self.main_menue_layer: pygame.Surface = None
        self.pause_layer: pygame.Surface = None
        self.game_over_layer: pygame.Surface = None
        self.victory_layer: pygame.Surface = None

    def render(self, main_layer, game):
        """render the layers on the screen"""
        self.pacgums_layer = pacgums_displayer(game.pacgums,
                                               self.settings.width,
                                               self.settings.height,
                                               self.settings.cell_size,
                                               self.settings.margin_left,
                                               self.settings.margin_top)

        main_layer.blit(self.maze_layer, (0, 0))
        main_layer.blit(self.pacgums_layer, (0, 0))