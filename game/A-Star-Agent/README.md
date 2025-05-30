# A* agent

An autonomous agent that finds and walks the guaranteed shortest path from the player to the point on every move.
No learning is involved — the algorithm uses known map information (obstacle positions, grid size) to compute the optimal route at runtime.

* How to run

```bash
cd game
python AStarAgent/main.py
```

---

## What is A\*

A Star is a search algorithm that finds the shortest path between two points on a grid.
It is guaranteed to find the shortest path as long as its heuristic never over-estimates the remaining distance — a property called *admissibility*.

At every step it evaluates cells using the formula:

```code
f(n) = g(n) + h(n)

g(n)  — steps taken from the start to cell n
h(n)  — estimated steps remaining from n to the goal (Manhattan distance)
f(n)  — total estimated cost of a path through n
```

The cell with the lowest `f` value is always explored next.
Because `h` never over-estimates (Manhattan distance is exact for a 4-directional grid),
the first time A\* reaches the goal it has found the shortest possible path.

### Manhattan distance

The heuristic used is Manhattan distance:

```code
h(a, b) = |col_a - col_b| + |row_a - row_b|
```

This is the number of horizontal and vertical steps between two cells.
It is always admissible here because the player cannot move diagonally — every real path between two cells requires at least this many steps.

---

## File reference

### `astar.py`

Contains the full pathfinding algorithm. No pygame dependency — pure Python using only the standard library `heapq`.

**Public API:**

```python
from astar import find_path

path = find_path(start_cell, goal_cell, obstacle_cells)
# start_cell    : (col, row) — current player position
# goal_cell     : (col, row) — current point position
# obstacle_cells: set of (col, row) — impassable wall cells
#
# Returns: list of (col, row) from start (exclusive) to goal (inclusive)
#          Empty list if no path exists or start == goal
```

**Internal functions (not part of the public API):**

| Function | Purpose |
|---|---|
| `_manhattan(a, b)` | Computes the admissible heuristic between two cells |
| `_neighbours(cell, obstacle_cells)` | Yields the up to 4 walkable neighbours of a cell, filtering out walls and grid boundaries |

**Algorithm walkthrough:**

```python
push (f=h, g=0, start) onto the open set (min-heap)

while open set is not empty:
    pop cell with lowest f

    if cell already in closed set → skip (found via cheaper path earlier)
    add cell to closed set

    if cell == goal:
        reconstruct path by following came_from back to start
        reverse and return

    for each walkable neighbour:
        tentative_g = current_g + 1
        if tentative_g < known g for neighbour:
            record came_from[neighbour] = current
            push (f = tentative_g + h(neighbour, goal), tentative_g, neighbour)

return []   ← no path found
```

### `main.py`

Runs the autonomous demo. Imports from the parent `game/` directory using `sys.path.insert`.

**Key logic:**

```python
# Convert pygame pixel position → grid cell
start = pixel_to_cell(*player.get_position())   # (x, y) → (col, row)
goal  = pixel_to_cell(*point.get_position())

# Plan the full path upfront
path = find_path(start, goal, obstacle_cells)   # [(col, row), ...]

# Execute one step per frame
next_col, next_row = path[path_index]
dx = next_col * BOX_SIZE - player.x
dy = next_row * BOX_SIZE - player.y
player.move(dx, dy)
path_index += 1

# When point is collected, re-plan immediately
path = find_path(new_start, new_goal, obstacle_cells)
path_index = 0
```

The planned path is visualised as yellow dots drawn at the centre of each remaining cell.

---

