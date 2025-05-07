import pygame
import random
import os

import Constants


# Import necessary modules and constants for the Food class
SCREEN_WIDTH = Constants.SCREEN_WIDTH
SCREEN_HEIGHT = Constants.SCREEN_HEIGHT

POINT_SIZE = Constants.POINT_SIZE
POINT_COLOR = Constants.POINT_COLOR

# Calculate how many full grid columns and rows fit on the screen
cols = SCREEN_WIDTH // Constants.BOX_SIZE
rows = SCREEN_HEIGHT // Constants.BOX_SIZE


'''
The Point class inherits from pygame.sprite.Sprite.

Updated to accept an obstacle_cells set so that the collectible never spawns
on top of a wall.  The set is read-only here — Point does not modify it.

Main methods:
    - __init__                  : places the point at a random free grid cell
    - draw                      : draws the point on the screen
    - move_to_random_position   : relocates to a new random free cell
    - get_rect / get_size / get_position : geometry helpers
'''



class Point(pygame.sprite.Sprite):
    def __init__(self):

        '''Initializes the Point object by setting its position to a random location on the screen and creating a rectangle for collision detection.'''

        pygame.sprite.Sprite.__init__(self)
        # Pick a random grid step index and scale it back to pixel coordinates
        self.x = random.randint(0, cols - 1) * Constants.BOX_SIZE
        self.y = random.randint(0, rows - 1) * Constants.BOX_SIZE
        self.point_rect = pygame.Rect(self.x, self.y, *POINT_SIZE)



    def draw(self, screen):

        '''Draws the point on the screen as a rectangle filled with the specified color.'''

        point_image = pygame.Surface(POINT_SIZE)
        point_image.fill(POINT_COLOR)
        screen.blit(point_image, self.point_rect)



    def move_to_random_position(self):

        '''Moves the point to a new random position on the screen.'''
        '''Moves the point to a new random grid block position on the screen.'''
        
        # Pick a random grid step index and scale it back to pixel coordinates
        self.x = random.randint(0, cols - 1) * Constants.BOX_SIZE
        self.y = random.randint(0, rows - 1) * Constants.BOX_SIZE
        
        # Correctly bind the top-left of the rect to the grid coordinates
        self.point_rect = pygame.Rect(self.x, self.y, *POINT_SIZE)



    def get_rect(self):

        '''Returns the rectangle representing the point's position and size for collision detection.'''

        return self.point_rect



    def get_size(self):

        '''Returns the size of the point.'''

        return POINT_SIZE



    def get_position(self):

        '''Returns the current position of the point as a tuple (x, y).'''

        return (self.x, self.y)    