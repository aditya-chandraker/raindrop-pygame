
import pygame
import sys
import random

class RaindropGame:
    def __init__(self):
        pygame.init()

        # Set up display
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Raindrop")

        # Set up colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (120, 120, 255)

        # Set up the player block
        self.BLOCK_WIDTH, self.BLOCK_HEIGHT = 50, 50
        self.block_x, self.block_y = 20, self.height - self.BLOCK_HEIGHT - 20
        self.block_speed = 0
        self.ACCELERATION = 0.1

        # Set up the dropped blocks
        self.dropped_blocks = []

        # Set up a timer for dropping blocks
        self.drop_timer = pygame.time.get_ticks()

        # Main game loop
        self.clock = pygame.time.Clock()

    def handle_quit_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def check_win_and_collisions(self):
        # Check if the player reaches the right side and wins
        if self.block_x >= self.width - self.BLOCK_WIDTH:
            print("Congratulations! You reached the right side. You Win!")
            pygame.quit()
            sys.exit()

        # Check for collisions with dropped blocks
        player_rect = pygame.Rect(self.block_x, self.block_y, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        for dropped_block in self.dropped_blocks[:]:
            dropped_block.y += 10
            if player_rect.colliderect(dropped_block):
                print("You hit a dropped block! Game Over!")
                pygame.quit()
                sys.exit()

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.block_x > 0:
            self.block_speed -= self.ACCELERATION
        elif keys[pygame.K_RIGHT] and self.block_x < self.width - self.BLOCK_WIDTH:
            self.block_speed += self.ACCELERATION
        else:
            self.block_speed *= 0.9  # Apply friction to gradually slow down when not pressing left or right

        # Update the block position based on the speed
        self.block_x += self.block_speed

    def draw_objects(self):
        # Clear the screen
        self.screen.fill(self.BLACK)

        # Draw the player block
        pygame.draw.rect(self.screen, self.WHITE, (self.block_x, self.block_y, self.BLOCK_WIDTH, self.BLOCK_HEIGHT))

        # Draw the dropped blocks
        for dropped_block in self.dropped_blocks:
            pygame.draw.rect(self.screen, self.BLUE, dropped_block)

    def drop_new_block(self):
        # Drop a new block every 100 milliseconds
        current_time = pygame.time.get_ticks()
        if current_time - self.drop_timer > 100:
            new_block_x = random.randint(0, self.width)
            new_block_y = 0 - self.BLOCK_HEIGHT
            self.dropped_blocks.append(pygame.Rect(new_block_x, new_block_y, self.BLOCK_WIDTH / 2, self.BLOCK_HEIGHT / 2))
            self.drop_timer = current_time

    def run(self):
        while True:
            self.handle_quit_event()
            self.check_win_and_collisions()
            self.handle_input()
            self.drop_new_block()
            self.draw_objects()

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(60)

if __name__ == "__main__":
    game = RaindropGame()
    game.run()
