from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Sequence


@dataclass
class Maze:
    name: str
    matrix: Sequence[Sequence[int]]
    start: tuple[int, int]
    goal: tuple[int, int]
    description: str = ""

    @property
    def rows(self) -> int:
        return len(self.matrix)

    @property
    def cols(self) -> int:
        return len(self.matrix[0]) if self.matrix else 0

    def __post_init__(self) -> None:
        if not self.matrix:
            raise ValueError("Maze matrix cannot be empty.")
        if any(len(row) != self.cols for row in self.matrix):
            raise ValueError("Maze matrix must be rectangular.")

    def as_list(self) -> list[list[int]]:
        return [list(row) for row in self.matrix]

    def copy(self) -> "Maze":
        return Maze(
            name=self.name,
            matrix=[list(row) for row in self.matrix],
            start=self.start,
            goal=self.goal,
            description=self.description,
        )

    def __str__(self) -> str:
        return f"Maze({self.name}, {self.rows}x{self.cols}, start={self.start}, goal={self.goal})"


@dataclass
class SearchResult:
    algorithm: str
    path_found: bool
    path: list[tuple[int, int]]
    path_length: int
    visited_nodes: int
    expanded_nodes: int
    execution_time: float
    explored_order: list[tuple[int, int]] = field(default_factory=list)
    parent_map: dict[tuple[int, int], Optional[tuple[int, int]]] = field(default_factory=dict)

    def as_summary(self) -> str:
        status = "found" if self.path_found else "not found"
        return (
            f"{self.algorithm}: {status}. "
            f"Path length = {self.path_length}, "
            f"Visited = {self.visited_nodes}, Expanded = {self.expanded_nodes}, "
            f"Execution time = {self.execution_time:.6f}s"
        )
