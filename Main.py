
import utilities    # Local module
import pygame
from random import randint       


# Initialise pygame
pygame.init()

# Set up the game's screen size
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
#screen =pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Generate the FPS
clock = pygame.time.Clock()

# Prepare the camera
camera_group = utilities.camera()

# Grab the player spriteas
player_sprite_sheet_image = pygame.image.load("images/sprites/player/Player Animations V2.png").convert_alpha() #https://cupnooble.itch.io/sprout-lands-asset-pack

# Set up the first image of the player via a sprite sheet
player_animations_List = [
    "stationaryN,8", "stationaryE,8", "stationaryS,8", "stationaryW,8",
    "walkN,8", "walkE,8", "walkS,8", "walkW,8"
]

# Load in the players sprites
player = utilities.player(player_sprite_sheet_image, 14, 17, player_animations_List, camera_group, (640, 360))

# Set the players borders (50 px either side)
player.N_limit, player.W_limit, player.E_limit, player.S_limit = 200, 200, SCREEN_WIDTH - player.width - 200, SCREEN_HEIGHT - player.height - 200

# Set up the trees variables
tree_animations_list = ["immobileS,1","stationaryS,4","windyS,6","galeS,14"]
tree_sprite_sheet = pygame.image.load("images/sprites/trees/tree.png").convert_alpha() #https://cupnooble.itch.io/sprout-lands-asset-pack
num_of_trees = 20
tree_width, tree_height = 48, 33

apple_tree_sprite_sheet = pygame.image.load("images/sprites/trees/apple.png").convert_alpha()
num_of_apple_trees = 50

# Load in lots of trees within a tree dict, change the animations randomly
tree_dict = {}

i = 0
for _ in range(num_of_trees):
    random_x = randint(5,SCREEN_WIDTH - 10)                                         # Set rand X interval for the tree
    random_y = randint(5,SCREEN_HEIGHT - 20)                                        # Set rand Y interval for the tree
    # Generate the tree
    tree_dict[i] = utilities.sprite(tree_sprite_sheet, tree_width, tree_height, tree_animations_list, camera_group, (random_x, random_y))
    rand_animation = randint(0, len(tree_animations_list) -1 )                      # Generate a random type of animation for the tree
    tree_dict[i].action = tree_animations_list[rand_animation].split("S")[0]        # Preventing keying issues - remove S from key check as it is re-added later
    tree_dict[i].animation_cooldown = randint(100,300)                              # Update the animation for the trees to be rand intervals - make them look uniques
    i += 1

for _ in range(num_of_apple_trees):
    random_x = randint(5,SCREEN_WIDTH - 10)                                         # Set rand X interval for the tree
    random_y = randint(5,SCREEN_HEIGHT - 20)                                        # Set rand Y interval for the tree
    # Generate the tree
    tree_dict[i] = utilities.sprite(apple_tree_sprite_sheet, tree_width, tree_height, tree_animations_list, camera_group, (random_x, random_y))
    rand_animation = randint(0, len(tree_animations_list) -1 )                      # Generate a random type of animation for the tree
    tree_dict[i].action = tree_animations_list[rand_animation].split("S")[0]        # Preventing keying issues - remove S from key check as it is re-added later
    tree_dict[i].animation_cooldown = randint(100,300)                              # Update the animation for the trees to be rand intervals - make them look uniques
    i += 1
# Give the game a name
pygame.display.set_caption("Quinzee's Adventures")

# Begin the game
run = True
while run:

    current_time = pygame.time.get_ticks()      # Get the current time
    player.update_sprite(current_time)          # Run animation updates for the player
    for i in range(num_of_trees + num_of_apple_trees):                         # Run animation updates for the trees
        tree_dict[i].update_sprite(current_time)


    # Event handler
    for event in pygame.event.get():
        # If the user selects to quit, ensure this code is quit too
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        
        if event.type == pygame.MOUSEWHEEL:
            new_zoom = camera_group.zoom_scale + event.y * 0.03
            if new_zoom < 1.2 and new_zoom > 0.5:
                camera_group.zoom_scale += event.y * 0.03
            print(camera_group.zoom_scale)
            

    # Fill the screen
    screen.fill('#71ddee')

    # Update thea camera group
    camera_group.update()
    camera_group.custom_draw(player)
    

    # Finally update the display
    pygame.display.update()
    clock.tick(60)

  