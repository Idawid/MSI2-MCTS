import numpy as np
from collections import defaultdict


class MonteCarloTreeSearchNode:
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = self.untried_actions()

    def untried_actions(self) -> list:
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    def q(self) -> int:
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self) -> int:
        return self._number_of_visits

    def expand(self) -> 'MonteCarloTreeSearchNode':
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self) -> bool:
        return self.state.is_game_over()

    def rollout(self) -> int:
        current_rollout_state = self.state
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()

    def backpropagate(self, result: int) -> None:
        self._number_of_visits += 1
        self._results[result] += 1
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self) -> bool:
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1) -> 'MonteCarloTreeSearchNode':
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves: list) -> int:
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self) -> 'MonteCarloTreeSearchNode':
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self) -> 'MonteCarloTreeSearchNode':
        simulation_no = 100
        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        return self.best_child(c_param=0.1)


class State:
    def __init__(self, board: list):
        self.board = board

    def get_legal_actions(self) -> list:
        legal_actions = []
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] == "":
                    legal_actions.append((row, col))
        return legal_actions

    def is_game_over(self) -> bool:
        return self._has_game_ended() != -1

    def game_result(self) -> int:
        result = self._has_game_ended()
        if result == 1:
            return 1  # Player 1 wins
        elif result == 2:
            return -1  # Player 2 wins
        else:
            return 0  # Draw or game is not

    def move(self, action: tuple) -> 'State':
        player_color = self._get_current_color()  # 1 or 2 as we don't have the game engine here xD
        new_board = [row[:] for row in self.board]  # Make a deep copy of the board
        new_board[action[0]][action[1]] = player_color
        return State(new_board)

    def _get_current_color(self) -> str:
        # 1P 2P made moves, now it's 1P turn.
        # 1P made move, now it's 2P turn.
        white_moves = sum(row.count('white') for row in self.board)
        black_moves = sum(row.count('black') for row in self.board)
        return 'white' if white_moves == black_moves else 'black'

    def _has_game_ended(self) -> int:
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                color = self.board[row][col]
                if color != "":
                    # Check horizontal
                    if col + 4 < len(self.board) and all(self.board[row][col + i] == color for i in range(5)):
                        return 1 if color == 'white' else 2
                    # Check vertical
                    if row + 4 < len(self.board) and all(self.board[row + i][col] == color for i in range(5)):
                        return 1 if color == 'white' else 2
                    # Check diagonal
                    if row + 4 < len(self.board) and col + 4 < len(self.board) and all(
                            self.board[row + i][col + i] == color for i in range(5)):
                        return 1 if color == 'white' else 2
                    # Check anti-diagonal
                    if row + 4 < len(self.board) and col - 4 >= 0 and all(
                            self.board[row + i][col - i] == color for i in range(5)):
                        return 1 if color == 'white' else 2

        if any("" in row for row in self.board):
            return -1  # Game is not over, there are possible moves
        else:
            return 0  # Draw, no winner and no more possible moves
