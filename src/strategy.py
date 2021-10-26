from board import Board
import math
import random
from copy import deepcopy

class Strategy:
    def next_move(self,board):
        """
        Return the computer's next move
        """
        raise Exception('Subclass strategy in order to implement computer play')

class RandomMoveStrategy(Strategy):

    def next_move(self,board):
        """
        Make a random valid move
        """
        available_moves = []
        for col in range(board.col_count):
            for row in range(board.row_count):
                if board.is_free(row,col):
                    available_moves.append((row,col))
        move = random.choice(available_moves)
        return board.move(move[1], move[0], '0')


class BetterStrategy(Strategy):

    @staticmethod
    def evaluate_window(window, symbol):
        """
        THis function takes as parameter a sequence of symbols (for eg. on a row, col, diagonal), and counts the repeating symbols
        then calculates the score accordingly
        :param window:sequence of symbols, a list
        :param symbol:the symbol that we need to check for repeated occurences
        :return:the score
        """
        score = 0
        opponent_symbol = 'X'
        if symbol == opponent_symbol:
            opponent_symbol = '0'

        if window.count(symbol) == 5:
            score += 10000
        elif window.count(symbol) == 4 and window.count('-') == 1:
            score += 80
        elif window.count(symbol) == 3 and window.count('-') == 2:
            score += 10
        elif window.count(symbol) == 2 and window.count('-') == 3:
            score += 2

        if window.count(opponent_symbol) == 4 and window.count('-') == 1:
            score -= 100

        if window.count(opponent_symbol) == 3 and window.count('-') == 2:
            score -= 60


        return score

    def score_position(self,board,symbol='0'):
        """
        This function creates arrays for each row, column and diagonal and sends them as parameters
        to the evaluate_window function which then computes the score accordingly
        :param board: the board of the game
        :param symbol: the symbol we need to check for repeated occurences. The default is the symbol
        with which the computer plays
        :return: the score for the array
        """
        score = 0

        #Aim for the center
        for x in range((board.row_count // 2 )- 3, (board.row_count // 2 ) + 3):
            for y in range((board.col_count // 2)-3, (board.col_count // 2) + 3):
                center_array = [board.get_symbol(x,y + i) for i in range(4)]
                center_count = center_array.count(symbol)
                score += center_count


        #Score Horizontal
        for x in range(board.row_count):
            row_array = board.get_row(x)[:]
            for y in range(board.col_count - 4):
                window = row_array[y:y+5]
                score += self.evaluate_window(window,symbol)


        #Score Vertical
        for y in range(board.col_count):
            col_array = board.get_col(y)[:]
            for x in range(board.row_count - 4):
                window = col_array[x:x+5]
                score += self.evaluate_window(window,symbol)

        #Score Positive Slope Diagonal
        for x in range(board.row_count - 4):
            for y in range(board.col_count - 4):
                window = [board.get_symbol(x+i,y+i) for i in range(5)]
                score += self.evaluate_window(window, symbol)

        #Score Negative Slope Diagonal
        for x in range(board.row_count - 4):
            for y in range(board.col_count - 4):
                window = [board.get_symbol(x + 4 - i, y + i) for i in range(5)]
                score += self.evaluate_window(window, symbol)

        return score



    def best_move(self,board,symbol):
        """
        This function decides which is the best move for teh computer to make
        :param board: the game board
        :param symbol: the symbol according to which we make the best move
        :return: A tuple representing the ideal position that yields the highest score
        """
        # We choose a negative score so that the computer will be more tempted to block the opponent
        best_score = -1000
        best_placement = random.choice(board.get_available_locations())
        available_locations = board.get_available_locations()
        for location in available_locations:
            temp_board = deepcopy(board)
            temp_board.move(location[1],location[0],symbol)
            score = self.score_position(temp_board,symbol)
            if score > best_score:
                best_score = score
                best_placement = location
        return best_placement

    @staticmethod
    def winning_move(board,symbol):
        """
        This function checks all rows, columns and diagonals for repeating symbols.
        :param board: the game board
        :param symbol: the symbol we need to check for repeating occurences
        :return: True if 5 repeating symbols are found
        """
        #Check horizontal locations for win
        for y in range(board.col_count - 4):
            for x in range(board.row_count):
                if board.get_symbol(x,y) == symbol and board.get_symbol(x,y+1) == symbol and board.get_symbol(x,y+2) == symbol and board.get_symbol(x,y+3) == symbol and board.get_symbol(x,y+4) == symbol:
                    return True

        #Check vertical locations for win
        for y in range(board.col_count):
            for x in range(board.row_count - 4):
                if board.get_symbol(x,y) == symbol and board.get_symbol(x+1,y) == symbol and board.get_symbol(x+2,y) == symbol and board.get_symbol(x+3,y) == symbol and board.get_symbol(x+4,y) == symbol:
                    return True

        #Check positively sloped diagonals
        for y in range(board.col_count - 4):
            for x in range(board.row_count - 4):
                if board.get_symbol(x,y) == symbol and board.get_symbol(x+1,y+1) == symbol and board.get_symbol(x+2, y+2) == symbol and board.get_symbol(x+3,y+3) == symbol and board.get_symbol(x+4,y+4) == symbol:
                    return True

        #Check negatively sloped diagonals
        for y in range(board.col_count - 4):
            for x in range(4, board.row_count):
                if board.get_symbol(x,y) == symbol and board.get_symbol(x-1,y+1) == symbol and board.get_symbol(x-2,y+2) == symbol and board.get_symbol(x-3,y+3) == symbol and board.get_symbol(x-4, y+4) == symbol:
                    return True


    def next_move(self,board):
        """
        This function makes the next move of the computer on the position returned by best_move
        :param board: the game board
        :return: same return value as the move method of the board
        """
        best_placement = self.best_move(board,'0')
        return board.move(best_placement[1], best_placement[0],'0')
