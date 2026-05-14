from game_logic.ghosts import Ghost
import pygame


class GhostRenderer:
    """Class handeling the animation of the characters (pacman and ghosts)"""
    def __init__(self, settings):
        self.settings = settings
        self.last_direction = {"inky": (0, 1),
                               "blinky": (0, 1),
                               "pinky": (0, 1),
                               "clyde": (0, 1)
                               }
        self.frames = {}
        for name in ["blinky", "inky", "pinky", "clyde"]:
            self.frames[name] = self.load_frames(name)

    def load_frames(self, name) -> dict[str, list[pygame.Surface]]:
        """load the frames of ghosts, and scale them to the cell size"""
        frames = {
            "up": [],
            "down": [],
            "left": [],
            "right": []
        }

        for direction in frames.keys():
            for i in range(2):
                frame = pygame.image.load(
                        f"sprite/{name}/{name}_{direction}_{i}.png"
                        )
                frame = pygame.transform.scale(frame,
                                            (self.settings.cell_size // 2,
                                            self.settings.cell_size // 2))
                frames[direction].append(frame)
        return frames

    def get_ghost_frame(self, name: str,
                        cell_from: tuple[int, int],
                        cell_to: tuple[int, int],
                        move_timer: float) -> pygame.Surface:
        """
        get pacman frame will return the new frame of pacman to display
        """
        if cell_from != cell_to:
            self.last_direction[name] = (cell_to[0] - cell_from[0],
                                         cell_to[1] - cell_from[1])

        str_direction = self.get_str_direction(self.last_direction[name])
        frames_len = len(self.frames[name][str_direction])

        ghost = self.frames[name][str_direction][int(move_timer * frames_len)]

        return ghost

    def render(self, main_layer: pygame.Surface, ghost: Ghost):
        """render pacman on the main layer"""
        next_cell = ghost.path[0] if ghost.path else ghost.cell

        frame = self.get_ghost_frame(ghost.name, ghost.cell, next_cell, ghost.move_timer)
        main_layer.blit(frame,
                        self.lerp(ghost.cell,
                                  next_cell,
                                  ghost.move_timer))

    def lerp(self, start: tuple[int, int], end: tuple[int, int], t: float) -> tuple[int, int]:
        """lerp between two positions, it will be used to make the animation smoother"""
        pos = ((start[0] + (end[0] - start[0]) * t),
                (start[1] + (end[1] - start[1]) * t))
        pos = self.translate_pos(pos)
        return pos

    def translate_pos(self, tup):
        """translate the position of pacman from the cell coordinates to the pixel coordinates"""
        return ((tup[0] * self.settings.cell_size + self.settings.margin_left + self.settings.offset + self.settings.cell_size // 8),
                 tup[1] * self.settings.cell_size + self.settings.margin_top + self.settings.offset + self.settings.cell_size // 8)

    def get_str_direction(self, direction: tuple[int, int]):
        translate = {
            (0, 1): "down",
            (0, -1): "up",
            (1, 0): "right",
            (-1, 0): "left",
        }
        return translate[direction]
