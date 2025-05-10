import pygame
import Constants



'''Draws a grid on the given surface using the specified box size from Constants.
This function is used to visually divide the game screen into a grid, which can help with movement and collision detection.'''

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



'''
draw_frame — renders one complete frame.

Updated signature accepts an optional list of obstacles so that the human game
and the A* demo can both use the same helper.
'''

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