import pygame
import Constants
import Util
from Point import Point
from Player import Player
from Obstacle import Obstacle

PLAYER_SPEED = Constants.PLAYER_SPEED
BOX_SIZE = Constants.BOX_SIZE

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

# Text rendering setup
font = pygame.font.Font(None, 36)
text_color = Constants.WHITE




# Main game loop
def main():

    ''' Initialize score and render the initial score text '''
    score = 0
    rendered_score = font.render(f"Score: {score}", True, text_color)



    ''' Initialize game objects '''
    obstacles, obstacle_cells = Util.build_obstacles(Obstacle)
    player = Player()
    point  = Point(obstacle_cells)   # point will never spawn on a wall



    ''' Main game loop '''
    running = True
    while running:

        # --- event ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        # --- input (grid-snapped movement) ---
        dx, dy = 0, 0
        player_input = pygame.key.get_pressed()
        if player_input[pygame.K_w]:
            dy = -PLAYER_SPEED
        if player_input[pygame.K_s]:
            dy =  PLAYER_SPEED
        if player_input[pygame.K_a]:
            dx = -PLAYER_SPEED
        if player_input[pygame.K_d]:
            dx =  PLAYER_SPEED
        
        # --- move with obstacle collision ---
        if dx != 0 or dy != 0:
            new_x = player.x + dx
            new_y = player.y + dy

            # Convert proposed pixel position to grid cell
            new_col = new_x // BOX_SIZE
            new_row = new_y // BOX_SIZE

            # Only move if the target cell is not a wall
            if (new_col, new_row) not in obstacle_cells:
                player.move(dx, dy)


        # --- screen boundary clamp ---
        screen_rect = screen.get_rect()
        player.get_rect().topleft = player.get_position()
        player.get_rect().clamp_ip(screen_rect)
        player.set_position(*player.get_rect().topleft)

        # --- draw ---
        Util.draw_frame(screen, player, point, rendered_score, obstacles)

        # --- collision with point ---
        if player.get_rect().colliderect(point.get_rect()):
            score += 1
            rendered_score = font.render(f"Score: {score}", True, text_color)
            point.move_to_random_position()

        pygame.display.flip()
        clock.tick(Constants.GAME_TICK_RATE)

    pygame.quit()


if __name__ == "__main__":
    main()