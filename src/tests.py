import unittest
from board import Board
from strategy import RandomMoveStrategy, BetterStrategy
from game import Game
class TestGame(unittest.TestCase):
    def setUp(self):
        self._good_strategy = BetterStrategy()
        self._game = Game(self._good_strategy)

    def test_board(self):
        board = Board()
        self.assertEqual(board.row_count, 15)
        self.assertEqual(board.col_count, 15)
        self.assertEqual(len(board.get_available_locations()), 15*15 )
        try:
            board.move(16,16,'X')
        except ValueError:
            assert True
        try:
            board.move(2, 3, 'U')
        except Exception:
            assert True
        board.move(3,5,'X')
        self.assertEqual(board.get_symbol(5,3), 'X')
        self.assertEqual(len(board.get_available_locations()), 15*15-1)
        self.assertEqual(board.get_row(5), ['-', '-', '-', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'])
        self.assertEqual(board.get_col(3),['-', '-', '-', '-', '-', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-'])
        try:
            board.move(3, 5, '0')
        except Exception:
            assert True

    def test_strategy_horiz(self):
        board = Board()
        board.move(5,5, '0')
        board.move(6,5, '0')
        board.move(7,5, '0')
        self.assertEqual(self._good_strategy.score_position(board, '0'), 43)
        self.assertTrue(self._good_strategy.best_move(board, '0') == (5,4) or  self._good_strategy.best_move(board, '0') == (5,8))
        for i in range(4):
            board.move(8+i,9,'X')
        self.assertTrue(self._good_strategy.best_move(board, '0') == (9,12) or self._good_strategy.best_move(board, '0') == (9,7))
        #Block opponent from both sides
        self._good_strategy.next_move(board)
        self._good_strategy.next_move(board)
        #Score
        self._good_strategy.next_move(board)
        self._good_strategy.next_move(board)
        self.assertTrue(self._good_strategy.winning_move(board, '0'))

    def test_strategy_vertical(self):
        board = Board()
        board.move(5, 6, '0')
        board.move(5, 7, '0')
        board.move(5, 8, '0')
        self.assertEqual(self._good_strategy.score_position(board, '0'), 40)
        self.assertTrue(self._good_strategy.best_move(board, '0') == (5, 5) or self._good_strategy.best_move(board, '0') == (8, 5))
        self._good_strategy.next_move(board)
        self._good_strategy.next_move(board)
        self.assertTrue(self._good_strategy.winning_move(board, '0'))

    def test_strategy_diagonal(self):
        board1 = Board()
        board1.move(5, 5, '0')
        board1.move(6, 6, '0')
        board1.move(7, 7, '0')
        self.assertTrue(self._good_strategy.best_move(board1, '0') == (4, 4) or self._good_strategy.best_move(board1, '0') == (8, 8))
        self._good_strategy.next_move(board1)
        self._good_strategy.next_move(board1)
        self.assertTrue(self._good_strategy.winning_move(board1, '0'))
        board2 = Board()
        board2.move(8, 8, '0')
        board2.move(9, 7, '0')
        board2.move(10, 6,'0')
        self.assertTrue(self._good_strategy.best_move(board2, '0') == (11, 5) or self._good_strategy.best_move(board2, '0') == (9,7))
        self._good_strategy.next_move(board2)
        self._good_strategy.next_move(board2)
        self.assertTrue(self._good_strategy.winning_move(board2, '0'))
