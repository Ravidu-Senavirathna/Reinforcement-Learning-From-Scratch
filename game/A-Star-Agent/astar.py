import heapq
import sys
import os
import Constants

# Make the parent game/ directory importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



'''
A* Pathfinding — grid-based implementation.

find_path(start_cell, goal_cell, obstacle_cells) -> list[tuple[int,int]]

    Returns an ordered list of (col, row) cells from start (exclusive) to
    goal (inclusive), or an empty list if no path exists.

    start_cell    : (col, row) — where the player is now
    goal_cell     : (col, row) — where the point is
    obstacle_cells: set of (col, row) — impassable wall cells
'''


# --- heuristic ---
def manhattan(a, b):
    '''
    Manhattan distance — the number of horizontal + vertical steps between two
    grid cells.  

    h(n) = |col_a - col_b| + |row_a - row_b|
    '''
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# --- neighbour generator ---
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]   # UP DOWN LEFT RIGHT

def neighbours(cell, obstacle_cells):
    '''
    Yield walkable grid neighbours of `cell`.

    A neighbour is valid when:
        1. It is inside the screen boundary  (0 ≤ col < COLUMNS, 0 ≤ row < ROWS)
        2. It is not in obstacle_cells
    '''
    col, row = cell
    for dir_col, dir_row in DIRECTIONS:
        neigh_col, neigh_row = col + dir_col, row + dir_row
        if 0 <= neigh_col < Constants.COLUMNS and 0 <= neigh_row < Constants.ROWS:
            if (neigh_col, neigh_row) not in obstacle_cells:
                yield (neigh_col, neigh_row)


def find_path(start_cell, goal_cell, obstacle_cells):

    # open_set entries: (f_score, g_score, cell)
    # g_score is included as a tiebreaker so cells with the same f_score are
    # explored in insertion order (keeps the heap stable).
    open_set = []
    heapq.heappush(open_set, (0 + manhattan(start_cell, goal_cell), 0, start_cell))

    # came_from[cell] = the cell we arrived from
    came_from = {}

    # g_score[cell] = cheapest known cost from start to cell
    g_score = {start_cell: 0}

    # closed set — cells already fully explored
    closed_set = set()

    while open_set:
        f, g, current = heapq.heappop(open_set)

        # Skip if we already processed this cell via a cheaper path
        if current in closed_set:
            continue
        closed_set.add(current)

        # ── goal reached — reconstruct path ──────────────────────────────────
        if current == goal_cell:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()          # start → goal order
            return path             # start cell itself is excluded

        # ── expand neighbours ─────────────────────────────────────────────────
        for neighbour in neighbours(current, obstacle_cells):
            if neighbour in closed_set:
                continue

            tentative_g = g + 1     # every step costs 1

            if tentative_g < g_score.get(neighbour, float('inf')):
                # Found a cheaper route to this neighbour
                came_from[neighbour] = current
                g_score[neighbour]   = tentative_g
                f_score              = tentative_g + manhattan(neighbour, goal_cell)
                heapq.heappush(open_set, (f_score, tentative_g, neighbour))

    # open set exhausted — no path exists
    return []