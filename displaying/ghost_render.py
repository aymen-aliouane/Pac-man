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
        for name in ["blinky", "inky", "pinky", "clyde", "dead", "frightened"]:
            self.frames[name] = self.load_frames(name)

    def load_frames(self, name) -> dict[str, list[pygame.Surface]]:
        """load the frames of ghosts, and scale them to the cell size"""
        frames = {
            "up": [],
            "down": [],
            "left": [],
            "right": []
        }

        if name not in {"dead", "frightened"}:
            for direction in frames.keys():
                for i in range(2):
                    frame = pygame.image.load(
                            f"sprite/{name}/{name}_{direction}_{i}.png"
                            )
                    frame = pygame.transform.scale(frame,
                                                (self.settings.cell_size // 2,
                                                self.settings.cell_size // 2))
                    frames[direction].append(frame)
        elif name == "dead":
            for direction in frames.keys():
                frame = pygame.image.load(
                        f"sprite/other/{name}_{direction}.png"
                        )
                frame = pygame.transform.scale(frame,
                                            (self.settings.cell_size // 1.7,
                                            self.settings.cell_size // 1.7))
                frames[direction].append(frame)
        elif name == "frightened":
            for i in range(2):
                frame = pygame.image.load(
                        f"sprite/other/{name}_{i}.png"
                        )
                frame = pygame.transform.scale(frame,
                                            (self.settings.cell_size // 1.8,
                                            self.settings.cell_size // 1.8))
                frames["up"].append(frame)
                frames["down"].append(frame)
                frames["left"].append(frame)
                frames["right"].append(frame)
        return frames

    def get_ghost_frame(self, name: str,
                        state: str,
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

        if state == "normal":
            ghost = self.frames[name][str_direction][int(move_timer * frames_len)]
        elif state == "frightened":
            ghost = self.frames["frightened"][str_direction][int(move_timer * frames_len)]
        elif state == "dead":
            ghost = self.frames["dead"][str_direction][0]

        return ghost

    def render(self, main_layer: pygame.Surface, ghost: Ghost):
        """render pacman on the main layer"""
        next_cell = ghost.path[0] if ghost.path else ghost.cell

        if not ghost.alive:
            frame = self.get_ghost_frame(ghost.name, "dead", ghost.cell, next_cell, ghost.move_timer)
        elif ghost.frightened_timer > 0.0:
            frame = self.get_ghost_frame(ghost.name, "frightened", ghost.cell, next_cell, ghost.move_timer)
        else:
            frame = self.get_ghost_frame(ghost.name, "normal", ghost.cell, next_cell, ghost.move_timer)

        # debug to see the cell of ghost
        # cell = pygame.Surface((self.settings.cell_size, self.settings.cell_size))
        # cell.fill((0, 255, 0))
        # main_layer.blit(cell, (ghost.cell[0] * self.settings.cell_size + self.settings.margin_left,
        #                        ghost.cell[1] * self.settings.cell_size + self.settings.margin_top))

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
