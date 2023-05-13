import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('Helvetica.ttf', 25)

# Credits for inspiration, direction and tutorials to Python Engineer (https://github.com/patrickloeber)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# Declaring constants with RGB colour-codes
WHITE = (255, 255, 255)
RED = (200, 0, 0)
# This and the following Blue make up together the snake player
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
# Screen background
BLACK = (0, 0, 0)

# Additional constants with the size of the block that compose the snake and the speed of the snake/player. They can
# be changed, but I found these values pretty good after testing.
BLOCK_SIZE = 20
SPEED = 18


class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display and the game title
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake game')
        self.clock = pygame.time.Clock()

        # init game state / starts the game
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

# Function to place the food
    # The function first generates two random numbers, x and y, between 0 and the width or
    # height of the grid, respectively. The function then creates a new Point object with the coordinates x and y and
    # assigns it to the food attribute of the self object.
    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # 1. This piece of code will collect user input when playing the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # 2. This will move the snake character
        self._move(self.direction)  # update the head
        self.snake.insert(0, self.head)

        # 3. This will check if there is a game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. Place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5. This is to update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def _is_collision(self):
        # This is to identify when the snake is hitting the walls
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # This is to identify when the snake is hitting itself
        if self.head in self.snake[1:]:
            return True

        return False

# The _update_ui function takes one argument, self, which is an object that represents the game. The function updates
    # the user interface by drawing the snake, the food, and the score on the display.

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

# The _move function takes two arguments, self and direction. The function moves the head of the snake in the
    # specified direction.
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)


if __name__ == '__main__':
    game = SnakeGame()

    # Main Loop
    while True:
        game_over, score = game.play_step()

        if game_over:
            break

    print('Congratulations! Your Final Score is: ', score)

    pygame.quit()
