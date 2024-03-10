import pygame
import sys
import random
from collections import deque

class RaindropGame:
    BLOCK_WIDTH, BLOCK_HEIGHT = 50, 50  # Class attributes
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (120, 120, 255)
    RED = (255, 0, 0)

    def __init__(self):
        pygame.init()

        # Set up display
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Raindrop")

        # Set up the dropped blocks using a deque with a maximum size of 30
        self.MAX_DROPPED_BLOCKS = 10
        self.DROP_INTERVAL = 100
        self.dropped_blocks = deque(maxlen=self.MAX_DROPPED_BLOCKS)

        # Set up a timer for dropping blocks
        self.drop_timer = pygame.time.get_ticks()

        # Main game loop
        self.clock = pygame.time.Clock()

    def handle_quit_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    class User:
        def __init__(self, game, name):
            self.game = game
            self.name = name

            # Set up the player block
            self.block_x, self.block_y = 20, self.game.height - RaindropGame.BLOCK_HEIGHT - 20
            self.block_speed = 0
            self.ACCELERATION = 0.1

        def check_win_and_collisions(self):
            # Check if the player reaches the right side and wins
            if self.block_x >= self.game.width - RaindropGame.BLOCK_WIDTH:
                print("Congratulations! You reached the right side. You Win!")
                pygame.quit()
                sys.exit()

            # Check for collisions with dropped blocks
            player_rect = pygame.Rect(self.block_x, self.block_y, RaindropGame.BLOCK_WIDTH, RaindropGame.BLOCK_HEIGHT)
            for dropped_block in self.game.dropped_blocks:
                if player_rect.colliderect(dropped_block):
                    print("You hit a dropped block! Game Over!")
                    pygame.quit()
                    sys.exit()

        def handle_input(self):
            self.check_win_and_collisions()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] and self.block_x > 0:
                self.block_speed -= self.ACCELERATION
            elif keys[pygame.K_RIGHT] and self.block_x < self.game.width - RaindropGame.BLOCK_WIDTH:
                self.block_speed += self.ACCELERATION
            else:
                self.block_speed *= 0.9  # Apply friction to gradually slow down when not pressing left or right

            # Update the block position based on the speed
            self.block_x += self.block_speed

            # Draw the player block
            pygame.draw.rect(self.game.screen, RaindropGame.RED, (self.block_x, self.block_y, RaindropGame.BLOCK_WIDTH, RaindropGame.BLOCK_HEIGHT))

    class Bot:
        def __init__(self, game, name):
            self.game = game
            self.name = name

            # Set up the player block
            self.block_x, self.block_y = 20, self.game.height - RaindropGame.BLOCK_HEIGHT - 20
            self.block_speed = 0
            self.ACCELERATION = 0.1
            self.alive = True

        def check_win_and_collisions(self):
            # Check if the player reaches the right side and wins
            if self.block_x >= self.game.width - RaindropGame.BLOCK_WIDTH:
                print(self.name + " reached the right side")

            # Check for collisions with dropped blocks
            player_rect = pygame.Rect(self.block_x, self.block_y, RaindropGame.BLOCK_WIDTH, RaindropGame.BLOCK_HEIGHT)
            for dropped_block in self.game.dropped_blocks:
                if player_rect.colliderect(dropped_block):
                    print(self.name + " hit a dropped block!")
                    self.alive = False

        def handle_computer_input(self, move_left=0):
            self.check_win_and_collisions()

            # Simulate computer player input
            if move_left == 1 and self.block_x > 0:
                self.block_speed -= self.ACCELERATION
            elif move_left == 2:
                self.block_speed += self.ACCELERATION
            else:
                self.block_speed *= 0.9
            
            # Update the block position based on the speed
            self.block_x += self.block_speed
            
            # Draw the player block
            pygame.draw.rect(self.game.screen, RaindropGame.WHITE, (self.block_x, self.block_y, RaindropGame.BLOCK_WIDTH, RaindropGame.BLOCK_HEIGHT))

        def random_move(self, percent_chance=0.5):
            if not self.alive:
                return  # Do nothing if the bot is not alive

            if random.random() < percent_chance:
                self.handle_computer_input(1)
            else:
                self.handle_computer_input(2)

        def get_distance_to_blocks(self):
            player_center_x = self.block_x + RaindropGame.BLOCK_WIDTH / 2
            player_center_y = self.block_y + RaindropGame.BLOCK_HEIGHT / 2

            distances = []
            for dropped_block in self.game.dropped_blocks:
                block_center_x = dropped_block.x + dropped_block.width / 2
                block_center_y = dropped_block.y + dropped_block.height / 2

                # Calculate the distance between player and dropped block using Pythagorean theorem
                distance_x = block_center_x - player_center_x
                distance_y = block_center_y - player_center_y

                distances.append({"x": distance_x, "y": distance_y})

            return distances

    def draw_objects(self):
        # Clear the screen
        self.screen.fill(RaindropGame.BLACK)

        # Draw the dropped blocks
        for dropped_block in self.dropped_blocks:
            pygame.draw.rect(self.screen, RaindropGame.BLUE, dropped_block)

    def drop_new_block(self):
        for dropped_block in self.dropped_blocks:
            dropped_block.y += 10

        # Drop a new block every 100 milliseconds
        current_time = pygame.time.get_ticks()
        if current_time - self.drop_timer > self.DROP_INTERVAL:
            new_block_x = random.randint(0, self.width)
            new_block_y = 0 - RaindropGame.BLOCK_HEIGHT
            self.dropped_blocks.append(pygame.Rect(new_block_x, new_block_y, RaindropGame.BLOCK_WIDTH / 2, RaindropGame.BLOCK_HEIGHT / 2))
            self.drop_timer = current_time

    def run(self):
        bot_1 = self.Bot(self, "Bot 1")
        bot_2 = self.Bot(self, "Bot 2")
        user_1 = self.User(self, "User 1")

        while True:
            self.handle_quit_event()
            self.drop_new_block()
            self.draw_objects()            

            # User Controlled
            user_1.handle_input()

            # Computer Controlled (0 = only right, 1 = only left
            # between (0-1) = random chance of left or right based on percent_chance)
            bot_1.random_move(0.0)
            bot_2.random_move(0.5)

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(60)

if __name__ == "__main__":
    game = RaindropGame()
    game.run()
