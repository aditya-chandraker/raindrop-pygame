import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Accelerating Block Game")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Set up the player block
block_width, block_height = 50, 50
block_x, block_y = (width - block_width) // 2, height - block_height - 20
block_speed = 0
acceleration = 0.1  # You can adjust the acceleration factor

# Set up the dropped blocks
dropped_blocks = []

# Set up a timer for dropping blocks
drop_timer = pygame.time.get_ticks()

# Function to drop a new block
def drop_block():
    new_block_x = random.randint(0, width)
    new_block_y = 140 # 0 - block_height
    dropped_blocks.append(pygame.Rect(new_block_x, new_block_y, block_width/2, block_height/2))
    print ("Dropped a new block at", new_block_x, new_block_y)

# Main game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and block_x > 0:
        block_speed -= acceleration
    elif keys[pygame.K_RIGHT] and block_x < width - block_width:
        block_speed += acceleration
    else:
        # Apply friction to gradually slow down when not pressing left or right
        block_speed *= 0.9

    # Update the block position based on the speed
    block_x += block_speed

    # Check for collisions with dropped blocks
    player_rect = pygame.Rect(block_x, block_y, block_width, block_height)
    for dropped_block in dropped_blocks[:]:  # Use [:] to iterate over a copy of the list
        dropped_block.y += 10  # Adjust the speed of the dropping blocks
        if player_rect.colliderect(dropped_block):
            print("You hit a dropped block! Game Over!")
            pygame.quit()
            sys.exit()

    # Drop a new block every minute
    current_time = pygame.time.get_ticks()
    if current_time - drop_timer > 100:  # 60000 milliseconds = 1 minute
        drop_block()
        drop_timer = current_time

    # Clear the screen
    screen.fill(black)

    # Draw the player block
    pygame.draw.rect(screen, white, (block_x, block_y, block_width, block_height))

    # Draw the dropped blocks
    for dropped_block in dropped_blocks:
        pygame.draw.rect(screen, red, dropped_block)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)