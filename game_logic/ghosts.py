import heapq
import math
import random
from collections import deque


class PriorityQueue:
    def __init__(self):
        self.element = []

    def is_empty(self):
        return not self.element

    def add(self, dist: int, tup: tuple[int ,int]):
        heapq.heappush(self.element, (dist, tup))

    def get_element(self):
        return heapq.heappop(self.element)


class Ghost:
    def __init__(self, name, pos: tuple[int, int]):
        self.name = name
        self.cell = pos
        self.initial_corner = pos
        self.speed = 3.0
        self.move_timer = 0.0

        self.alive = True
        self.frightened_timer = 0.0
        self.path: deque[tuple[int, int]] = []

    def get_path(self, objective: tuple[int, int], maze: list[list[int]]):
        heap = PriorityQueue()

        path = {self.cell: None}
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        heap.add(self.distance(self.cell, objective), self.cell)

        while not heap.is_empty():
            dist, actual_cell = heap.get_element()

            if actual_cell == objective:
                break

            for direction in directions:
                if not self.is_wall(direction, actual_cell, maze):

                    next_cell = (actual_cell[0] + direction[0], actual_cell[1] + direction[1])

                    if next_cell in path:
                        continue

                    heap.add(self.distance(next_cell, objective), next_cell)

                    path[next_cell] = actual_cell

        end = objective
        final_path = []

        while end != self.cell:
            final_path.append(end)
            end = path[end]

        final_path.reverse()

        return deque(final_path)

    def update_path(self, objective: tuple[int, int],
                    direction: tuple[int, int], maze: list[list[int]]):
        if not self.alive:
            if self.path:
                return
            elif self.cell != self.initial_corner:
                self.path = self.get_path(self.initial_corner, maze)
            else:
                self.alive = True

        elif self.frightened_timer > 0.0:
            if self.path:
                return

            next_pos = (random.randint(0, len(maze[0]) - 1), random.randint(0, len(maze) - 1))
            while maze[next_pos[1]][next_pos[0]] == 15:
                next_pos = (random.randint(0, len(maze[0]) - 1), random.randint(0, len(maze) - 1))

            self.path = self.get_path(next_pos, maze)


        elif self.move_timer == 0.0:
            if self.name == "blinky":
                self.path = self.get_path(objective, maze)

            elif self.name == "pinky":
                next_possible = (objective[0] + direction[0] * 2, objective[1] + direction[1] * 2)
                if (0 <= next_possible[0] <= len(maze[0]) - 1 and
                        0 <= next_possible[1] <= len(maze) - 1 and
                        maze[next_possible[1]][next_possible[0]] != 15):
                    self.path = self.get_path(next_possible, maze)
                else:
                    self.path = self.get_path(objective, maze)

            elif self.name == "clyde":
                if (self.cell[0] - objective[0] >= 4 or self.cell[0] - objective[0] <= -4 or
                        self.cell[1] - objective[1] >= 4 or self.cell[1] - objective[1] <= -4):
                    self.path = self.get_path(objective, maze)
                else:
                    self.path = self.get_path(self.initial_corner, maze)

            elif self.name == "inky":
                if self.path:
                    return
                next_pos = (random.randint(0, len(maze[0]) - 1), random.randint(0, len(maze) - 1))
                if maze[next_pos[1]][next_pos[0]] != 15:
                    self.path = self.get_path(next_pos, maze)
                else:
                    self.path = self.get_path(objective, maze)

    def update_state(self):
        if self.frightened_timer > 0.0:
            self.speed = 2.0
        elif not self.alive:
            self.speed = 5.0
        else:
            self.speed = 3.0
            self.frightened_timer = 0.0

    def move(self, dt: float) -> tuple[int, int]:
        if self.frightened_timer >= 0.0:
            self.frightened_timer -= dt
        if not self.path:
            return self.cell

        self.move_timer += dt * self.speed

        if self.move_timer >= 1.0:
            self.move_timer = 0.0
            self.cell = self.path.popleft()

        self.update_state()

        return self.cell


    def is_wall(self, movement, cell, maze):
        """
        verify if there is a wall in the given direction
        """
        x, y = cell
        if (movement == (0, -1) and maze[y][x] & 1 or
                movement == (1, 0) and maze[y][x] & 2 or
                movement == (0, 1) and maze[y][x] & 4 or
                movement == (-1, 0) and maze[y][x] & 8):
            return True
        return False


    def distance(self, start, end):
        return math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)
