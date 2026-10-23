from __future__ import annotations

from typing import Sequence

import matplotlib.pyplot as plt
import networkx as nx

from .graph_builder import build_maze_graph
from .models import Maze, SearchResult


def _base_positions(rows: int, cols: int) -> dict[tuple[int, int], tuple[float, float]]:
    return {(row, col): (col, -row) for row in range(rows) for col in range(cols)}


def _draw_grid(ax, maze: Maze, explored: set[tuple[int, int]] | None = None, path: set[tuple[int, int]] | None = None) -> None:
    graph = build_maze_graph(maze.matrix)
    pos = _base_positions(maze.rows, maze.cols)
    nx.draw_networkx_edges(graph, pos=pos, ax=ax, edge_color="lightgray", width=1.3, alpha=0.8)
    for row_index, row in enumerate(maze.matrix):
        for col_index, value in enumerate(row):
            cell = (row_index, col_index)
            if value == 1:
                color = "dimgray"
            elif cell in (explored or set()):
                color = "lightblue"
            elif cell in (path or set()):
                color = "orange"
            else:
                color = "white"
            ax.add_patch(plt.Rectangle((col_index - 0.5, -row_index - 0.5), 1, 1, facecolor=color, edgecolor="black"))

    ax.scatter([maze.start[1]], [-maze.start[0]], color="green", s=180, label="Start")
    ax.scatter([maze.goal[1]], [-maze.goal[0]], color="red", s=180, label="Goal")
    ax.set_xlim(-0.5, maze.cols - 0.5)
    ax.set_ylim(-maze.rows + 0.5, 0.5)
    ax.set_aspect("equal")
    ax.set_xticks(range(maze.cols))
    ax.set_yticks(range(-maze.rows + 1, 1))
    ax.set_yticklabels(list(range(maze.rows - 1, -1, -1)))
    ax.set_xticklabels(range(maze.cols))
    ax.set_title(f"{maze.name}")
    ax.legend(loc="upper right")


def draw_maze_overview(maze: Maze, *, title: str | None = None) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7, 7))
    _draw_grid(ax, maze)
    ax.set_title(title or f"Maze Overview: {maze.name}")
    fig.tight_layout()
    return fig


def draw_search_result(maze: Maze, result: SearchResult, *, title: str | None = None) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7, 7))
    explored = set(result.explored_order)
    path = set(result.path)
    _draw_grid(ax, maze, explored=explored, path=path)
    ax.set_title(title or f"{result.algorithm} Search: {maze.name}")
    fig.tight_layout()
    return fig


def draw_comparison(maze: Maze, bfs_result: SearchResult, dfs_result: SearchResult) -> plt.Figure:
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    _draw_grid(axes[0], maze, explored=set(bfs_result.explored_order), path=set(bfs_result.path))
    _draw_grid(axes[1], maze, explored=set(dfs_result.explored_order), path=set(dfs_result.path))
    axes[0].set_title(f"BFS: {maze.name}")
    axes[1].set_title(f"DFS: {maze.name}")
    fig.tight_layout()
    return fig


def animate_search(maze: Maze, result: SearchResult, *, delay: float = 0.2) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7, 7))
    explored_so_far: set[tuple[int, int]] = set()
    for node in result.explored_order:
        explored_so_far.add(node)
        ax.clear()
        _draw_grid(ax, maze, explored=explored_so_far, path=set(result.path))
        ax.set_title(f"{result.algorithm} Exploration: {maze.name}")
        fig.canvas.draw_idle()
        plt.pause(delay)
    return fig


def show_figure(fig: plt.Figure, *, filename: str | None = None) -> None:
    if filename:
        fig.savefig(filename, dpi=200, bbox_inches="tight")
    try:
        plt.show(block=False)
    except Exception:
        if filename:
            print(f"Figure saved to {filename}")
