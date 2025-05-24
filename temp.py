import sys
import os
import pygame

# Allow imports from the parent game/ folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


'''
AStarAgent/main.py — autonomous demo using A* pathfinding.

The agent:
    1. Converts pixel positions to grid (col, row) coordinates.
    2. Calls astar.find_path() to get the optimal sequence of cells.
    3. Walks the path one cell per tick — identical speed to the human player.
    4. When the point is collected, a new path is planned immediately.

Run from the game/ directory:
    python AStarAgent/main.py
'''


import Constants
import Util
from Player   import Player
from Point    import Point
from Obstacle import Obstacle
from Util import build_obstacles , cell_to_pixel , pixel_to_cell
from astar    import find_path

PLAY_SPEED = 60
BOX_SIZE     = Constants.BOX_SIZE
PLAYER_SPEED = Constants.PLAYER_SPEED   # == BOX_SIZE, one cell per step




def main():
    pygame.init()
    screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    pygame.display.set_caption("A* Agent")
    clock = pygame.time.Clock()
    font  = pygame.font.Font(None, 36)

    # --- world setup ---
    obstacles, obstacle_cells = build_obstacles(Obstacle)
    player = Player()
    point  = Point(obstacle_cells)

    score          = 0
    rendered_score = font.render(f"Score: {score}", True, Constants.WHITE)

    # --- initial path ---
    start = pixel_to_cell(*player.get_position())
    goal  = pixel_to_cell(*point.get_position())
    path  = find_path(start, goal, obstacle_cells)   # list of (col, row) cells

    # path_index tracks which step in the current path we are executing next
    path_index = 0

    running = True
    while running:

        # --- quit event ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- agent movement ---
        if path_index < len(path):
            # Next cell the agent wants to move into
            next_col, next_row = path[path_index]
            target_x, target_y = cell_to_pixel(next_col, next_row)

            cur_x, cur_y = player.get_position()
            dx = target_x - cur_x   # will be exactly ±BOX_SIZE or 0
            dy = target_y - cur_y

            player.move(dx, dy)
            path_index += 1

        # --- collect point ---
        if player.get_rect().colliderect(point.get_rect()):
            score += 1
            rendered_score = font.render(f"Score: {score}", True, Constants.WHITE)
            point.move_to_random_position()

            # Plan a fresh path to the new point position
            start      = pixel_to_cell(*player.get_position())
            goal       = pixel_to_cell(*point.get_position())
            path       = find_path(start, goal, obstacle_cells)
            path_index = 0

        # --- re-plan if path ran out without collecting (shouldn't happen, but safe) ---
        elif path_index >= len(path):
            start      = pixel_to_cell(*player.get_position())
            goal       = pixel_to_cell(*point.get_position())
            path       = find_path(start, goal, obstacle_cells)
            path_index = 0

        # --- draw ---
        Util.draw_frame(screen, player, point, rendered_score, obstacles)

        # Draw the planned path as small yellow dots so you can see A* working
        for col, row in path[path_index:]:
            px = col * BOX_SIZE + BOX_SIZE // 2
            py = row * BOX_SIZE + BOX_SIZE // 2
            pygame.draw.circle(screen, Constants.BLUE, (px, py), 3)

        pygame.display.flip()
        clock.tick(PLAY_SPEED)

    pygame.quit()


if __name__ == "__main__":
    main()



















import heapq
import sys
import os

# Make the parent game/ directory importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import Constants


'''
A* Pathfinding — grid-based implementation matched to your game constants.

The grid is Constants.COLUMNS wide and Constants.ROWS tall.
Each cell is identified by a (col, row) integer tuple.
Diagonal movement is disabled to match the four-direction WASD controls.

Public API
----------
    find_path(start_cell, goal_cell, obstacle_cells) -> list[tuple[int,int]]

        Returns an ordered list of (col, row) cells from start (exclusive) to
        goal (inclusive), or an empty list if no path exists.

        start_cell    : (col, row) — where the player is now
        goal_cell     : (col, row) — where the point is
        obstacle_cells: set of (col, row) — impassable wall cells
'''


# ── heuristic functions ────────────────────────────────────────────────────────────────

def manhattan(a, b):
    '''
    Manhattan distance — the number of horizontal + vertical steps between two
    grid cells.  This is admissible (never over-estimates) for a grid where
    each move costs 1 and diagonal movement is not allowed.

    h(n) = |col_a - col_b| + |row_a - row_b|
    '''
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ── neighbour generator ───────────────────────────────────────────────────────

DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]   # UP DOWN LEFT RIGHT


def neighbours(cell, obstacle_cells):
    '''
    Yield walkable grid neighbours of `cell`.

    A neighbour is valid when:
        1. It is inside the screen boundary  (0 ≤ col < COLUMNS, 0 ≤ row < ROWS)
        2. It is not in obstacle_cells
    '''
    col, row = cell
    for dc, dr in DIRECTIONS:
        nc, nr = col + dc, row + dr
        if 0 <= nc < Constants.COLUMNS and 0 <= nr < Constants.ROWS:
            if (nc, nr) not in obstacle_cells:
                yield (nc, nr)


# ── A* ────────────────────────────────────────────────────────────────────────

def find_path(start_cell, goal_cell, obstacle_cells):
    '''
    A* search from start_cell to goal_cell on the game grid.

    How A* works
    ------------
    A* maintains an *open set* — cells discovered but not yet fully explored —
    ordered by f(n) = g(n) + h(n):

        g(n)  actual cost from start to cell n  (steps taken so far)
        h(n)  estimated cost from n to goal     (Manhattan distance)
        f(n)  total estimated cost through n

    At each step we pop the cell with the lowest f value and expand its
    neighbours.  Because the heuristic never over-estimates, the first time we
    reach the goal we are guaranteed to have found the shortest path.

    Parameters
    ----------
    start_cell     : (col, row)
    goal_cell      : (col, row)
    obstacle_cells : set of (col, row)

    Returns
    -------
    list of (col, row) — path from start (exclusive) to goal (inclusive).
    Empty list if no path exists.
    '''

    # Edge case: already there
    if start_cell == goal_cell:
        return []

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
