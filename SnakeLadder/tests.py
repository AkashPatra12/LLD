# command to see coverage - coverage report -m
import unittest
from unittest.mock import patch
from collections import deque
from SnakeLadder import *

# Assuming all classes are in a module named `snake_ladder_game`
# from snake_ladder_game import Player, NormalDice, BiasedDice, Board, Game, SnakeTile, LadderTile

class TestSnakeLadderGame(unittest.TestCase):

    def test_player_initial_position(self):
        p = Player("TestPlayer")
        self.assertEqual(p.position, 0)

    def test_biased_dice_always_returns_same(self):
        dice = BiasedDice(4)
        for _ in range(10):
            self.assertEqual(dice.roll(), 4)

    def test_normal_dice_in_range(self):
        dice = NormalDice()
        for _ in range(100):
            roll = dice.roll()
            self.assertTrue(1 <= roll <= 6)

    def test_snake_tile_moves_back(self):
        tile = SnakeTile(3)
        self.assertEqual(tile.move(99), 3)

    def test_ladder_tile_moves_forward(self):
        tile = LadderTile(77)
        self.assertEqual(tile.move(4), 77)

    def test_board_snake_and_ladder(self):
        board = Board(100)
        board.add_snake(20, 5)
        board.add_ladder(10, 90)
        self.assertIsInstance(board.tiles[20], SnakeTile)
        self.assertIsInstance(board.tiles[10], LadderTile)
        self.assertEqual(board.go_next(20), 5)
        self.assertEqual(board.go_next(10), 90)
        self.assertEqual(board.go_next(15), 15)  # NormalTile

    def test_game_turn_movement(self):
        board = Board(30)
        dice = BiasedDice(4)
        player1 = Player("A")
        player2 = Player("B")
        game = Game(board, [player1, player2], dice)
        game.play_turn()
        self.assertEqual(player1.position, 4)
        self.assertEqual(player2.position, 0)

    def test_game_win_condition(self):
        board = Board(10)
        board.add_ladder(6, 10)
        p = Player("Hero")
        game = Game(board, [p], BiasedDice(6))
        with patch('builtins.print') as mock_print:
            game.start()
            self.assertEqual(p.position, 10)
            mock_print.assert_any_call("Hero wins!")

if __name__ == '__main__':
    unittest.main()
