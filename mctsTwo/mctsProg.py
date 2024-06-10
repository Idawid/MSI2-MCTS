import random
from copy import deepcopy
import math


class NodeProg:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.move = move  # Store the move that led to this node
        self.untried_moves = state.get_legal_moves()

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, c_param=0.9):
        choices_weights = []
        for child in self.children:
            if child.visits > 0:
                exploitation = child.wins / child.visits
                exploration = math.sqrt((2 * math.log(self.visits) / child.visits))
                choices_weights.append(exploitation + c_param * exploration)
            else:
                choices_weights.append(float('inf'))
        return self.children[choices_weights.index(max(choices_weights))]

    def add_child(self, move, state):
        child_node = NodeProg(state, self, move)
        self.untried_moves.remove(move)
        self.children.append(child_node)
        return child_node


class mctsProg:
    def __init__(self, player_id: int, iterations: int = 1000, max_children: int = 10):
        self.player_id = player_id
        self.iterations = iterations
        self.max_children = max_children

    def get_move(self, board: 'Board'):
        root = NodeProg(deepcopy(board))
        for _ in range(self.iterations):
            node = self._select(root)
            if not node.state.is_game_over():
                node = self._expand(node)
            result = self._simulate(node.state)
            self._backpropagate(node, result)
        best_move = self._get_best_move(root)
        return best_move

    def _select(self, node: NodeProg):
        while not node.is_fully_expanded() and not node.state.is_game_over():
            if len(node.children) < self.max_children:
                return node
            node = node.best_child()
        return node

    def _expand(self, node: NodeProg):
        move = random.choice(node.untried_moves)
        new_state = deepcopy(node.state)
        new_state.make_move(move[0], move[1], self.player_id)
        return node.add_child(move, new_state)

    def _simulate(self, board: 'Board'):
        current_board = deepcopy(board)
        current_player = self.player_id
        while not current_board.is_game_over():
            legal_moves = current_board.get_legal_moves()
            move = random.choice(legal_moves)
            current_board.make_move(move[0], move[1], current_player)
            current_player = 3 - current_player  # Toggle between player 1 and 2
        return current_board.check_winner()

    def _backpropagate(self, node: NodeProg, result):
        while node is not None:
            node.visits += 1
            if result == self.player_id:
                node.wins += 1
            elif result != 0:
                node.wins -= 1
            node = node.parent

    def _get_best_move(self, root: NodeProg):
        best_child = root.best_child()
        for child in root.children:
            if child == best_child:
                return child.move
