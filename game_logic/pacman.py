class PacMan:
    def __init__(self, x: int, y: int, maze: list[list[int]]):
        """
        Initialise the player

        Parameters:
            x (int): the x coordinate of the player in the maze
            y (int): the y coordinate of the player in the maze
            maze (list[list[int]]): maze of the game,
                                    used to verify the movement

        Attributes:
            cell_from (tuple[int, int]): cell where the player is coming from
            cell_to (tuple[int, int]): cell where the player is going to
            direction (tuple[int, int]): current direction of the player
            next_direction (tuple[int, int]): next direction of the player
            lives (int): number of lives of the player
            move_timer (float): timer used to move the player smoothly
            speed (float): speed of the player
            movement_relation (dict[str, tuple[int, int]]): relation between
                the movement and the direction
            """
        self.cell_from = (x, y)
        self.cell_to = (x, y)
        self.maze = maze
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.lives = 3
        self.move_timer = 0.0
        self.speed = 4.0
        self.movement_relation = {
            "up": (0, -1),
            "right": (1, 0),
            "down": (0, 1),
            "left": (-1, 0),
        }

    def is_wall(self, movement: tuple[int, int]) -> bool:
        """
        verify if there is a wall in the given direction
        """
        x, y = self.cell_from
        if (
            movement == (0, -1) and self.maze[y][x] & 1
            or movement == (1, 0) and self.maze[y][x] & 2
            or movement == (0, 1) and self.maze[y][x] & 4
            or movement == (-1, 0) and self.maze[y][x] & 8
        ):
            return True
        return False

    def is_border(self, movement: tuple[int, int]) -> bool:
        """
        verify if there is a border in the given direction
        Used when player activate no collision cheat,
        to prevent him from going out of the maze
        """
        x, y = self.cell_from
        if (
            movement == (0, -1) and y == 0
            or movement == (1, 0) and x == len(self.maze[0]) - 1
            or movement == (0, 1) and y == len(self.maze) - 1
            or movement == (-1, 0) and x == 0
        ):
            return True
        return False

    def update_direction(self, movement: str) -> None:
        """Update the next direction of pacman"""
        self.next_direction = self.movement_relation[movement]

    def is_alive(self) -> bool:
        """True if player is alive"""
        return self.lives > 0

    def move(self, dt: float, no_collision: bool) -> tuple[int, int]:
        """
        Move the player in the maze, if no_collision is True,
        the player can go through walls but not borders
        then return the current cell of the player after the movement

        Parameters:
            dt (float): the time since the last update,
                        used to move the player smoothly
            no_collision (bool): if True, the player can go
                                through walls but not borders
        """
        if self.cell_from == self.cell_to:
            # if the player reached the next cell,
            # update the direction and cell_to (destination cell)
            if no_collision:
                # if no collision is activated,
                # the player can go through walls but not borders
                if not self.is_border(self.next_direction):
                    self.direction = self.next_direction
                    self.cell_to = (
                        self.cell_from[0] + self.direction[0],
                        self.cell_from[1] + self.direction[1],
                    )
            else:
                if (
                    self.next_direction != self.direction
                    and not self.is_wall(self.next_direction)
                ):
                    # if there is no wall in the next direction,
                    # update the direction to the next direction
                    self.direction = self.next_direction

                if not self.is_wall(self.direction):
                    # Turn if there is no wall in the current direction
                    self.cell_to = (
                        self.cell_from[0] + self.direction[0],
                        self.cell_from[1] + self.direction[1],
                    )
        else:
            # if the player is moving, update the timer
            self.move_timer += dt * self.speed

        if self.move_timer >= 1.0:
            # move player to next cell and reset timer
            self.cell_from = self.cell_to
            self.move_timer -= 1.0

        return self.cell_from
