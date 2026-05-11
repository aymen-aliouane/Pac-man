from component import DisplaySettings
import pygame


class Animator:
    def __init__(self, settings: DisplaySettings):
        self.cell_size = settings.cell_size
        self.left_offset = settings.margin_left + settings.offset + 7
        self.top_offset = settings.margin_top + settings.offset + 7

    def get_pos(self, x, y) -> tuple[int, int]:
        return (x * self.cell_size + self.left_offset, y * self.cell_size + self.top_offset)


    def get_pacman_frame(self) -> pygame.Surface:
        pacman = pygame.image.load("sprite/other/pacman_1.png")
        pacman = pygame.transform.scale(pacman,
                                        (self.cell_size - 25,
                                         self.cell_size - 25))

        return pacman
