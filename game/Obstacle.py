import pygame
import random
import Constants


'''
Obstacle class — represents a single impassable wall cell on the grid.

Each obstacle occupies exactly one BOX_SIZE * BOX_SIZE cell, consistent with
the Player and Point classes.  A set of occupied (col, row) tuples is passed in
at construction time so that obstacles are never placed on top of each other,
the player spawn, or the point.

Main methods:
    - __init__      : places the obstacle at a random free grid cell
    - draw          : renders the obstacle on the screen
    - get_rect      : returns the pygame.Rect for collision detection
    - get_cell      : returns the (col, row) grid coordinate
'''


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, occupied_cells: set):
        '''
        Place the obstacle at a random grid cell that is not already occupied.

        Parameters
        ----------
        occupied_cells : set of (col, row) tuples
            Cells that must not be used (player spawn, point, other obstacles).
            This set is mutated: the chosen cell is added to it so callers can
            pass the same set when constructing multiple obstacles.
        '''
        pygame.sprite.Sprite.__init__(self)

        # Pick a random free cell
        while True:
            col = random.randint(0, Constants.COLUMNS - 1)
            row = random.randint(0, Constants.ROWS - 1)
            if (col, row) not in occupied_cells:
                break

        occupied_cells.add((col, row))   # mark as taken for future obstacles

        self.col = col
        self.row = row
        self.x   = col * Constants.BOX_SIZE
        self.y   = row * Constants.BOX_SIZE
        self.rect = pygame.Rect(self.x, self.y,
                                Constants.BOX_SIZE, Constants.BOX_SIZE)


