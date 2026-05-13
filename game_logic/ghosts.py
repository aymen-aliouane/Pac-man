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
