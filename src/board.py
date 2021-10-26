from texttable import Texttable


class Board:
    def __init__(self):
        self._rows = 15
        self._columns = 15
        #Empty squares are marked with a dash
        self._data = [['-' for j in range(self._columns)] for i in range(self._rows)]
        #Count the number of unoccupied squares remaining
        self._free = self._rows * self._columns

    @property
    def row_count(self):
        return self._rows

    @property
    def col_count(self):
        return self._columns

    def get_symbol(self, x, y):
        return self._data[x][y]

    def is_free(self,x,y):
        return self.get_symbol(x,y) == '-'


    def get_available_locations(self):
        """
        Check for free squares on the board
        :return: a list containing all free positions
        """
        available_moves = []
        for col in range(self._columns):
            for row in range(self._rows):
                if self.is_free(row, col):
                    available_moves.append((row, col))
        return available_moves

    def get_row(self,x):
        return self._data[x]

    def get_col(self,y):
        return [row[y] for row in self._data]

    def move(self,x,y,symbol):
        """
        Makes a move on the board
        :param x: the column
        :param y: the row
        :param symbol: the symbol used in making the move
        :return: boolean checking if there are any squares left
        """
        if x > self.col_count and y > self.row_count:
            raise ValueError("Numbers outside of range!")
        if symbol not in ['X', '0']:
            raise Exception("Bad symbol!")
        if self._data[y][x] in ['X', '0']:
            raise Exception("Square already occupied!")
        self._data[y][x] = symbol
        self._free -= 1
        return self._free > 0

    def __str__(self):
        t = Texttable()
        t.header(['A', 'B', 'C', 'D', 'E', 'F','G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', ' '])
        for row in range(self._rows):
            row_data = []
            for index in self._data[row]:
                if index == '-':
                    row_data.append(' ')
                elif index == 'X' or index == '0':
                    row_data.append(index)
            t.add_row(row_data + [row])
        return t.draw()





