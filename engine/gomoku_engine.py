from strategy import Strategy
from strategy import HumanStrategy


class GomokuEngine:
    # 0 if nothing, 1 if player 1, 2 if player 2
    board = []
    board_size = 11

    def __init__(self, board_size=11):
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.board_size = board_size

    def get_current_board(self):
        return self.board

    def has_game_ended(self):
        for rowIndex, row in enumerate(self.board):
            for columnIndex, cell in enumerate(row):
                if cell == 0:
                    continue
                # Check horizontal
                should_end = True
                for number_of in range(1, 5):
                    if number_of+columnIndex >= self.board_size or self.board[rowIndex][columnIndex+number_of] != cell:
                        should_end = False
                        break
                if should_end:
                    return cell
                # Check vertical
                should_end = True
                for number_of in range(1, 5):
                    if number_of+rowIndex >= self.board_size or self.board[rowIndex+number_of][columnIndex] != cell:
                        should_end = False
                        break
                if should_end:
                    return cell
                # Check diagonal from NW to SE
                should_end = True
                for number_of in range(1, 5):
                    if (number_of+rowIndex >= self.board_size
                            or number_of+columnIndex >= self.board_size
                            or self.board[rowIndex+number_of][columnIndex+number_of] != cell):
                        should_end = False
                        break
                if should_end:
                    return cell
                # Check diagonal from NE to SW
                should_end = True
                for number_of in range(1, 5):
                    if (number_of+rowIndex >= self.board_size
                            or number_of-columnIndex < 0
                            or self.board[rowIndex+number_of][columnIndex-number_of] != cell):
                        should_end = False
                        break
                if should_end:
                    return cell
        return 0

    def apply_strategy(self, player_strategy: Strategy, player_index: int):
        move = player_strategy.get_next_move(board=self.board)
        if player_index != 1 and player_index != 2:
            raise "Unknown player index"
        if self.board[move[0]][move[1]] != 0:
            raise "Place on board already taken"
        self.board[move[0]][move[1]] = player_index


def print_board(printable_engine: GomokuEngine):
    b = printable_engine.get_current_board()
    for i in b:
        s = ""
        for j in i:
            s += " " + str(j)
        print(s)


if __name__ == "__main__":
    engine = GomokuEngine()

    print_board(engine)
    active_player = 1
    non_active_player = 2
    while engine.has_game_ended() == 0:
        y, x = map(int, input(f"Enter where Player {active_player} wants to move: ").split())
        engine.apply_strategy(HumanStrategy((x, y)), active_player)
        active_player, non_active_player = non_active_player, active_player
        print_board(engine)
    print(f"Player {engine.has_game_ended()} won!")

