import utilities
import pygame


# Initialise pygame
pygame.init()

# Set up the game's screen size
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

image = pygame.image.load("images/sprites/Default_Player_Spritesheet.png").convert_alpha()

sprite = utilities.sprite(image)

print(image.get_width())

print (sprite.get_animatons())