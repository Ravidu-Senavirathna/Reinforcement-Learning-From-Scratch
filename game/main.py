import pygame
import random
import os

from Constants import *

from Food import Food
from Player import Player

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the window
pygame.display.set_caption("Game")

# Set up the clock for managing the frame rate
clock = pygame.time.Clock()

# Text rendering setup
font = pygame.font.Font(None, 36)  # Use default font and size 36
text_color = WHITE  # White color for text


# Main game loop
def main():

    # Score 
    score = 0  # Initialize score
    rendered_score = font.render(f"Score: {score}", True, text_color)  # Render the score text

    # Game loop
    running = True

    player = Player()
    food = Food()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle player input
        player_input = pygame.key.get_pressed()
        if player_input[pygame.K_w]:
            player.move(0, -10)
        if player_input[pygame.K_s]:
            player.move(0, 10)
        if player_input[pygame.K_a]:
            player.move(-10, 0)
        if player_input[pygame.K_d]:
            player.move(10, 0)

        # Create a rect representing the screen
        screen_rect = screen.get_rect()

        # In your player update loop
        player_rect.topleft = player_pos
        player_rect.clamp_ip(screen_rect)
        player_pos[0], player_pos[1] = player_rect.topleft

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the player
        screen.blit(player_image, player_rect)
        # Draw the food
        screen.blit(food_image, food_rect)
        # Draw the score
        screen.blit(rendered_score, (10, 10))


        # Check for collision between player and food
        if player_rect.colliderect(food_rect):
            score = score + 1
            rendered_score = font.render(f"Score: {score}", True, text_color)

            # Move the food to a new random position (for simplicity, we just move it to a fixed position here)
            food_pos[0] = random.randint(0, SCREEN_WIDTH - food_size[0])
            food_pos[1] = random.randint(0, SCREEN_HEIGHT - food_size[1])
            food_rect.topleft = food_pos  # Update the food rect position

        # Update game state here
        pygame.display.flip()
        # Limit the frame rate to 60 frames per second
        clock.tick(60)


if __name__ == "__main__":
    main()