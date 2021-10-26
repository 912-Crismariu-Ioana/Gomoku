from game import Game,RandomMoveStrategy, BetterStrategy
class UI:
    def __init__(self):
        self._strategy = BetterStrategy()
        self._game = Game(self._strategy)

    def read_human_move(self):
        coord = input('play>')
        try:
            row = int(coord[1:])
            col = ord(coord[0].lower()) - 97
        except ValueError:
            print("Invalid Input!")
            return
        return row, col

    def start(self):
        finished = False
        human_turn = True

        while not finished:
            print(self._game.board)
            if human_turn:
                try:
                    coord = self.read_human_move()
                    self._game.human_move(coord[1], coord[0])
                except Exception as e:
                    print(str(e))
                    human_turn = human_turn
                    continue
                if self._game.winning_move('X') is True:
                    print("You win!")
                    print(self._game.board)
                    return

            else:
                self._game.computer_move()
                if self._game.winning_move('0') is True:
                    print("I win!")
                    print(self._game.board)
                    return

            human_turn = not human_turn


