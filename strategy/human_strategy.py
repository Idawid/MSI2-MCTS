from strategy import Strategy


class HumanStrategy(Strategy):
    next_move = (None, None)

    def __init__(self, next_move):
        self.next_move = next_move

    def get_next_move(self, board) -> (int, int):
        return self.next_move
