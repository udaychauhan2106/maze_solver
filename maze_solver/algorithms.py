from __future__ import annotations

import time
from collections import deque
from typing import Optional, Sequence

from .maze import validate_maze_inputs
from .models import SearchResult

DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def _reconstruct_path(
    parent_map: dict[tuple[int, int], Optional[tuple[int, int]]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]]:
    path: list[tuple[int, int]] = []
    current: Optional[tuple[int, int]] = goal
    while current is not None:
        path.append(current)
        if current == start:
            break
        current = parent_map.get(current)
    path.reverse()
    return path


def _valid_neighbors(matrix: Sequence[Sequence[int]], cell: tuple[int, int]) -> list[tuple[int, int]]:
    row, col = cell
    neighbors: list[tuple[int, int]] = []
    for delta_row, delta_col in DIRECTIONS:
        next_row = row + delta_row
        next_col = col + delta_col
        if 0 <= next_row < len(matrix) and 0 <= next_col < len(matrix[0]):
            if matrix[next_row][next_col] != 1:
                neighbors.append((next_row, next_col))
    return neighbors


def bfs_shortest_path(
    matrix: Sequence[Sequence[int]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> SearchResult:
    """Run a manual breadth-first search for the shortest maze path."""
    validate_maze_inputs(matrix, start, goal)
    if start == goal:
        return SearchResult(
            algorithm="BFS",
            path_found=True,
            path=[start],
            path_length=0,
            visited_nodes=1,
            expanded_nodes=1,
            execution_time=0.0,
            explored_order=[start],
            parent_map={start: None},
        )

    start_time = time.perf_counter()
    queue: deque[tuple[int, int]] = deque([start])
    visited = {start}
    parent_map: dict[tuple[int, int], Optional[tuple[int, int]]] = {start: None}
    explored_order: list[tuple[int, int]] = []

    while queue:
        current = queue.popleft()
        explored_order.append(current)
        if current == goal:
            break
        for neighbor in _valid_neighbors(matrix, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent_map[neighbor] = current
                queue.append(neighbor)

    elapsed = time.perf_counter() - start_time
    if goal not in parent_map:
        path: list[tuple[int, int]] = []
        found = False
    else:
        path = _reconstruct_path(parent_map, start, goal)
        found = path and path[-1] == goal

    return SearchResult(
        algorithm="BFS",
        path_found=found,
        path=path,
        path_length=len(path) - 1 if found else 0,
        visited_nodes=len(visited),
        expanded_nodes=len(explored_order),
        execution_time=elapsed,
        explored_order=explored_order,
        parent_map=parent_map,
    )


def dfs_explore_path(
    matrix: Sequence[Sequence[int]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> SearchResult:
    """Run a manual depth-first search to explore the maze and attempt a route."""
    validate_maze_inputs(matrix, start, goal)
    if start == goal:
        return SearchResult(
            algorithm="DFS",
            path_found=True,
            path=[start],
            path_length=0,
            visited_nodes=1,
            expanded_nodes=1,
            execution_time=0.0,
            explored_order=[start],
            parent_map={start: None},
        )

    start_time = time.perf_counter()
    stack = [start]
    visited = {start}
    parent_map: dict[tuple[int, int], Optional[tuple[int, int]]] = {start: None}
    explored_order: list[tuple[int, int]] = []

    while stack:
        current = stack.pop()
        explored_order.append(current)
        if current == goal:
            break
        neighbors = _valid_neighbors(matrix, current)
        neighbors.sort()  # Deterministic order to make exploration stable.
        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                visited.add(neighbor)
                parent_map[neighbor] = current
                stack.append(neighbor)

    elapsed = time.perf_counter() - start_time
    if goal not in parent_map:
        path = []
        found = False
    else:
        path = _reconstruct_path(parent_map, start, goal)
        found = path and path[-1] == goal

    return SearchResult(
        algorithm="DFS",
        path_found=found,
        path=path,
        path_length=len(path) - 1 if found else 0,
        visited_nodes=len(visited),
        expanded_nodes=len(explored_order),
        execution_time=elapsed,
        explored_order=explored_order,
        parent_map=parent_map,
    )
