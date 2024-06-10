from mcts.mcts_node import State, MonteCarloTreeSearchNode
from strategy import Strategy


class MCTSStrategy(Strategy):

    def __init__(self, board_size, choose_white=True, sim_no=100):
        self.start_board = [["" for _ in range(board_size)] for _ in range(board_size)]
        self.start_board[0][0] = "white"
        self.start_board[0][1] = "white"
        self.start_board[1][1] = "black"
        self.choose_white = choose_white
        self.sim_no = sim_no

    def get_next_move(self, board, last_move: (int, int)) -> (int, int):
        state = State(board)
        mcts_root = MonteCarloTreeSearchNode(state, sim_no=self.sim_no)
        selected_node = mcts_root.best_action()

        action = selected_node.parent_action

        return action[1], action[0]

    def get_start_swap_position(self, board):
        return self.start_board

    # If returns true if wants to play white
    def choose_starting_color(self, board) -> bool:
        return self.choose_white
