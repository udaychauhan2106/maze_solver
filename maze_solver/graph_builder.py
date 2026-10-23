from __future__ import annotations

from typing import Sequence

import networkx as nx

from .maze import validate_maze_inputs


def build_maze_graph(matrix: Sequence[Sequence[int]]) -> nx.Graph:
    """Convert a maze matrix into an undirected NetworkX graph of walkable cells."""
    if not matrix or not matrix[0]:
        raise ValueError("Maze matrix cannot be empty.")
    if any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError("Maze matrix must be rectangular.")

    graph = nx.Graph()
    for row_index, row in enumerate(matrix):
        for col_index, value in enumerate(row):
            if value == 1:
                continue
            graph.add_node((row_index, col_index))

    for row_index, row in enumerate(matrix):
        for col_index, value in enumerate(row):
            if value == 1:
                continue
            for delta_row, delta_col in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_row = row_index + delta_row
                next_col = col_index + delta_col
                if 0 <= next_row < len(matrix) and 0 <= next_col < len(matrix[0]):
                    if matrix[next_row][next_col] != 1:
                        graph.add_edge((row_index, col_index), (next_row, next_col))
    return graph


def validate_graph_compatibility(matrix: Sequence[Sequence[int]], start: tuple[int, int], goal: tuple[int, int]) -> nx.Graph:
    validate_maze_inputs(matrix, start, goal)
    return build_maze_graph(matrix)
