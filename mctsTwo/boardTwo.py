import copy


class Board:
    def __init__(self, size: int = 15):
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.moves_played = 0

    def make_move(self, x: int, y: int, player: int):
        if self.is_valid_move(x, y):
            self.grid[x][y] = player
            self.moves_played += 1

    def is_valid_move(self, x: int, y: int) -> bool:
        return self.grid[x][y] == 0 and 0 <= y < self.size and 0 <= x < self.size

    def get_legal_moves(self):
        legal_moves = []
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] == 0:
                    legal_moves.append((x, y))
        return legal_moves

    def is_game_over(self) -> bool:
        winner = self.check_winner()
        if winner != 0:
            return True
        if self.moves_played >= self.size * self.size:
            return True
        return False

    def check_winner(self) -> int:
        # Check all rows, columns, and diagonals for a winner.
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] != 0 and (
                        self._check_line(x, y, 1, 0) or
                        self._check_line(x, y, 0, 1) or
                        self._check_line(x, y, 1, 1) or
                        self._check_line(x, y, 1, -1)
                ):
                    return self.grid[x][y]
        return 0

    def _check_line(self, x: int, y: int, dx: int, dy: int) -> bool:
        player_id = self.grid[x][y]
        for i in range(1, min(5, self.size)):
            nx, ny = x + dx * i, y + dy * i
            if not (0 <= nx < self.size and 0 <= ny < self.size and self.grid[nx][ny] == player_id):
                return False
        return True

    def reset(self):
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.moves_played = 0

    def copy(self):
        new_board = Board(self.size)
        new_board.grid = copy.deepcopy(self.grid)
        new_board.moves_played = self.moves_played
        return new_board

    @staticmethod
    def from_2d_matrix(matrix: list) -> 'Board':
        size = len(matrix)
        new_board = Board(size)
        player_map = {"": 0, "white": 1, "black": 2}
        for x in range(size):
            for y in range(size):
                if matrix[x][y] in player_map:
                    new_board.grid[x][y] = player_map[matrix[x][y]]
                    if new_board.grid[x][y] != 0:
                        new_board.moves_played += 1
        return new_board

