# Algorithm Notes

## 1. Maze Matrix
The maze is represented as a 2D list of integers:

- 0 = walkable cell
- 1 = wall
- start and goal are stored separately as coordinate tuples

This is useful because the matrix makes cell checks fast and clear, while the graph layer still supports pathfinding and visualization.

## 2. Converting the Matrix to a Graph
Each walkable cell becomes a node. An undirected edge is created between neighboring walkable cells that are orthogonally adjacent. The graph is built once and reused by visualization and analysis.

```text
For each cell (r, c):
    if matrix[r][c] != 1:
        create node (r, c)
    for each neighbor in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
        if neighbor is inside the maze and not a wall:
            add undirected edge between the current cell and neighbor
```

## 3. Breadth-First Search (BFS)
BFS explores all nodes at the current depth before moving deeper. This makes it ideal for shortest-path detection in an unweighted maze.

### BFS Pseudocode
```text
queue = deque([start])
visited = {start}
parents = {start: None}
while queue is not empty:
    current = queue.popleft()
    if current == goal:
        break
    for neighbor in valid_neighbors(current):
        if neighbor not in visited:
            visited.add(neighbor)
            parents[neighbor] = current
            queue.append(neighbor)
return reconstruct_path(parents, goal)
```

### Why BFS Finds the Shortest Path
Because BFS visits nodes in increasing distance from the start, the first time it reaches the goal, it has found the minimum number of moves.

## 4. Depth-First Search (DFS)
DFS goes down one branch as far as possible before backtracking. It uses a stack and maintains a parent relationship to reconstruct the route.

### DFS Pseudocode
```text
stack = [start]
visited = {start}
parents = {start: None}
while stack is not empty:
    current = stack.pop()
    if current == goal:
        break
    for neighbor in reversed(sorted(valid_neighbors(current))):
        if neighbor not in visited:
            visited.add(neighbor)
            parents[neighbor] = current
            stack.append(neighbor)
return reconstruct_path(parents, goal)
```

### Why DFS is Different
DFS is a good exploration strategy, but it does not prioritize shortest distance. The route it finds depends on neighbor ordering and the traversal path chosen.

## 5. Path Reconstruction
Once the goal is reached or the search ends, a parent map allows the algorithm to walk backward from the goal to the start and reverse the list.

```text
path = []
current = goal
while current is not None:
    path.append(current)
    current = parents[current]
return reversed(path)
```

## 6. Complexity Summary
- BFS: O(V + E)
- DFS: O(V + E)
- Matrix + graph storage: O(R × C)
- On a rectangular grid, these simplify to O(R × C) time and space per search.
