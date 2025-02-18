import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))

# Set the title of the window
pygame.display.set_caption("Game")

# Set up the clock for managing the frame rate
clock = pygame.time.Clock()

# Text rendering setup
font = pygame.font.Font(None, 36)  # Use default font and size 36
text_color = (255, 255, 255)  # White color for text


# Player Properties
player_pos = [400, 300] # Starting position of the player
player_size = (20, 20) # Size of the player
player_image = pygame.Surface(player_size) # Create a simple surface for the player
player_image.fill((255, 0, 0))  # Red square as player
player_rect = pygame.Rect(player_pos[0], player_pos[1], *player_size) # Create a rect for the player to handle collisions and boundaries


# Food Properties
food_pos = [200, 150] # Starting position of the food
food_size = (10, 10) # Size of the food
food_image = pygame.Surface(food_size) # Create a simple surface for the food
food_image.fill((0, 255, 0))  # Green square as food
food_rect = pygame.Rect(food_pos[0], food_pos[1], *food_size) # Create a rect for the food to handle collisions



# Main game loop
def main():


    # Game loop
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # Handle player input
        player_input = pygame.key.get_pressed()
        if player_input[pygame.K_w]:
            player_pos[1] -= 10
        if player_input[pygame.K_s]:
            player_pos[1] += 10
        if player_input[pygame.K_a]:
            player_pos[0] -= 10
        if player_input[pygame.K_d]:
            player_pos[0] += 10


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

        # Update game state here
        pygame.display.flip()
        # Limit the frame rate to 60 frames per second
        clock.tick(60)


if __name__ == "__main__":
    main()