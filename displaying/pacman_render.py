from game_logic.characters import PacMan
import pygame


class PacManRenderer:
    """Class handeling the animation of the characters (pacman and ghosts)"""
    def __init__(self, settings):
        self.settings = settings
        self.angles = {
            (0, 1): -90,
            (0, -1): 90,
            (1, 0): 0,
            (-1, 0): 180,
        }
        self.last_angle = 0
        self.frames = self.load_frames()

    def load_frames(self):
        """load the frames of pacman, and scale them to the cell size"""
        frames = []
        for i in range(4):
            frame = pygame.image.load(f"sprite/other/pacman_{i}.png")
            frame = pygame.transform.scale(frame,
                                        (self.settings.cell_size / 4,
                                         self.settings.cell_size / 4))
            frames.append(frame)
        return frames

    def translate_pos(self, tup):
        """translate the position of pacman from the cell coordinates to the pixel coordinates"""
        return ((tup[0] * self.settings.cell_size + self.settings.margin_left + self.settings.offset + self.settings.cell_size // 8),
                 tup[1] * self.settings.cell_size + self.settings.margin_top + self.settings.offset + self.settings.cell_size // 8)

    def get_pacman_frame(self, cell_from: tuple[int, int], cell_to: tuple[int, int]) -> pygame.Surface:
        """
        get pacman frame will return the new frame of pacman to display
        """
        if cell_to != cell_from:
            direction = (cell_to[0] - cell_from[0],
                        cell_to[1] - cell_from[1])
            self.last_angle = self.angles[direction]

        pacman = pygame.image.load("sprite/other/pacman_1.png")
        pacman = pygame.transform.scale(pacman,
                                        (self.settings.cell_size // 2,
                                         self.settings.cell_size // 2))

        pacman = pygame.transform.rotate(pacman, self.last_angle)

        return pacman

    def render(self, main_layer: pygame.Surface, pacman: PacMan):
        """render pacman on the main layer"""
        frame = self.get_pacman_frame(pacman.cell_from, pacman.cell_to)
        main_layer.blit(frame,
                        self.lerp(pacman.cell_from,
                                       pacman.cell_to,
                                       pacman.move_timer))

    def lerp(self, start: tuple[int, int], end: tuple[int, int], t: float) -> tuple[int, int]:
        """lerp between two positions, it will be used to make the animation smoother"""
        pos = ((start[0] + (end[0] - start[0]) * t),
                (start[1] + (end[1] - start[1]) * t))
        pos = self.translate_pos(pos)
        return pos


