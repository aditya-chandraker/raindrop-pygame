import pygame
import sys
import random
from collections import deque
import numpy as np

class RaindropGame:
    BLOCK_WIDTH, BLOCK_HEIGHT = 50, 50

    WHITE = (255, 255, 255)
    WHITE_ALPHA_100 = (255, 255, 255, 100)
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
        self.MAX_DROPPED_BLOCKS = 15
        self.DROP_INTERVAL = 100
        self.dropped_blocks = deque(maxlen=self.MAX_DROPPED_BLOCKS)

        # Set up a timer for dropping blocks
        self.drop_timer = pygame.time.get_ticks()

        # Main game loop
        self.clock = pygame.time.Clock()

    def draw_rect_alpha(surface, color, rect, name):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)

        font = pygame.font.SysFont('arial', 18)
        text = font.render(name, 1, (0, 0, 0))
        textpos = (rect[0] + 10, rect[1] + 10)
        surface.blit(text, textpos)


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
            # pygame.draw.rect(self.game.screen, RaindropGame.RED, (self.block_x, self.block_y, RaindropGame.BLOCK_WIDTH, RaindropGame.BLOCK_HEIGHT))

            RaindropGame.draw_rect_alpha(self.game.screen, RaindropGame.RED, (self.block_x, self.block_y, RaindropGame.BLOCK_WIDTH, RaindropGame.BLOCK_HEIGHT), self.name)


    class Bot:
        def __init__(self, game, name):
            self.game = game
            self.name = name

            # Set up the player block
            self.block_x, self.block_y = 20, self.game.height - RaindropGame.BLOCK_HEIGHT - 20
            self.block_speed = 0
            self.ACCELERATION = 0.1
            self.alive = True
            self.win = False

        def check_win_and_collisions(self):
            # Check if the player reaches the right side and wins
            if self.block_x >= self.game.width - RaindropGame.BLOCK_WIDTH:
                print(self.name + " reached the right side")
                self.alive = False
                self.win = True


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
            # pygame.draw.rect(self.game.screen, RaindropGame.WHITE_ALPHA_100, (self.block_x, self.block_y, RaindropGame.BLOCK_WIDTH, RaindropGame.BLOCK_HEIGHT))
            RaindropGame.draw_rect_alpha(self.game.screen, RaindropGame.WHITE_ALPHA_100, (self.block_x, self.block_y, RaindropGame.BLOCK_WIDTH, RaindropGame.BLOCK_HEIGHT), self.name)


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

                distances.append(distance_x)
                distances.append(distance_y)

            return distances
    
    class NeuralNetworkBot(Bot):
        def __init__(self, game, name, hidden_size):
            super().__init__(game, name)
            self.input_size = game.MAX_DROPPED_BLOCKS * 2 + 1
            self.hidden_size = hidden_size
            self.output_size = 1

            self.fitness = 0

            # Initialize weights and biases randomly
            self.W1 = np.random.randn(self.input_size, self.hidden_size)
            self.b1 = np.zeros((1, self.hidden_size))

            self.W2 = np.random.randn(self.hidden_size, self.output_size)
            self.b2 = np.zeros((1, self.output_size))

        def sigmoid(self, x):
            return 1 / (1 + np.exp(-x))

        def forward(self, input_data):
            # Input layer
            layer1 = np.dot(input_data, self.W1) + self.b1

            # Hidden layer
            layer2 = self.sigmoid(layer1)

            # Output layer
            output = np.dot(layer2, self.W2) + self.b2

            return output
        
        def check_win_and_collisions(self):
            super().check_win_and_collisions()
            if self.win:
                self.fitness += pygame.time.get_ticks()
                self.fitness += 5000
            
            if not self.alive:
                self.fitness += pygame.time.get_ticks()
                self.fitness += np.floor(self.block_x*10)


        def determine_move(self):            
            if not self.alive:
                return  # Do nothing if the bot is not alive
            
            # Get the distances to the dropped blocks
            distances = super().get_distance_to_blocks()

            # if there are less than 10 blocks, pad the list with zeros
            if len(distances) < self.input_size - 1:
                distances += [0] * (self.input_size - 1 - len(distances))

            # Preprocess input data
            input_data = np.array([distances + [self.block_x]])
            # print("input " +  str(input_data))
            # print("\n")

            # Forward pass through the neural network
            output = self.forward(input_data)
            # print("output " + str(output[0][0]))
            # print("\n")

            # Determine the bot's move based on the output
            if output[0][0] > .6:
                super().handle_computer_input(1)
            elif output[0][0] < .4:
                super().handle_computer_input(2)
            else:
                super().handle_computer_input(0)


        def get_weights_and_biases(self):
            return np.concatenate((self.W1.flatten(), self.b1.flatten(), self.W2.flatten(), self.b2.flatten()))

        def set_weights_and_biases(self, weights_and_biases):
            weight_size = self.input_size * self.hidden_size
            bias_size = self.hidden_size
            W1_start = 0
            W1_end = weight_size
            b1_start = W1_end
            b1_end = b1_start + bias_size
            W2_start = b1_end
            W2_end = W2_start + self.hidden_size * self.output_size
            b2_start = W2_end
            b2_end = b2_start + self.output_size

            self.W1 = np.reshape(weights_and_biases[W1_start:W1_end], (self.input_size, self.hidden_size))
            self.b1 = np.reshape(weights_and_biases[b1_start:b1_end], (1, self.hidden_size))
            self.W2 = np.reshape(weights_and_biases[W2_start:W2_end], (self.hidden_size, self.output_size))
            self.b2 = np.reshape(weights_and_biases[b2_start:b2_end], (1, self.output_size))


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

    def handle_quit_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self, bots=[]):
        # bot_1 = self.Bot(self, "B1")
        # bot_2 = self.Bot(self, "B2")
        # bot_3 = self.NeuralNetworkBot(self, "NB1", 30)
        # user_1 = self.User(self, "U1")

        while True:
            self.handle_quit_event()
            self.drop_new_block()
            self.draw_objects()            

            # User Controlled
            # user_1.handle_input()

            # Computer Controlled (0 = only right, 1 = only left
            # between (0-1) = random chance of left or right based on percent_chance)
            # bot_1.random_move(0.0)
            # bot_2.random_move(0.5)
            # bot_3.determine_move()
            for bot in bots:
                bot.determine_move()

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(60)

            # print(pygame.time.get_ticks())

            if pygame.time.get_ticks() >= 10000:
                return

if __name__ == "__main__":
    game = RaindropGame()

    bot_0 = RaindropGame.NeuralNetworkBot(game, "NB0", 5)
    bot_1 = RaindropGame.NeuralNetworkBot(game, "NB1", 10)
    bot_2 = RaindropGame.NeuralNetworkBot(game, "NB2", 15)
    bot_3 = RaindropGame.NeuralNetworkBot(game, "NB3", 20)
    bot_4 = RaindropGame.NeuralNetworkBot(game, "NB4", 25)
    bot_5 = RaindropGame.NeuralNetworkBot(game, "NB5", 30)
    bot_6 = RaindropGame.NeuralNetworkBot(game, "NB6", 35)
    bot_7 = RaindropGame.NeuralNetworkBot(game, "NB7", 40)
    bot_8 = RaindropGame.NeuralNetworkBot(game, "NB8", 45)
    bot_9 = RaindropGame.NeuralNetworkBot(game, "NB9", 50)

    bots = [bot_0, bot_1, bot_2, bot_3, bot_4, bot_5, bot_6, bot_7, bot_8, bot_9]

    game.run(bots)

    for bot in bots:
        print(bot.name + " fitness: " + str(bot.fitness))

    pygame.quit()
    sys.exit()

