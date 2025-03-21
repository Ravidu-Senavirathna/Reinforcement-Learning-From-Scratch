import pygame
import random
import os

import Constants
import Util

PLAYER_SPEED = Constants.PLAYER_SPEED

from Point import Point
from Player import Player

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))

# Set the title of the window
pygame.display.set_caption("Game")

# Set up the clock for managing the frame rate
clock = pygame.time.Clock()

# Text rendering setup
font = pygame.font.Font(None, 36)
text_color = Constants.WHITE


# Main game loop
def main():

    ''' Initialize score and render the initial score text '''
    score = 0
    rendered_score = font.render(f"Score: {score}", True, text_color)



    ''' Initialize game objects '''
    player = Player()
    point = Point()



    ''' Main game loop '''
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        ''' Handle player input: 
        Move the player based on WASD keys'''
        player_input = pygame.key.get_pressed()
        if player_input[pygame.K_w]:
            player.move(0, -PLAYER_SPEED)
        if player_input[pygame.K_s]:
            player.move(0, PLAYER_SPEED)
        if player_input[pygame.K_a]:
            player.move(-PLAYER_SPEED, 0)
        if player_input[pygame.K_d]:
            player.move(PLAYER_SPEED, 0)



        ''' Keep the player within the screen boundaries:
        Get the player's rect and clamp it to the screen rect, then update the player's position accordingly'''
        screen_rect = screen.get_rect()
        player.get_rect().topleft = player.get_position()  # Update the player's rect position
        player.get_rect().clamp_ip(screen_rect)
        player.set_position(*player.get_rect().topleft)


        Util.draw_frame(screen, player, point, rendered_score)


        '''Check for collision between player and point: 
        If they collide, increase the score and move the point to a new random position'''
        if player.get_rect().colliderect(point.get_rect()):
            score = score + 1
            rendered_score = font.render(f"Score: {score}", True, text_color)
            point.move_to_random_position()



        '''Update game state here'''
        pygame.display.flip()


        '''Limit the frame rate to 60 frames per second'''
        clock.tick(Constants.GAME_TICK_RATE)


if __name__ == "__main__":
    main()