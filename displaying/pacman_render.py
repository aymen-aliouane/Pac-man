import pygame

from components.settings import DisplaySettings
from game_logic.pacman import PacMan


class PacManRenderer:
    """
    Class displaying pacman on the screen,
    it will handle the animation of pacman and
    the rotation of pacman based on the direction
    """

    def __init__(self, settings: DisplaySettings):
        """Init the class,
        load the frames of pacman and
        set the angles for each direction

        Attributes:
            settings (DisplaySettings): the settings of the displaying
            angles (dict): containing the angles for each direction,
                            used to rotate the frames of pacman
            last_angle (int): the last angle of pacman,
                            used to rotate the frames of pacman when
                            not moving
            frames (list[pygame.Surface]): contain the frames of pacman,
                                            it will be used to animate pacman
        """
        self.settings = settings
        self.angles = {
            (0, 1): -90,
            (0, -1): 90,
            (1, 0): 0,
            (-1, 0): 180,
        }
        self.last_angle = 0
        self.frames = self.load_frames()

    def load_frames(self) -> list[pygame.Surface]:
        """load the frames of pacman, and scale them to the cell size"""
        frames = []
        for i in range(4):
            frame = pygame.image.load(f"sprite/other/pacman_{i}.png")
            frame = pygame.transform.scale(
                frame,
                (self.settings.cell_size // 2, self.settings.cell_size // 2),
            )
            frames.append(frame)
        return frames

    def translate_pos(self, tup: tuple[float, float]) -> tuple[float, float]:
        """translate the position of pacman from
        the cell coordinates to the pixel coordinates"""
        return (
            (
                tup[0] * self.settings.cell_size
                + self.settings.margin_left
                + self.settings.offset
                + self.settings.cell_size // 8
            ),
            tup[1] * self.settings.cell_size
            + self.settings.margin_top
            + self.settings.offset
            + self.settings.cell_size // 8,
        )

    def get_pacman_frame(
        self,
        cell_from: tuple[int, int],
        cell_to: tuple[int, int],
        move_timer: float,
    ) -> pygame.Surface:
        """
        Return the new frame of pacman to display,
        based on the movement direction of pacman and the move timer.
        """

        # get the direction of the movement, if there is a movement
        if cell_to != cell_from:
            direction = (cell_to[0] - cell_from[0], cell_to[1] - cell_from[1])
            self.last_angle = self.angles[direction]

        # get the frame of pacman based on the move timer,
        # used to animate pacman
        frame = self.frames[int(move_timer * len(self.frames))]

        # rotate the frame
        pacman = pygame.transform.rotate(frame, self.last_angle)

        return pacman

    def render(self, main_layer: pygame.Surface, pacman: PacMan) -> None:
        """render pacman on the main layer"""
        # get the new frame of pacman to display
        frame = self.get_pacman_frame(
            pacman.cell_from,
            pacman.cell_to,
            pacman.move_timer,
        )

        # debug to see the cell of pacman
        # cell = pygame.Surface((self.settings.cell_size,
        #                        self.settings.cell_size))
        # cell.fill((255, 0, 0))
        # main_layer.blit(
        #     cell,
        #     (pacman.cell_from[0] * self.settings.cell_size
        #      + self.settings.margin_left,
        #      pacman.cell_from[1] * self.settings.cell_size
        #      + self.settings.margin_top)
        #      )

        # blit to the main layer,
        # the position is calculated by lerping between
        # the cell_from and cell_to, based on the move timer,
        # to make the animation smoother
        main_layer.blit(
            frame,
            self.lerp(pacman.cell_from, pacman.cell_to, pacman.move_timer),
        )

    def lerp(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        t: float,
    ) -> tuple[float, float]:
        """lerp between two positions,
            will be used to make the animation smoother"""
        pos = (
            (start[0] + (end[0] - start[0]) * t),
            (start[1] + (end[1] - start[1]) * t),
        )
        pos = self.translate_pos(pos)
        return pos
