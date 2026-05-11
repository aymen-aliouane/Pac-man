class PacMan:
    def __init__(self, x, y):
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
        self.x = x
        self.y = y
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.lives = 3
        self.movement_relation = {
            "up": (0, -1),
            "right": (1, 0),
            "down": (0, 1),
            "left": (-1, 0)
            }

    def is_wall(self, movement, maze):
        """
        verify if there is a wall in the given direction
        """
        if (movement == (0, -1) and maze[self.y][self.x] & 1 or
                movement == (1, 0) and maze[self.y][self.x] & 2 or
                movement == (0, 1) and maze[self.y][self.x] & 4 or
                movement == (-1, 0) and maze[self.y][self.x] & 8):
            return True
        return False

    def update_direction(self, movement):
        """
        Update the next direction of pacman
        """
        self.next_direction = self.movement_relation[movement]

    # def move(self, maze: list[list[int]]):        
        


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
