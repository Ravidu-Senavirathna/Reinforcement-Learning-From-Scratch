import pygame
import random
import os

from Constants import *


# Initialize the player's starting position
STARTING_POSITION_X = (SCREEN_WIDTH // 2) - (PLAYER_SIZE[0] // 2)
STARTING_POSITION_Y = (SCREEN_HEIGHT // 2) - (PLAYER_SIZE[1] // 2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = STARTING_POSITION_X
        self.y = STARTING_POSITION_Y
        self.player_rect = pygame.Rect(self.x, self.y, *PLAYER_SIZE) # Create a rect for the player to handle collisions and boundaries

    def draw(self, screen):
        player_image = pygame.Surface(PLAYER_SIZE) # Create a simple surface for the player
        player_image.fill(PLAYER_COLOR)  # Red square as player
        screen.blit(player_image, (self.x, self.y))
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.player_rect.topleft = (self.x, self.y)  # Update the player's rect position

    def get_rect(self):
        pass
    
    def get_position(self):
        pass

    def set_position(self, x, y):
        pass