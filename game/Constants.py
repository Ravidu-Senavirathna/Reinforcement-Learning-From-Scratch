import os
import random


# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GAME_TICK_RATE = 600  # Frames per second
BOX_SIZE = 20  # Size of the grid boxes for movement and collision detection

# Player properties
PLAYER_SIZE = (BOX_SIZE, BOX_SIZE)  # Size of the player
PLAYER_COLOR = RED  # Red color for the player
PLAYER_SPEED = 1  # Speed of the player

# Food properties
POINT_SIZE = (BOX_SIZE, BOX_SIZE)  # Size of the food
POINT_COLOR = GREEN  # Green color for the food