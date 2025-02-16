import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))

# Set the title of the window
pygame.display.set_caption("Game")

# Set up the clock for managing the frame rate
clock = pygame.time.Clock()


# Player Properties
player_pos = [400, 300]
player_image = pygame.Surface((20, 20))
player_image.fill((255, 0, 0))  # Red square as player


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

        
        # Clear the screen        
        screen.fill((0, 0, 0))  # Fill the screen with black

        # Draw the player
        screen.blit(player_image, player_pos)

        # Update game state here
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 frames per second


if __name__ == "__main__":
    main()