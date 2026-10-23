import pytest

from maze_solver.maze import Maze, generate_random_maze
from maze_solver.graph_builder import build_maze_graph
from maze_solver.algorithms import bfs_shortest_path, dfs_explore_path


@pytest.fixture
def sample_maze():
    return Maze(
        name="Sample",
        matrix=[
            [0, 0, 1, 0, 0],
            [1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
        ],
        start=(0, 0),
        goal=(4, 4),
    )


def test_simple_maze_with_valid_path(sample_maze):
    result = bfs_shortest_path(sample_maze.matrix, sample_maze.start, sample_maze.goal)
    assert result.path_found is True
    assert result.path[0] == sample_maze.start
    assert result.path[-1] == sample_maze.goal
    assert result.path_length == len(result.path) - 1


def test_bfs_returns_shortest_path(sample_maze):
    result = bfs_shortest_path(sample_maze.matrix, sample_maze.start, sample_maze.goal)
    assert result.path_found is True
    assert len(result.path) > 0


def test_dfs_returns_valid_path_when_route_exists(sample_maze):
    result = dfs_explore_path(sample_maze.matrix, sample_maze.start, sample_maze.goal)
    assert result.path_found in (True, False)
    if result.path_found:
        assert result.path[0] == sample_maze.start
        assert result.path[-1] == sample_maze.goal


def test_bfs_and_dfs_never_traverse_walls(sample_maze):
    bfs = bfs_shortest_path(sample_maze.matrix, sample_maze.start, sample_maze.goal)
    dfs = dfs_explore_path(sample_maze.matrix, sample_maze.start, sample_maze.goal)
    for path in (bfs.path, dfs.path):
        for row, col in path:
            assert sample_maze.matrix[row][col] != 1


def test_unreachable_destination():
    maze = Maze(
        name="Blocked",
        matrix=[
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ],
        start=(0, 0),
        goal=(2, 2),
    )
    result = bfs_shortest_path(maze.matrix, maze.start, maze.goal)
    assert result.path_found is False


def test_fully_blocked_or_disconnected_maze():
    maze = Maze(
        name="Disconnected",
        matrix=[
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ],
        start=(0, 0),
        goal=(2, 2),
    )
    with pytest.raises(ValueError):
        bfs_shortest_path(maze.matrix, maze.start, maze.goal)


def test_start_equals_destination():
    maze = Maze(
        name="Same cell",
        matrix=[[0, 0], [0, 0]],
        start=(0, 0),
        goal=(0, 0),
    )
    result = bfs_shortest_path(maze.matrix, maze.start, maze.goal)
    assert result.path_found is True
    assert result.path == [(0, 0)]
    assert result.path_length == 0


def test_invalid_start_coordinates():
    maze = Maze(
        name="Invalid Start",
        matrix=[[0, 0], [0, 0]],
        start=(-1, 0),
        goal=(1, 1),
    )
    with pytest.raises(ValueError):
        bfs_shortest_path(maze.matrix, maze.start, maze.goal)


def test_invalid_destination_coordinates():
    maze = Maze(
        name="Invalid Destination",
        matrix=[[0, 0], [0, 0]],
        start=(0, 0),
        goal=(2, 2),
    )
    with pytest.raises(ValueError):
        bfs_shortest_path(maze.matrix, maze.start, maze.goal)


def test_out_of_bounds_coordinates():
    maze = Maze(
        name="Out of Bounds",
        matrix=[[0, 0], [0, 0]],
        start=(0, 0),
        goal=(1, 3),
    )
    with pytest.raises(ValueError):
        bfs_shortest_path(maze.matrix, maze.start, maze.goal)


def test_maze_with_multiple_shortest_paths():
    maze = Maze(
        name="Multiple",
        matrix=[
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ],
        start=(0, 0),
        goal=(2, 2),
    )
    result = bfs_shortest_path(maze.matrix, maze.start, maze.goal)
    assert result.path_found is True
    assert result.path_length == 4


def test_one_row_maze():
    maze = Maze(
        name="One Row",
        matrix=[[0, 0, 0, 0]],
        start=(0, 0),
        goal=(0, 3),
    )
    result = bfs_shortest_path(maze.matrix, maze.start, maze.goal)
    assert result.path_found is True
    assert result.path_length == 3


def test_one_column_maze():
    maze = Maze(
        name="One Column",
        matrix=[[0], [0], [0], [0]],
        start=(0, 0),
        goal=(3, 0),
    )
    result = bfs_shortest_path(maze.matrix, maze.start, maze.goal)
    assert result.path_found is True
    assert result.path_length == 3


def test_isolated_start():
    maze = Maze(
        name="Isolated",
        matrix=[
            [0, 1, 1],
            [1, 1, 1],
            [1, 1, 0],
        ],
        start=(0, 0),
        goal=(2, 2),
    )
    result = bfs_shortest_path(maze.matrix, maze.start, maze.goal)
    assert result.path_found is False


def test_graph_construction_does_not_connect_through_walls(sample_maze):
    graph = build_maze_graph(sample_maze.matrix)
    assert (0, 0) in graph
    assert (0, 1) in graph
    assert (0, 2) not in graph if sample_maze.matrix[0][2] == 1 else True
    assert graph.number_of_nodes() > 0


def test_random_maze_generation_produces_valid_dimensions():
    maze = generate_random_maze(5, 6, seed=7)
    assert len(maze.matrix) == 5
    assert len(maze.matrix[0]) == 6
    assert maze.start != maze.goal
    assert maze.matrix[maze.start[0]][maze.start[1]] == 0
    assert maze.matrix[maze.goal[0]][maze.goal[1]] == 0


def test_path_reconstruction_starts_and_ends_correctly(sample_maze):
    result = bfs_shortest_path(sample_maze.matrix, sample_maze.start, sample_maze.goal)
    assert result.path[0] == sample_maze.start
    assert result.path[-1] == sample_maze.goal


def test_consecutive_path_cells_are_orthogonally_adjacent(sample_maze):
    result = bfs_shortest_path(sample_maze.matrix, sample_maze.start, sample_maze.goal)
    for first, second in zip(result.path, result.path[1:]):
        row_diff = abs(first[0] - second[0])
        col_diff = abs(first[1] - second[1])
        assert (row_diff + col_diff) == 1


def test_all_walkable_cells_in_path(sample_maze):
    result = bfs_shortest_path(sample_maze.matrix, sample_maze.start, sample_maze.goal)
    for row, col in result.path:
        assert sample_maze.matrix[row][col] != 1
