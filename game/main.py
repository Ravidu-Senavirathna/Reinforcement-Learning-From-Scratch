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



def build_obstacles():
    '''
    Generate NUM_OBSTACLES wall cells, making sure none of them land on the
    player's fixed starting cell (centre of the grid).
    Returns (obstacle_list, obstacle_cells_set).
    '''
    # Reserve the player's starting grid cell
    player_col = Constants.COLUMNS // 2
    player_row = Constants.ROWS    // 2
    occupied   = {(player_col, player_row)}

    obstacles = []
    for _ in range(Constants.NUM_OBSTACLES):
        obs = Obstacle(occupied)   # Obstacle adds its own cell to `occupied`
        obstacles.append(obs)

    return obstacles, occupied



# Main game loop
def main():

    ''' Initialize score and render the initial score text '''
    score = 0
    rendered_score = font.render(f"Score: {score}", True, text_color)



    ''' Initialize game objects '''
    player = Player()
    point = Point()



    ''' Main game loop '''
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            dx, dy = 0, 0

            ''' Handle player input: 
            Move the player based on WASD keys'''
            player_input = pygame.key.get_pressed()
            if player_input[pygame.K_w]:
                dy = -PLAYER_SPEED
            if player_input[pygame.K_s]:
                dy = PLAYER_SPEED
            if player_input[pygame.K_a]:
                dx = -PLAYER_SPEED
            if player_input[pygame.K_d]:
                dx = PLAYER_SPEED
        
        # Apply grid movement if an action was taken
        if dx != 0 or dy != 0:
            player.move(dx, dy)


        ''' Keep the player within the screen boundaries:
        Get the player's rect and clamp it to the screen rect, then update the player's position accordingly'''
        screen_rect = screen.get_rect()
        player.get_rect().topleft = player.get_position()  # Update the player's rect position
        player.get_rect().clamp_ip(screen_rect)
        player.set_position(*player.get_rect().topleft)


        Util.draw_frame(screen, player, point, rendered_score)


        '''Check for collision between player and point: 
        If they collide, increase the score and move the point to a new random position'''
        if player.get_rect().colliderect(point.get_rect()):
            score = score + 1
            rendered_score = font.render(f"Score: {score}", True, text_color)
            point.move_to_random_position()



        '''Update game state here'''
        pygame.display.flip()


        '''Limit the frame rate to 60 frames per second'''
        clock.tick(Constants.GAME_TICK_RATE)


if __name__ == "__main__":
    main()