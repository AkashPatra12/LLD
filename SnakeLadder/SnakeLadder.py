'''
entities: player, dice, snake, ladder, board, game
'''
from abc import ABC, abstractmethod
from collections import deque
from random import randint


class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0

class Dice(ABC):
    @abstractmethod
    def roll(self):
        pass

class NormalDice(Dice):
    def roll(self):
        return randint(1,6)

class BiasedDice(Dice):
    def __init__(self, value):
        self.value = value

    def roll(self):
        return self.value

class Tile(ABC):
    @abstractmethod
    def move(self, player_position):
        pass

class NormalTile(Tile):
    def move(self, player_position):
        return player_position

class SnakeTile(Tile):
    def __init__(self, end_pos):
        self.end_pos = end_pos

    def move(self, _):
        return self.end_pos

class LadderTile(Tile):
    def __init__(self, end_pos):
        self.end_pos = end_pos

    def move(self, _):
        return self.end_pos

class Board:
    def __init__(self, size):
        self.size = size
        self.tiles = [NormalTile() for _ in range(size+1)]

    def add_snake(self, start, end):
        self.tiles[start] = SnakeTile(end)

    def add_ladder(self, start, end):
        self.tiles[start] = LadderTile(end)

    def go_next(self, position):
        return self.tiles[position].move(position)

class Game:
    def __init__(self, board: Board, players: list, dice: Dice):
        self.board = board
        self.players = deque(players)
        self.dice = dice

    def play_turn(self):
        player = self.players.popleft()
        roll = self.dice.roll()
        next_pos = player.position + roll
        if next_pos <= self.board.size:
            player.position = self.board.go_next(next_pos)
        print(f"{player.name} moved to {player.position}")
        if player.position == self.board.size:
            print(f"{player.name} wins!")
            return True
        self.players.append(player)
        return False

    def start(self):
        while True:
            if self.play_turn():
                break


players = [Player("Alice"), Player("Bob")]

board = Board(100)
dice = NormalDice()

board.add_snake(99, 2)
board.add_snake(95, 13)
board.add_ladder(4, 90)
board.add_ladder(10, 40)

game = Game(board, players, dice)
game.start()