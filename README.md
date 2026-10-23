# Maze Solver / Path Finder Using Graph Theory, BFS, DFS, and NetworkX

## Abstract
This project implements a maze-solving and path-finding application in Python using a matrix representation, NetworkX graph construction, manual Breadth-First Search (BFS), manual Depth-First Search (DFS), and Matplotlib visualizations. The system is designed as a clear academic mini project for Data Structures and Algorithms courses, where students can explain the relationship between the matrix, graph, traversal logic, and final visual output.

## Problem Statement
A maze can be represented as a grid where walls are blocked cells and open cells are walkable. To solve it effectively, the problem must be transformed into a graph model so that shortest-path analysis and exploration can be demonstrated. BFS guarantees the shortest path in an unweighted graph, while DFS explores deeply before backtracking. NetworkX is used to represent legal movement between cells, while Matplotlib visually highlights the maze, explored nodes, and output path.

## Objectives
- Represent a maze using a two-dimensional matrix.
- Convert the matrix into a NetworkX graph of walkable cells.
- Implement BFS manually using a queue and reconstruct the shortest path.
- Implement DFS manually using a stack and record exploration order.
- Compare BFS and DFS on identical inputs.
- Visualize the maze and results with Matplotlib.
- Package the project in a beginner-friendly but testable structure.

## Features
- Predefined maze selection.
- Random maze generation with valid start and goal coordinates.
- Matrix validation and boundary checking.
- Manual BFS and DFS implementations.
- Graph construction from matrix cells using orthogonal adjacency.
- Path reconstruction and metrics such as visited nodes, expanded nodes, and execution time.
- Grid-aligned Matplotlib visualization.
- Optional animation of exploration.

## Technologies Used
- Python 3.11+
- NumPy for convenient matrix handling and random generation support
- NetworkX for graph construction and edges
- Matplotlib for visual rendering
- Pytest for automated unit tests

## System Architecture
The project separates responsibilities into a small set of modules:

- maze.py: Maze validation, predefined sample mazes, and random generation.
- graph_builder.py: Conversion of a matrix to a NetworkX graph.
- algorithms.py: BFS, DFS, and path reconstruction.
- models.py: Data models for maze and search result objects.
- visualization.py: Grid-shaped maze rendering and exploration views.
- main.py: CLI entry point for menu-based interaction.

## Matrix and Graph Representation
A maze is stored as a matrix of integers:

- 0 = walkable
- 1 = wall
- start and goal are stored separately as coordinate tuples

From this matrix, a graph is created where each walkable cell is a node. Edges connect neighboring walkable cells up, down, left, and right. Diagonal movement is intentionally not allowed. This preserves a direct correspondence between cells and graph nodes while keeping the implementation easy to explain in a viva.

## BFS Explanation
BFS explores neighbors level by level. It uses a queue, a visited set, and a parent dictionary. When it reaches the goal, the parent chain is reversed to reconstruct the shortest path. Because each edge has equal cost in a grid maze, BFS guarantees the minimum number of moves.

## DFS Explanation
DFS uses a stack to travel as deeply as possible before backtracking. It maintains a visited set and parent links to reconstruct a route when a goal is found. DFS is useful for exploration but does not guarantee shortest paths in unweighted graphs.

## BFS and DFS Pseudocode

### BFS
```
queue = [start]
visited = {start}
parents = {start: None}
while queue is not empty:
    current = queue.pop_left()
    if current == goal:
        break
    for neighbor in valid_neighbors(current):
        if neighbor not in visited:
            visited.add(neighbor)
            parents[neighbor] = current
            queue.push(neighbor)
return reconstruct_path(parents, goal)
```

### DFS
```
stack = [start]
visited = {start}
parents = {start: None}
while stack is not empty:
    current = stack.pop()
    if current == goal:
        break
    for neighbor in sorted(valid_neighbors(current)):
        if neighbor not in visited:
            visited.add(neighbor)
            parents[neighbor] = current
            stack.push(neighbor)
return reconstruct_path(parents, goal)
```

## Time and Space Complexity
Let R = the number of rows and C = the number of columns.

- Matrix storage: O(R × C)
- Graph construction: O(R × C) because each cell is examined and each walkable cell has a bounded four-direction neighbor set
- BFS: O(V + E), which simplifies to O(R × C) on a rectangular grid
- DFS: O(V + E), which also simplifies to O(R × C)
- Auxiliary search space: O(V) for the queue/stack, parent map, and visited set

The graph representation adds additional memory compared with storing only the matrix, but it makes the connectivity structure explicit and is easier to visualize with NetworkX.

## Installation Instructions
From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Execution Instructions
Run the project from the workspace root:

```powershell
.\.venv\Scripts\python.exe main.py
```

Choose options from the menu to inspect a maze, run BFS/DFS, compare them, or visualize the search.

## Example Output
```text
========================================
       MAZE SOLVER / PATH FINDER
========================================

Menu:
1. Select a predefined maze
2. Generate a random maze
3. Display the maze
4. Find shortest path using BFS
5. Explore maze using DFS
6. Compare BFS and DFS
7. Visualize BFS exploration
8. Visualize DFS exploration
9. Animate algorithm exploration
10. Exit
```

## Visualization Explanation
The visualization uses a deterministic grid layout rather than a spring layout. Each node is drawn at its actual row and column coordinate. Walls are dark gray, walkable cells are white, explored cells are light blue, the path is orange, the start is green, and the goal is red. NetworkX supplies the graph structure and edges, while Matplotlib renders the final view.

## Testing Instructions
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Experimental Comparison
The project can be run on several sample mazes, including:
- Simple maze
- Maze with multiple routes
- Unreachable maze
- Start-goal adjacent maze
- Random maze

For each maze, the application records path length, visited count, expanded count, and time. BFS is expected to find the shortest path in an unweighted maze; DFS may find a valid route that is longer.

## Limitations
- The CLI is intentionally simple and console-based.
- Full animation is optional and depends on a GUI-capable Matplotlib backend.
- Random mazes are generated with guaranteed solvability but not necessarily with a specific difficulty level.

## Future Enhancements
- Add difficulty levels for random mazes.
- Add save/export functions for visualizations.
- Add a richer step-by-step animation with configurable delay and pause controls.
- Add a larger test set for more edge-case conditions.

## References
- Python documentation: https://docs.python.org/3/
- NetworkX documentation: https://networkx.org/documentation/stable/
- Matplotlib documentation: https://matplotlib.org/stable/contents.html
- pytest documentation: https://docs.pytest.org/en/stable/
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). Introduction to Algorithms. MIT Press.

## Role of Each Library
- Python: Core language and data structures.
- NumPy: Efficient matrix operations and random generation support.
- NetworkX: Graph representation, nodes, edges, and structural visualization.
- Matplotlib: Maze rendering and algorithm result display.
- pytest: Automated correctness tests.
