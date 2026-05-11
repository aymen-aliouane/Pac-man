class PacMan:
    def __init__(self, x, y):
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
        if (movement == (0, -1) and maze[self.y][self.x] & 1 or
                movement == (1, 0) and maze[self.y][self.x] & 2 or
                movement == (0, 1) and maze[self.y][self.x] & 4 or
                movement == (-1, 0) and maze[self.y][self.x] & 8):
            print("there is a wall there with movement", movement)
            return True
        print("no wall here with movement", movement)
        return False

    def update_direction(self, movement, maze):
        movement_coordinate = self.movement_relation[movement]

        if not self.is_wall(movement_coordinate, maze):
            self.next_direction = movement_coordinate

    # def move(self, maze: list[list[int]]):


####  bug here
        
        


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
