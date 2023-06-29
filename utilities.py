"""
Utilities.py
Generated:  11 Oct 22
By:         Bish AFC

Description:
Hosts all of the classes used by MyGame
"""

# Import all of the required modules
from asyncio.windows_events import NULL
from doctest import BLANKLINE_MARKER
import pygame #https://www.pygame.org/docs/


# All classes
class sprite (pygame.sprite.Sprite):
    """
    A class for all sprites
    """
    def __init__(self, sheet, width, height, animations_list, group, pos):
        
        """
        sheet=the sprite sheet, width=width of each sprite, height=height of each sprite,
        animations=list of available animations
        """

        super().__init__(group)                     # Enables sprite to added immediately into a group
        
        self.sheet = sheet                          # Load in the sheet for this sprite
        self.frame = 0                              # Current frame loaded
        self.direction = pygame.math.Vector2()      # Set up the camera following direction
        self.facing = "S"                           # Set default facing location
        self.action = "stationary"                  # Set default animation action
        self.width = width                          # Width of each sprite
        self.height = height                        # Height of each sprite
        self.scale = 3                             # Scale of the sprites
        self.colour = (0, 0, 0)                     # Set black to make transparent
        self.direction.x = 0                        # X movement speed
        self.direction.y = 0                        # Y movement speed
        self.animation_cooldown = 100               # The cooldown time for this instance
        self.speed = 2                              # number of pixels moved per frame
        self.N_limit = 50                           # Set the northern boundary for the sprite
        self.E_limit = 500                          # Set the eastern boundary for the sprite
        self.S_limit = 500                          # Set the southern boundary for the sprite
        self.W_limit = 50                           # Set the western boundary for the sprite
        self.animations= {}                         # Set up a dictionary to hold all animations
        self.animations_list = animations_list      # Add the list of the different types of animations
        self.pos = pos                              # Set the X Y positions
        self.last_update = pygame.time.get_ticks()  # Set up a timer so animations can happen
        self.frame = 0
        
        self.load_animations()                      # load in all of the sprites
        self.image = self.get_animations()[0]       # Set the inital view of the sprite to be stationary south facing

    def load_animations(self):
        """"
        Seperate function so scale can be altered mid-game
        """

        sheetY = 0  # Prep the Y value of the sheet
        # Set up the dictionary of animations
        for animation in self.animations_list:        # e.g. would be run/walk/stationary
            
            animation_name = animation.split(",")[0]
            animation_number = int(animation.split(",")[1])
            sheetX = 0 # Reset the X value of the sheet                

            # Clean out the list 
            self.animations[animation_name] = []
            
            # Get the # of sprites per line by using the number provided in the csv string
            for _ in range(animation_number):
                
                # Add each sprite to the dictionary
                self.animations[animation_name].append(self._get_sprite_image(sheetX, sheetY))

                # Move the x value over to the next sprite
                sheetX += self.width
        
            # Move the y value down to the next animation
            sheetY += self.height

        # Update the rectangle, using the last entry as a size
        self.rect = self.animations[animation_name][0].get_rect(center = self.pos)
        
    def _get_sprite_image (self, spriteX, spriteY):

        # Set up a surface just for the image - to the size of the sprite not the sheet
        self.image = pygame.Surface((self.width,self.height)).convert_alpha()

        # Show it onto the surface
        # First 0,0 is the XY of the sheet itself
        # Second 0,0 is the XY of the first sprite, along with the width and height
        self.image.blit(self.sheet, (0,0), (spriteX, spriteY, self.width, self.height))

        # Alter the image so it scales as requested
        self.image = pygame.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))

        # Ensure that the returned image has a transparent backround
        self.image.set_colorkey(self.colour)

        # Return the entire surface
        return self.image

    def get_animations(self):
        """Returns the list of the currently in use animations"""
        return self.animations[self.action + self.facing]

    def draw(self,screen):
        """Gives the ability to draw within groups"""
        screen.blit(self.image, self.rect)

    def update_sprite(self, current_time):
        """Update the sprite if it is due to be updated"""
        
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1                      # Increment the frames
        
            # if the # of frames is > number of images, loop back to the beginning
            if len(self.get_animations()) <= self.frame:
                self.frame = 0
            self.last_update = current_time      # Reset the timer cooldown

        # Update the sprite
        self.image = self.get_animations()[self.frame]
    
class player(sprite):
    """Sub-class of sprite to include functional input"""
    def __init__(self, sheet, width, height, animations_list, group, pos):
        super().__init__(sheet, width, height, animations_list, group, pos)
    
    def input(self, event = NULL):
        """Focussed keypresses for the player"""

        # See if the user has pressed down the key
        pressed = pygame.key.get_pressed()

        self.action = "walk"                            # Start action as walking
        self.animation_cooldown = 50                    # Set animation cooldown to 50
        self.direction.y, self.direction.x = 0, 0       # Start velocity on both vectors to 0

        # If the user has held down any of the direction keys, make the character walk            
        if pressed[pygame.K_w] or pressed[pygame.K_UP]:         # If going North
            self.facing, self.direction.y = "N", -1
        elif pressed[pygame.K_s] or pressed[pygame.K_DOWN]:     # If going South
            self.facing, self.direction.y = "S", 1
            
        if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:      # If going East
            self.facing, self.direction.x = "E", 1
        elif pressed[pygame.K_a] or pressed[pygame.K_LEFT]:     # If going West
            self.facing, self.direction.x = "W", -1

    def update(self):
        """Called upon externally when updating the screen"""
        self.input()                                    # Update the input
        self.rect.center += self.direction * self.speed # Set the vector factor

        if self.direction.x + self.direction.y == 0:    # Change the sprite to stationary if not moving
            self.action = "stationary"
            self.animation_cooldown = 120
        
        self.rect.center += self.direction * self.speed # Update the sprite's velocity
      
