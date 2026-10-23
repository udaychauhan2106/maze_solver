from __future__ import annotations

import random
from typing import Iterable, Sequence

import numpy as np

from .models import Maze


def _is_valid_matrix(matrix: Sequence[Sequence[int]]) -> bool:
    if not matrix or not matrix[0]:
        return False
    width = len(matrix[0])
    return all(len(row) == width for row in matrix)


def validate_cell_coordinates(matrix: Sequence[Sequence[int]], coordinate: tuple[int, int]) -> tuple[int, int]:
    if not isinstance(coordinate, tuple) or len(coordinate) != 2:
        raise ValueError(f"Coordinate {coordinate} is invalid. Expected a (row, column) tuple.")
    row, col = coordinate
    if not isinstance(row, int) or not isinstance(col, int):
        raise ValueError(f"Coordinate {coordinate} contains non-integer values.")
    if row < 0 or row >= len(matrix) or col < 0 or col >= len(matrix[0]):
        raise ValueError(f"Coordinate {coordinate} is out of bounds for a {len(matrix)}x{len(matrix[0])} maze.")
    return row, col


def validate_maze_inputs(matrix: Sequence[Sequence[int]], start: tuple[int, int], goal: tuple[int, int]) -> None:
    if not _is_valid_matrix(matrix):
        raise ValueError("Maze must be a non-empty rectangular matrix.")
    start = validate_cell_coordinates(matrix, start)
    goal = validate_cell_coordinates(matrix, goal)
    if matrix[start[0]][start[1]] == 1:
        raise ValueError(f"Start cell {start} is a wall.")
    if matrix[goal[0]][goal[1]] == 1:
        raise ValueError(f"Goal cell {goal} is a wall.")


def get_predefined_mazes() -> dict[str, Maze]:
    mazes = {
        "Simple": Maze(
            name="Simple",
            matrix=[
                [0, 0, 1, 0, 0],
                [1, 0, 1, 0, 1],
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0],
            ],
            start=(0, 0),
            goal=(4, 4),
            description="Simple maze with an obvious solution.",
        ),
        "Exploration": Maze(
            name="Exploration",
            matrix=[
                [0, 0, 0, 1, 0, 0, 0],
                [1, 1, 0, 1, 0, 1, 0],
                [0, 0, 0, 0, 0, 1, 0],
                [0, 1, 1, 1, 0, 1, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [1, 1, 0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ],
            start=(0, 0),
            goal=(6, 6),
            description="Maze requiring more exploration and backtracking.",
        ),
        "Multiple Routes": Maze(
            name="Multiple Routes",
            matrix=[
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 1, 0],
                [1, 1, 0, 1, 0],
                [0, 0, 0, 0, 0],
            ],
            start=(0, 0),
            goal=(4, 4),
            description="Several possible routes exist to the destination.",
        ),
        "No Path": Maze(
            name="No Path",
            matrix=[
                [0, 1, 0, 0, 0],
                [1, 1, 1, 1, 0],
                [0, 0, 0, 1, 0],
                [0, 1, 0, 1, 0],
                [0, 1, 0, 0, 0],
            ],
            start=(0, 0),
            goal=(4, 4),
            description="The destination is disconnected from the start.",
        ),
        "Blocked Start": Maze(
            name="Blocked Start",
            matrix=[
                [1, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ],
            start=(0, 0),
            goal=(2, 2),
            description="The start cell is a wall and is invalid.",
        ),
        "Adjacent": Maze(
            name="Adjacent",
            matrix=[
                [0, 0, 0],
                [1, 1, 0],
                [0, 0, 0],
            ],
            start=(0, 0),
            goal=(0, 1),
            description="The start and goal are directly adjacent.",
        ),
    }
    return mazes


def generate_random_maze(rows: int, cols: int, *, seed: int | None = None, wall_density: float = 0.18) -> Maze:
    if rows <= 0 or cols <= 0:
        raise ValueError("Maze dimensions must be positive integers.")
    if not 0.0 <= wall_density <= 0.7:
        raise ValueError("Wall density must be between 0.0 and 0.7.")

    rng = random.Random(seed)
    matrix = np.zeros((rows, cols), dtype=int).tolist()
    start = (rng.randrange(rows), rng.randrange(cols))
    goal = (rng.randrange(rows), rng.randrange(cols))
    while goal == start:
        goal = (rng.randrange(rows), rng.randrange(cols))

    for r in range(rows):
        for c in range(cols):
            if (r, c) in {start, goal}:
                continue
            if rng.random() < wall_density:
                matrix[r][c] = 1

    # Guarantee solvability with a simple corridor between the start and goal.
    path = [start]
    current = start
    while current != goal:
        r, c = current
        options = []
        if r > 0:
            options.append((r - 1, c))
        if c < cols - 1:
            options.append((r, c + 1))
        if r < rows - 1:
            options.append((r + 1, c))
        if c > 0:
            options.append((r, c - 1))
        next_cell = min(options, key=lambda cell: abs(cell[0] - goal[0]) + abs(cell[1] - goal[1]))
        if next_cell in path:
            break
        path.append(next_cell)
        current = next_cell
    for row, col in path:
        matrix[row][col] = 0

    maze = Maze(name="Random Maze", matrix=matrix, start=start, goal=goal, description="Generated maze.")
    return maze
