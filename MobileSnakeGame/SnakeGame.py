from abc import ABC, abstractmethod
from collections import deque
import random

# --- Interfaces ---

class IFoodStrategy(ABC):
    @abstractmethod
    def generate_food(self, board_width, board_height, snake_body):
        pass

# --- Strategy Pattern for Food Placement ---

class RandomFoodStrategy(IFoodStrategy):
    def generate_food(self, board_width, board_height, snake_body):
        while True:
            x, y = random.randint(0, board_width-1), random.randint(0, board_height-1)
            if (x, y) not in snake_body:
                return (x, y)

# --- Core Game Entities ---

class Snake:
    def __init__(self, start_pos=(0, 0)):
        self.body = deque([start_pos])
        self.direction = (1, 0)  # moving right initially

    def move(self, grow=False):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.appendleft(new_head)
        if not grow:
            self.body.pop()

    def set_direction(self, direction):
        self.direction = direction

    def get_head(self):
        return self.body[0]

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def wrap_position(self, pos):
        x, y = pos
        return (x % self.width, y % self.height)

class FoodSpawner:
    def __init__(self, strategy: IFoodStrategy):
        self.strategy = strategy

    def spawn_food(self, board_width, board_height, snake_body):
        return self.strategy.generate_food(board_width, board_height, snake_body)

class GameLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameLogger, cls).__new__(cls)
        return cls._instance

    def log_event(self, event):
        print(f"LOG: {event}")

class Renderer:
    def render(self, board, snake, food):
        print("\n" + "=" * board.width)
        for y in range(board.height):
            row = ''
            for x in range(board.width):
                if (x, y) == food:
                    row += 'F'
                elif (x, y) in snake.body:
                    row += 'S'
                else:
                    row += '.'
            print(row)
        print("=" * board.width + "\n")

class InputHandler:
    def __init__(self):
        self.callbacks = []

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def on_input(self, direction):
        for cb in self.callbacks:
            cb(direction)

# --- Game Engine ---

class SnakeGameEngine:
    def __init__(self, board_width=10, board_height=10):
        self.board = Board(board_width, board_height)
        self.snake = Snake()
        self.food_spawner = FoodSpawner(RandomFoodStrategy())
        self.food = self.food_spawner.spawn_food(board_width, board_height, self.snake.body)
        self.logger = GameLogger()
        self.renderer = Renderer()
        self.input_handler = InputHandler()
        self.input_handler.register_callback(self.handle_input)
        self.running = True

    def handle_input(self, direction):
        self.snake.set_direction(direction)

    def update(self):
        self.snake.move()
        head = self.board.wrap_position(self.snake.get_head())
        self.snake.body[0] = head
        if head == self.food:
            self.logger.log_event("Food eaten")
            self.snake.move(grow=True)
            self.food = self.food_spawner.spawn_food(self.board.width, self.board.height, self.snake.body)
        self.renderer.render(self.board, self.snake, self.food)

    def start_game(self, steps=10):
        for _ in range(steps):
            if not self.running:
                break
            self.update()

# --- Example Usage ---

if __name__ == "__main__":
    game = SnakeGameEngine()
    # Simulate some direction changes
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for dir in directions:
        game.input_handler.on_input(dir)
        game.update()


import threading
import time

class GameServerInterface(ABC):
    @abstractmethod
    def sync_state(self, game_state):
        pass

    @abstractmethod
    def fetch_remote_moves(self):
        pass

class MockGameServer(GameServerInterface):
    def __init__(self):
        self.state = None
        self.input_queue = deque()
        self.lock = threading.Lock()

    # def sync_state(self, game_state):
    #     with self.lock:
    #         self.state = game_state

    # def fetch_remote_moves(self):
    #     with self.lock:
    #         if self.input_queue:
    #             return self.input_queue.popleft()
    #         return None

    def add_input(self, direction):
        with self.lock:
            self.input_queue.append(direction)

# --- Example Usage ---

def run_game():
    game = SnakeGameEngine()
    game.start_game(steps=10)

# if __name__ == "__main__":
#     server = MockGameServer()
#     server.add_input((1, 0))  # right
#     server.add_input((0, 1))  # down
#     server.add_input((-1, 0))  # left
#
#     game_thread = threading.Thread(target=run_game)
#     game_thread.start()
#
#     # Simulate external input
#     time.sleep(2)
#     server.add_input((0, -1))  # up
#     server.add_input((1, 0))   # right
#     game_thread.join()