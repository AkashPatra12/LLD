import unittest
from collections import deque
from MobileSnakeGameWithThread.SnakeGameWithThreads import (
    Snake, Board, FoodSpawner, RandomFoodStrategy,
    SnakeGameEngine, MockGameServer
)

class TestSnakeGame(unittest.TestCase):

    def test_snake_initial_position(self):
        snake = Snake((2, 3))
        self.assertEqual(snake.get_head(), (2, 3))
        self.assertEqual(len(snake.body), 1)

    def test_snake_movement(self):
        snake = Snake((0, 0))
        snake.set_direction((1, 0))
        snake.move()
        self.assertEqual(snake.get_head(), (1, 0))

    def test_snake_growth(self):
        snake = Snake((0, 0))
        snake.move(grow=True)
        self.assertEqual(len(snake.body), 2)

    def test_board_wrapping(self):
        board = Board(5, 5)
        self.assertEqual(board.wrap_position((6, 7)), (1, 2))

    def test_food_not_on_snake(self):
        snake_body = deque([(0, 0), (1, 0)])
        spawner = FoodSpawner(RandomFoodStrategy())
        food = spawner.spawn_food(10, 10, snake_body)
        self.assertNotIn(food, snake_body)

    def test_mock_server_input(self):
        server = MockGameServer()
        server.add_input((0, 1))
        self.assertEqual(server.fetch_remote_moves(), (0, 1))
        self.assertIsNone(server.fetch_remote_moves())

    def test_game_engine_updates_snake_position(self):
        server = MockGameServer()
        game = SnakeGameEngine(board_width=5, board_height=5, server=server)
        initial_head = game.snake.get_head()
        game.update()
        new_head = game.snake.get_head()
        self.assertNotEqual(initial_head, new_head)

if __name__ == '__main__':
    unittest.main()
