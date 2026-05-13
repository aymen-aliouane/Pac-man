class PacMan:
    def __init__(self, x, y, maze):
        """
        Initialise the player
        
        x: int = position x of the player
        y: int = position y of the player
        direction and next_direction: tuple[int, int] =
        current and next direction of the player default to right
        lives: int = remaining lives of the player
        movement_relation: dict[str, tuple[int, int]] = relation between the
        direction in str format and it's coordinate
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
            "left": (-1, 0)
            }

    def is_wall(self, movement):
        """
        verify if there is a wall in the given direction
        """
        x, y = self.cell_from
        if (movement == (0, -1) and self.maze[y][x] & 1 or
                movement == (1, 0) and self.maze[y][x] & 2 or
                movement == (0, 1) and self.maze[y][x] & 4 or
                movement == (-1, 0) and self.maze[y][x] & 8):
            return True
        return False

    def update_direction(self, movement):
        """
        Update the next direction of pacman
        """
        self.next_direction = self.movement_relation[movement]

    def is_alive(self):
        return self.lives > 0

    def move(self, dt: float) -> tuple[int, int]:
        if self.cell_from == self.cell_to:
            if (self.next_direction != self.direction and
                    not self.is_wall(self.next_direction)):
                self.direction = self.next_direction

            if not self.is_wall(self.direction):
                self.cell_to = (self.cell_from[0] + self.direction[0],
                                self.cell_from[1] + self.direction[1])
        else:
            self.move_timer += dt * self.speed

        if self.move_timer >= 1.0:
            self.cell_from = self.cell_to
            self.move_timer -= 1.0

        return self.cell_from



class Ghost:
    def __init__(self, name, x, y):
        self.name = name

        self.x = x
        self.y = y

        self.alive = True
        self.edible = False
        self.path = None

    def update_path(self, player_x, player_y):
        pass
