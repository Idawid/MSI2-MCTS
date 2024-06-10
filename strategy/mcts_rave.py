from mctsTwo.boardTwo import Board
from mctsTwo.mctsRAVE import mctsRAVE
from strategy import Strategy


class MCTSStrategyRAVE(Strategy):
    choose_white = None

    def __init__(self, player_id, choose_white = True):
        self.player_id = player_id
        self.choose_white = choose_white

    def get_next_move(self, board) -> (int, int):
        player2 = mctsRAVE(player_id=self.player_id, iterations=100)
        move = player2.get_move(Board.from_2d_matrix(board))
        return move[1], move[0]

    def get_start_swap_position(self, board):
        return self.start_board

    # If returns true if wants to play white
    def choose_starting_color(self, board) -> bool:
        return self.choose_white