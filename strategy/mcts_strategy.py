from mcts.mcts_node import State, MonteCarloTreeSearchNode
from strategy import Strategy


class MCTSStrategy(Strategy):
    next_move = (None, None)
    start_board = None
    choose_white = None

    def __init__(self, next_move, start_board, choose_white = True):
        self.next_move = next_move
        self.start_board = start_board
        self.choose_white = choose_white

    def get_next_move(self, board) -> (int, int):
        state = State(board)
        mcts_root = MonteCarloTreeSearchNode(state)
        selected_node = mcts_root.best_action()

        action = selected_node.parent_action

        return action[1], action[0]

    def get_start_swap_position(self, board):
        return self.start_board

    # If returns true if wants to play white
    def choose_starting_color(self, board) -> bool:
        return self.choose_white
