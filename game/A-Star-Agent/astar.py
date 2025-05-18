import heapq
import sys
import os

# Make the parent game/ directory importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])



def find_path(start_cell, goal_cell, obstacle_cells):

    # open_set entries: (f_score, g_score, cell)
    # g_score is included as a tiebreaker so cells with the same f_score are
    # explored in insertion order (keeps the heap stable).
    open_set = []
    heapq.heappush(open_set, (0 + manhattan(start_cell, goal_cell), 0, start_cell))


    # closed set — cells already fully explored
    closed_set = set()

    while open_set:
        f, g, current = heapq.heappop(open_set)

        # Skip if we already processed this cell via a cheaper path
        if current in closed_set:
            continue
        closed_set.add(current)
