from mctsTwo.boardTwo import Board
from mctsTwo.mctsTwo import mctsTwo
from strategy import Strategy


class MCTSStrategyDawcio(Strategy):
    choose_white = None

    def __init__(self, player_id, choose_white = True):
        self.player_id = player_id
        self.choose_white = choose_white

    def get_next_move(self, board, last_move:(int, int)) -> (int, int):
        player2 = mctsTwo(player_id=self.player_id, iterations=1000)
        move = player2.get_move(Board.from_2d_matrix(board))
        return move[1], move[0]

    def get_start_swap_position(self, board):
        return self.start_board

    # If returns true if wants to play white
    def choose_starting_color(self, board) -> bool:
        return self.choose_white