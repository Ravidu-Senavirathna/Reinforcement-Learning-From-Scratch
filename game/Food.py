import pygame
import random
import os

from Constants import *

class Food(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = random.randint(0, SCREEN_WIDTH - FOOD_SIZE[0])
        self.y = random.randint(0, SCREEN_HEIGHT - FOOD_SIZE[1])
        self.food_rect = pygame.Rect(self.x, self.y, *FOOD_SIZE) # Create a rect for the food to handle collisions

    def draw(self, screen):
        food_image = pygame.Surface(FOOD_SIZE) # Create a simple surface for the food
        food_image.fill(FOOD_COLOR)  # Green square as food
        screen.blit(food_image, (self.x, self.y))

    def move_to_random_position(self):
        self.x = random.randint(0, SCREEN_WIDTH - FOOD_SIZE[0])
        self.y = random.randint(0, SCREEN_HEIGHT - FOOD_SIZE[1])
        self.food_rect.topleft = (self.x, self.y)

    def get_rect(self):
        return self.food_rect
    
    def get_size(self):
        return FOOD_SIZE
    
    def get_position(self):
        return (self.x, self.y)
    

    