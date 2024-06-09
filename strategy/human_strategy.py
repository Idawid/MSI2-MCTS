from strategy import Strategy


class HumanStrategy(Strategy):
    next_move = (None, None)
    start_board = None
    choose_white = None

    def __init__(self, next_move, start_board, choose_white):
        self.next_move = next_move
        self.start_board = start_board
        self.choose_white = choose_white

    def get_next_move(self, board) -> (int, int):
        return self.next_move

    def get_start_swap_position(self, board):
        return self.start_board

    # If returns true if wants to play white
    def choose_starting_color(self, board) -> bool:
        return self.choose_white
