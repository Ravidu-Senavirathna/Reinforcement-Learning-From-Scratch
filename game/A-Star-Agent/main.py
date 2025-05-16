import sys
import os
import pygame

# Allow imports from the parent game/ folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



import Constants
import Util
from Player   import Player
from Point    import Point
from Obstacle import Obstacle
from Util import build_obstacles 

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

    running = True
    while running:

        # --- quit event ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- draw ---
        Util.draw_frame(screen, player, point, rendered_score, obstacles)
        
        pygame.display.flip()
        clock.tick(PLAY_SPEED)

    pygame.quit()


if __name__ == "__main__":
    main()
