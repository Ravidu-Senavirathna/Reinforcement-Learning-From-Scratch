import pygame
import Constants



'''Draws a grid on the given surface using the specified box size from Constants.'''

def draw_grid(surface, 
              box_size=Constants.BOX_SIZE, 
              color=Constants.GRAY, 
              width= Constants.SCREEN_WIDTH, 
              height=Constants.SCREEN_HEIGHT
              ):
    
    for x in range(0, width, box_size):
        pygame.draw.line(surface, color, (x, 0), (x, height))
    for y in range(0, height, box_size):
        pygame.draw.line(surface, color, (0, y), (width, y))



'''Simple font-render helper.'''

def render_text(text, font, color):
    
    return font.render(text, True, color)



'''draw_frame — renders one complete frame.'''

def draw_frame(screen, player, point, score_text, obstacles=None):
    '''Draw the current game state: background, grid, obstacles, player, point, HUD.'''

    screen.fill(Constants.BLACK)
    draw_grid(screen)

    # Draw obstacles first (behind player and point)
    if obstacles:
        for obs in obstacles:
            obs.draw(screen)

    player.draw(screen)
    point.draw(screen)
    screen.blit(score_text, (10, 10))


'''Generate NUM_OBSTACLES wall cells, making sure none of them land on the player's fixed starting cell.'''
def build_obstacles(Obstacle):

    # Reserve the player's starting grid cell
    player_col = Constants.COLUMNS // 2
    player_row = Constants.ROWS    // 2
    occupied   = {(player_col, player_row)}

    obstacles = []
    for _ in range(Constants.NUM_OBSTACLES):
        obs = Obstacle(occupied)   # Obstacle adds its own cell to `occupied`
        obstacles.append(obs)

    return obstacles, occupied



'''Convert top-left pixel coordinates to (col, row).'''
def pixel_to_cell(x, y):
    x  = x // Constants.BOX_SIZE
    y =  y // Constants.BOX_SIZE
    return x, y

    
'''Convert (col, row) to top-left pixel coordinates.'''
def cell_to_pixel(col, row):
    col = col * Constants.BOX_SIZE
    row = row * Constants.BOX_SIZE
    return col, row