class camera(pygame.sprite.Group):
    """
    Class to host camera operation for a pygame. Class taken inspiration from
    https://github.com/clear-code-projects/Pygame-Cameras/blob/main/camera.py
    YT - https://www.youtube.com/watch?v=u7LPRqrzry8&t=222s&ab_channel=ClearCode
    """
    # Init requires connection to super class containing python group settings
    def __init__(self):
        super().__init__()                                         # Initiate the super class (pygame.sprite.Group)
        self.display_surface = pygame.display.get_surface()        # Generate a surface just for the cameras viewing
        self.offset = pygame.math.Vector2()                        # Set the offset of the camera
        self.half_w = self.display_surface.get_size()[0] // 2      # Get the halfway X point of the screen
        self.half_h = self.display_surface.get_size()[1] // 2      # Get the halfway Y point of the screen

        # This is the play area a player can move around in
        self.camera_borders = {'left' : 200, 'right': 200, 'top' : 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect (l, t, w, h)

        # camera speed
        self.keyboard_speed = 5
        self.mouse_speed = 0.2

        # Load in the ground's image (just waves)
        self.ground_surface     = pygame.image.load("images/backgrounds/MyGameWorld.png").convert_alpha()
        self.ground_rect        = self.ground_surface.get_rect(topleft = (0, 0))    # Put a rectangle aroun the ground
    
        self.zoom_scale = 1 # Set the zoom scale
        self.internal_surface_size = (2500, 2500)
        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surface.get_rect(center = (self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset = pygame.math.Vector2() # Recalculate offset again for zoom
        self.internal_offset.x = self.internal_surface_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surface_size[1] // 2 - self.half_h
        

    def center_target_camera(self, target):
        # Run the center target onto the player - makes it appear to follow them and everything else static
        self.offset.x = target.rect.centerx - self.half_w  # Put the center of the camera on the player - X
        self.offset.y = target.rect.centery - self.half_h  # Put the center of the camera on the player - Y 

    def box_target_camera(self,target):
        # Generate the play zone that the player can menouver in
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom
    
        # Update the play zone's borders to reflect the overall map movement
        self.offset.x = self.camera_rect.left - self.camera_borders['left']    
        self.offset.y = self.camera_rect.top - self.camera_borders['top']  
    
    def keyboard_control(self):
    	# See if a key is pressed
        keys = pygame.key.get_pressed()
	    
        # Modify camera position based on the key
        if keys[pygame.K_a]: self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_d]: self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_w]: self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_s]: self.camera_rect.y += self.keyboard_speed
        
        # Modify the offsets
        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def mouse_control(self):
        """"Move the camera if the mouse heads on ouside of the zone border for the player"""

        mouse = pygame.math.Vector2(pygame.mouse.get_pos())     # Set the vector of the current mouse position
        mouse_offset_vector = pygame.math.Vector2()             

        # Set the borders for the mouse
        left_border = self.camera_borders['left'] 
        top_border = self.camera_borders['top']
        right_border = self.display_surface.get_size()[0] - self.camera_borders['right']
        bottom_border = self.display_surface.get_size()[1] - self.camera_borders['bottom']

        # Lots of mouse logic..
        if top_border < mouse.y < bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector.x = mouse.x - left_border
                pygame.mouse.set_pos((left_border,mouse.y))
            
            if mouse.x > right_border:
                mouse_offset_vector.x = mouse.x - right_border
                pygame.mouse.set_pos((right_border,mouse.y))
 
        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border,top_border)
                pygame.mouse.set_pos((left_border,top_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border,top_border)
                pygame.mouse.set_pos((right_border,top_border))
 
        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border,bottom_border)
                pygame.mouse.set_pos((left_border,bottom_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border,bottom_border)
                pygame.mouse.set_pos((right_border,bottom_border))

        if left_border < mouse.x < right_border:
            if mouse.y < top_border:
                mouse_offset_vector.y = mouse.y - top_border
                pygame.mouse.set_pos((mouse.x,top_border))
            if mouse.y > bottom_border:
                mouse_offset_vector.y = mouse.y - bottom_border
                pygame.mouse.set_pos((mouse.x,bottom_border))

        # Finally modify the offset
        self.offset += mouse_offset_vector * self.mouse_speed
    
    def zoom_keybord_control(self):
        """Zoom if the keyboard requests it"""
        keys = pygame.key.get_pressed()

        # If the PLUS key is selected
        if keys[pygame.K_PLUS]:
            self.zoom_scale += 0.1

        # if the MINUS key is slected
        elif keys[pygame.K_MINUS]:
            self.zoon_scale -= 0.1

    def custom_draw(self, player):
        """Customised draw method to manipulate the camera, ensures that the player can appear to be behind objects"""
        
        self.center_target_camera(player)
        self.box_target_camera(player)
		#self.keyboard_control()
        #self.mouse_control()

        self.internal_surface.fill('#71ddee')

        # Load the ground surface
        ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
        self.internal_surface.blit(self.ground_surface, ground_offset)

        # Retrieve all sprites within the group of the camera (ensures draw order so things higher up appear behind those lower down)
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.bottom) :
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset         # Generate the offset for each sprite
            self.internal_surface.blit(sprite.image, offset_pos)    # Reproduce sprite on the screen

        scaled_surface = pygame.transform.scale(self.internal_surface, self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surface.get_rect(center = (self.half_w, self.half_h))


        self.display_surface.blit(scaled_surface,scaled_rect)