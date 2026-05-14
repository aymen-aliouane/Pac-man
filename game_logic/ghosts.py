import heapq
import math
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
        self.speed = 3.0
        self.move_timer = 0.0

        self.alive = True
        self.edible = False
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

    def update_path(self, objective: tuple[int, int], maze: list[list[int]]):
        if self.move_timer == 0.0:
            self.path = self.get_path(objective, maze)


    def move(self, dt: float) -> tuple[int, int]:
        if not self.path:
            return self.cell

        self.move_timer += dt * self.speed

        if self.move_timer >= 1.0:
            self.move_timer = 0.0
            self.cell = self.path.popleft()

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
