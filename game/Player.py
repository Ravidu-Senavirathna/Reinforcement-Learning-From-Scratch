import pygame
import random
import os

import Constants

COLS = Constants.COLUMNS
ROWS = Constants.ROWS

# Import necessary modules and constants for the Player class
STARTING_POSITION_X = COLS // 2 * Constants.BOX_SIZE
STARTING_POSITION_Y = ROWS // 2 * Constants.BOX_SIZE

PLAYER_COLOR = Constants.PLAYER_COLOR
PLAYER_SIZE = Constants.PLAYER_SIZE




'''
The Player class inherits from pygame.sprite.Sprite, 
which allows it to be used in conjunction with Pygame's sprite groups and collision detection features.

Main methods of the Player class include:
    - __init__: Initializes the player with a starting position and creates a rectangle for collision detection 
    - draw: Draws the player on the screen as a rectangle filled with the specified color
    - move: Moves the player by a certain amount in the x and y directions and updates the player's rect position accordingly   

The class also includes methods: 
    - getting the player's rect for collision detection and boundary checking 
    - getting and setting the player's position.  

'''


class Player(pygame.sprite.Sprite):
    def __init__(self):

        ''' Initialize the player with a starting position and create a rect for collision detection '''

        pygame.sprite.Sprite.__init__(self)
        self.x = STARTING_POSITION_X
        self.y = STARTING_POSITION_Y
        self.player_rect = pygame.Rect(self.x, self.y, *PLAYER_SIZE)



    def draw(self, screen):

        ''' Draw the player on the screen. The player is represented as a simple rectangle for now, 
        but this can be replaced with an image or sprite later on '''

        player_image = pygame.Surface(PLAYER_SIZE)
        player_image.fill(PLAYER_COLOR)
        screen.blit(player_image, self.player_rect)
 


    def move(self, dx, dy):

        ''' Move the player by a certain amount in the x and y directions 
            and update the player's rect position accordingly '''

        self.x += dx
        self.y += dy
        self.player_rect = pygame.Rect(self.x, self.y, *PLAYER_SIZE)



    def get_rect(self):

        ''' Get the player's rect for collision detection and boundary checking '''

        return self.player_rect



    def get_position(self):

        ''' Get the player's current position as a tuple (x, y) '''

        return self.x, self.y



    def set_position(self, x, y):

        ''' Set the player's position to a specific (x, y) coordinate 
        and update the player's rect position accordingly '''

        self.x = x
        self.y = y
        self.player_rect = pygame.Rect(self.x, self.y, *PLAYER_SIZE)