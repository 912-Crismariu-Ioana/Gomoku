from strategy import RandomMoveStrategy,Strategy,Board, BetterStrategy
import random

class Game:
    def __init__(self,strategy):
        self._board = Board()
        self._strategy = strategy

    @property
    def board(self):
        return self._board

    def human_move(self,x,y):
        return self._board.move(x,y,'X')

    def computer_move(self):
        return self._strategy.next_move(self._board)

    def winning_move(self,symbol):
        return self._strategy.winning_move(self._board, symbol)














