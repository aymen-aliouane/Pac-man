import heapq
import math
import random
from typing import cast
from collections import deque


class PriorityQueue:
    """
    Class used to partially implement the A* algorithm,
    it is a wrapper around the heapq module
    """

    def __init__(self) -> None:
        """init the list of elements"""
        self.element: list[tuple[float, tuple[int, int]]] = []

    def is_empty(self) -> bool:
        """True if empty"""
        return not self.element

    def add(self, dist: float, tup: tuple[int, int]) -> None:
        """
        append an element to the list,
        the element is a tuple of the distance and the cell
        """
        heapq.heappush(self.element, (dist, tup))

    def get_element(self) -> tuple[float, tuple[int, int]]:
        """pop the first element, the element with the smallest distance
        """
        return heapq.heappop(self.element)


class Ghost:
    def __init__(self, name: str, pos: tuple[int, int]):
        """
        init the ghost with its name and its position

        Parameters:
            name (str): the name of the ghost, used to determine its behavior
            pos (tuple[int, int]): the initial position of the ghost

        Attributes:
            cell (tuple[int, int]): the current position of the ghost
            initial_corner (tuple[int, int]): the initial
                                              position (corner) of the ghost
            speed (float): the speed of the ghost
            move_timer (float): the timer used to move the ghost smoothly
            alive (bool): True if the ghost is alive, False if it is dead
            frightened_timer (float): the timer used to determine how long
                                      the ghost is frightened
            path (deque[tuple[int, int]]): the path that the ghost
                                           is currently following
        """
        self.name = name
        self.cell = pos
        self.initial_corner = pos
        self.speed = 3.0
        self.move_timer = 0.0

        self.alive = True
        self.frightened_timer = 0.0
        self.scatter_timer = 0.0
        self.chase_timer = 10.0
        self.path: deque[tuple[int, int]] = deque()

    def get_path(
        self,
        objective: tuple[int, int],
        maze: list[list[int]],
    ) -> deque[tuple[int, int]]:
        """Return the path from the ghost's current position to the
        objective using A* algorithm

        Parameters:
            objective (tuple[int, int]): the position of the objective
            maze (list[list[int]]): maze of the game,
                                    used to verify the movement
        """
        # init the priority queue with the ghost's current position
        # and its distance to the objective
        heap = PriorityQueue()
        heap.add(self.distance(self.cell, objective), self.cell)

        # the path dictionary will store cells in a child: parent format.
        # this will help us reconstruct the path from the objective
        # to the ghost's current position
        path: dict[tuple[int, int], tuple[int, int] | None] = {
            self.cell: None
            }
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        while not heap.is_empty():
            dist, actual_cell = heap.get_element()

            if actual_cell == objective:
                # break if we reached the objective
                break

            # iterate over the possible directions to move
            for direction in directions:
                # if a wall no wall in the direction,
                # we can move to the next cell
                if not self.is_wall(direction, actual_cell, maze):

                    # next cell is the current cell plus the direction
                    next_cell = (
                        actual_cell[0] + direction[0],
                        actual_cell[1] + direction[1],
                    )

                    # if next cell is already in the path,
                    # we have already visited it, so we skip it
                    if next_cell in path:
                        continue

                    # add the next cell to the priority queue
                    # with its distance to the objective
                    heap.add(self.distance(next_cell, objective), next_cell)

                    # add the next cell to the path with parent actual cell
                    path[next_cell] = actual_cell

        # after we reached the objective,
        # we can reconstruct the path from the objective
        end = objective
        final_path = []

        # we iterate from objective
        # until we reach the ghost's current position.
        while end != self.cell:
            # we append the current cell to the final path,
            # then we update the current cell to its parent in the path
            final_path.append(end)
            end = cast(tuple[int, int], path[end])

        # reverse the final path to switch from end->start to start->end
        final_path.reverse()

        return deque(final_path)

    def update_path(
        self,
        objective: tuple[int, int],
        direction: tuple[int, int],
        maze: list[list[int]],
    ) -> None:
        """Update the path of the ghost based on its state and it's behavior

        Parameters:
            objective (tuple[int, int]): the position of the pacman
            direction (tuple[int, int]): the current direction of the pacman
            maze (list[list[int]]): the maze of the game,
                                    used to verify the movement
        """
        if not self.alive:
            # if the ghost is dead, it will go back to its initial corner,
            # and it will be alive again when it reaches it
            if self.path:
                return
            elif self.cell != self.initial_corner:
                self.path = self.get_path(self.initial_corner, maze)
            else:
                self.alive = True

        elif self.frightened_timer > 0.0:
            # if the ghost is frightened, it will move to a random position
            # in the maze.
            if self.path:
                return

            # update the path only if the ghost does not already have one.
            next_pos = (
                random.randint(0, len(maze[0]) - 1),
                random.randint(0, len(maze) - 1),
            )
            while maze[next_pos[1]][next_pos[0]] == 15:
                next_pos = (
                    random.randint(0, len(maze[0]) - 1),
                    random.randint(0, len(maze) - 1),
                )
            self.path = self.get_path(next_pos, maze)

        elif self.scatter_timer > 0.0:
            # if the ghost is in scatter mode,
            # it will move to its initial corner
            if self.path:
                return
            elif self.cell != self.initial_corner:
                self.path = self.get_path(self.initial_corner, maze)

        elif self.move_timer == 0.0:
            # if the ghost is not moving, or reached a cell,
            # we update its path based on its behavior
            if self.name == "blinky":
                # blinky will always chase pacman
                self.path = self.get_path(objective, maze)

            elif self.name == "pinky":
                # pinky will try to move to the second cell in front of pacman,
                # if it can't then it will move to pacman
                next_possible = (
                    objective[0] + direction[0] * 2,
                    objective[1] + direction[1] * 2,
                )
                if (
                    0 <= next_possible[0] <= len(maze[0]) - 1
                    and 0 <= next_possible[1] <= len(maze) - 1
                    and maze[next_possible[1]][next_possible[0]] != 15
                ):
                    self.path = self.get_path(next_possible, maze)
                else:
                    self.path = self.get_path(objective, maze)

            elif self.name == "clyde":
                # clyde will try to move to pacman if it is far from him,
                # if it is close to him, it will move to its initial corner
                if (
                    self.cell[0] - objective[0] >= 4
                    or self.cell[0] - objective[0] <= -4
                    or self.cell[1] - objective[1] >= 4
                    or self.cell[1] - objective[1] <= -4
                ):
                    self.path = self.get_path(objective, maze)
                else:
                    self.path = self.get_path(self.initial_corner, maze)

            elif self.name == "inky":
                # inky is the most unpredictable ghost,
                # it will try to move to a random position in the maze,
                # if it can't then it will move to pacman
                if self.path:
                    return
                next_pos = (
                    random.randint(0, len(maze[0]) - 1),
                    random.randint(0, len(maze) - 1),
                )
                if maze[next_pos[1]][next_pos[0]] != 15:
                    self.path = self.get_path(next_pos, maze)
                else:
                    self.path = self.get_path(objective, maze)

    def update_state(self) -> None:
        """
        Update the state of the ghost,
        it will update the speed of the ghost based on its state
        """
        if self.frightened_timer > 0.0:
            self.speed = 2.0
        elif not self.alive:
            self.speed = 5.0
        else:
            self.speed = 3.0
            self.frightened_timer = 0.0

    def move(self, dt: float) -> tuple[int, int]:
        """
        Move the ghost in the maze based on its path,
        then return the current cell of the ghost after the movement
        """
        if not self.path:
            # if there is no path, the ghost will stay in its current cell
            return self.cell

        # update the timer tp move ghost smoothly, it will move to next cell
        # when timer >= 1.0
        self.move_timer += dt * self.speed

        if self.move_timer >= 1.0:
            # the ghost will move to the next cell in the path
            self.move_timer = 0.0
            self.cell = self.path.popleft()

        # update ghost state
        self.update_state()

        return self.cell

    def is_wall(
        self,
        movement: tuple[int, int],
        cell: tuple[int, int],
        maze: list[list[int]],
    ) -> bool:
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

    def distance(self, start: tuple[int, int], end: tuple[int, int]) -> float:
        """Return the distance between two cells, used as heuristic for
        the A* algorithm
        """
        return math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)
