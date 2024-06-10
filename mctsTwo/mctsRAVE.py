import random
from copy import deepcopy
import math


class NodeRAVE:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.amaf_wins = {}
        self.amaf_visits = {}
        self.move = move  # Store the move that led to this node

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_moves())

    def best_child(self, c_param=0.9, rave_bias=0.5):
        choices_weights = []
        for child in self.children:
            if child.visits > 0:
                exploitation = child.wins / child.visits
                exploration = math.sqrt((2 * math.log(self.visits) / child.visits))

                action = child.move
                if action in self.amaf_visits and self.amaf_visits[action] > 0:
                    rave_exploitation = self.amaf_wins[action] / self.amaf_visits[action]
                    beta = self.amaf_visits[action] / (self.visits + self.amaf_visits[action] + 4 * self.visits * self.amaf_visits[action])
                    combined_value = (1 - beta) * exploitation + beta * rave_exploitation
                else:
                    combined_value = exploitation

                choices_weights.append(combined_value + c_param * exploration)
            else:
                choices_weights.append(float('inf'))
        return self.children[choices_weights.index(max(choices_weights))]

    def add_child(self, child_node):
        self.children.append(child_node)


class mctsRAVE:
    def __init__(self, player_id: int, iterations: int = 1000):
        self.player_id = player_id
        self.iterations = iterations

    def get_move(self, board: 'Board'):
        root = NodeRAVE(deepcopy(board))
        for _ in range(self.iterations):
            node = self._select(root)
            if not node.state.is_game_over():
                node = self._expand(node)
            result, path = self._simulate(node.state)
            self._backpropagate(node, result, path)
        best_move = self._get_best_move(root)
        return best_move

    def _select(self, node: NodeRAVE):
        while node.is_fully_expanded() and not node.state.is_game_over():
            node = node.best_child()
        return node

    def _expand(self, node: NodeRAVE):
        legal_moves = node.state.get_legal_moves()
        for move in legal_moves:
            new_state = deepcopy(node.state)
            new_state.make_move(move[0], move[1], self.player_id)
            child_node = NodeRAVE(new_state, node, move)
            node.add_child(child_node)
        return random.choice(node.children)

    def _simulate(self, board: 'Board'):
        current_board = deepcopy(board)
        current_player = self.player_id
        path = []
        while not current_board.is_game_over():
            legal_moves = current_board.get_legal_moves()
            move = random.choice(legal_moves)
            current_board.make_move(move[0], move[1], current_player)
            path.append((move[0], move[1], current_player))
            current_player = 3 - current_player  # Toggle between player 1 and 2
        return current_board.check_winner(), path

    def _backpropagate(self, node: NodeRAVE, result, path):
        visited = set()
        while node is not None:
            node.visits += 1
            if result == self.player_id:
                node.wins += 1
            elif result != 0:
                node.wins -= 1

            for (x, y, player) in path:
                if (x, y) not in visited:
                    if (x, y) not in node.amaf_wins:
                        node.amaf_wins[(x, y)] = 0
                        node.amaf_visits[(x, y)] = 0
                    if player == self.player_id:
                        node.amaf_wins[(x, y)] += 1
                    node.amaf_visits[(x, y)] += 1
                    visited.add((x, y))

            node = node.parent

    def _get_best_move(self, root: NodeRAVE):
        best_child = root.best_child()
        for child in root.children:
            if child == best_child:
                for x in range(root.state.size):
                    for y in range(root.state.size):
                        if root.state.grid[x][y] != best_child.state.grid[x][y]:
                            return x, y
