from abc import ABC, abstractmethod
from collections import deque
import random

# --- Interfaces ---

# Abstract interface for food generation strategy
class IFoodStrategy(ABC):
    @abstractmethod
    def generate_food(self, board_width, board_height, snake_body):
        pass

# --- Strategy Pattern for Food Placement ---

# Concrete strategy to generate random food on the board
class RandomFoodStrategy(IFoodStrategy):
    def generate_food(self, board_width, board_height, snake_body):
        # Keep generating random positions until we find one that's not occupied by the snake
        while True:
            x, y = random.randint(0, board_width - 1), random.randint(0, board_height - 1)
            if (x, y) not in snake_body:
                return (x, y)

# --- Core Game Entities ---

# Snake class manages the snake's body, movement, and direction
class Snake:
    def __init__(self, start_pos=(0, 0)):
        self.body = deque([start_pos])  # Deque used for fast head/tail operations
        self.snake_set = set([start_pos])  # For quick lookup
        self.direction = (1, 0)         # Initially moving right

    # Moves the snake in the current direction; grows if `grow=True`
    def move(self, grow=False):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.appendleft(new_head)  # Add new head
        self.snake_set.add(new_head)
        if not grow:
            tail = self.body.pop()  # Remove tail if not growing
            self.snake_set.remove(tail)

    def set_direction(self, direction):
        self.direction = direction

    def get_head(self):
        return self.body[0]

    def hits_itself(self):
        # Head is already added, so if it's seen more than once, it's a self-hit
        return self.body[0] in self.snake_set and self.body.count(self.body[0]) > 1

# Board class stores board dimensions and provides boundary check
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    # Check if a position is outside board boundaries
    def is_out_of_bounds(self, pos):
        x, y = pos
        return x < 0 or x >= self.width or y < 0 or y >= self.height

# Spawner class to generate food using a strategy
class FoodSpawner:
    def __init__(self, strategy: IFoodStrategy):
        self.strategy = strategy

    # Spawn food only if there’s empty space left
    def spawn_food(self, board_width, board_height, snake_body):
        total_cells = board_width * board_height
        if len(snake_body) == total_cells:
            print("Snake filled the board. You win!")  # No space left
            return None
        return self.strategy.generate_food(board_width, board_height, snake_body)

# Handles external inputs (like direction changes) using registered callbacks
class InputHandler:
    def __init__(self):
        self.callbacks = []  # List of functions to call on input

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def on_input(self, direction):
        for cb in self.callbacks:
            cb(direction)  # Trigger each callback with direction input

# --- Game Engine ---

class SnakeGameEngine:
    def __init__(self, board_width=10, board_height=10):
        self.board = Board(board_width, board_height)
        self.snake = Snake()
        self.food_spawner = FoodSpawner(RandomFoodStrategy())
        self.food = self.food_spawner.spawn_food(board_width, board_height, self.snake.body)
        self.input_handler = InputHandler()
        self.input_handler.register_callback(self.handle_input)
        self.running = True  # Game is active

    # Update the snake’s direction
    def handle_input(self, direction):
        self.snake.set_direction(direction)

    # Print the current game board to the console
    def print_board(self):
        print("\n" + "=" * self.board.width)
        for y in range(self.board.height):
            row = ''
            for x in range(self.board.width):
                if (x, y) == self.food:
                    row += 'F'  # Food
                elif (x, y) in self.snake.body:
                    row += 'S'  # Snake segment
                else:
                    row += '.'  # Empty cell
            print(row)
        print("=" * self.board.width + "\n")

    # Main game update logic (runs once per tick/step)
    def update(self):
        if not self.running:
            return

        self.snake.move()
        head = self.snake.get_head()

        # Snake collides with itself
        if self.snake.hits_itself():
            print("Snake hit itself. Game Over!")
            self.running = False
            return

        # Snake hits the wall
        if self.board.is_out_of_bounds(head):
            print("Snake hit the boundary. Game Over!")
            self.running = False
            return

        # Snake eats the food
        if head == self.food:
            print("Food eaten")
            self.snake.move(grow=True)  # Move again with growth
            self.food = self.food_spawner.spawn_food(self.board.width, self.board.height, self.snake.body)
            if self.food is None:
                self.running = False  # Game ends if snake fills the board
                return

        self.print_board()

    # Start the game loop for `steps` number of updates
    def start_game(self, steps=10):
        for _ in range(steps):
            if not self.running:
                print("Game stopped.")
                break
            self.update()

# --- Example Usage ---

if __name__ == "__main__":
    game = SnakeGameEngine()
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Simulated direction changes: right, down, left, up
    for dir in directions:
        game.input_handler.on_input(dir)
        game.update()
