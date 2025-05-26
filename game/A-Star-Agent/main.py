import sys
import os
import pygame

# Allow imports from the parent game/ folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

'''
Autonomous demo using A* pathfinding.

The agent:
    1. Converts pixel positions to grid (col, row) coordinates.
    2. Calls astar.find_path() to get the optimal sequence of cells.
    3. Walks the path one cell per tick — identical speed to the human player.
    4. When the point is collected, a new path is planned immediately.
'''

import Constants
import Util
from Player   import Player
from Point    import Point
from Obstacle import Obstacle
from Util import build_obstacles , cell_to_pixel , pixel_to_cell
from astar import find_path

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
