from strategy import Strategy
from strategy import HumanStrategy
from strategy.mcts_strategy import MCTSStrategy


class GomokuEngine:
    # 0 if nothing, 1 if player 1, 2 if player 2
    board = []
    board_size = 11
    has_start_position_been_set = False
    has_swap_query_occurred = False
    player_1_color = "white"
    player_2_color = "black"

    def __init__(self, board_size=11):
        self.board = [["" for _ in range(board_size)] for _ in range(board_size)]
        self.board_size = board_size

    def get_current_board(self):
        return self.board

    def has_game_ended(self):
        winning_color = self.has_color_won()
        if winning_color == "":
            return 0
        return 1 if self.has_color_won()==self.player_1_color else 2

    def has_color_won(self):
        for rowIndex, row in enumerate(self.board):
            for columnIndex, cell in enumerate(row):
                if cell == "":
                    continue
                # Check horizontal
                should_end = True
                for number_of in range(1, 5):
                    if number_of+columnIndex >= len(self.board) or self.board[rowIndex][columnIndex+number_of] != cell:
                        should_end = False
                        break
                if should_end:
                    return cell
                # Check vertical
                should_end = True
                for number_of in range(1, 5):
                    if number_of+rowIndex >= len(self.board) or self.board[rowIndex+number_of][columnIndex] != cell:
                        should_end = False
                        break
                if should_end:
                    return cell
                # Check diagonal from NW to SE
                should_end = True
                for number_of in range(1, 5):
                    if (number_of+rowIndex >= len(self.board)
                            or number_of+columnIndex >= len(self.board)
                            or self.board[rowIndex+number_of][columnIndex+number_of] != cell):
                        should_end = False
                        break
                if should_end:
                    return cell
                # Check diagonal from NE to SW
                should_end = True
                for number_of in range(1, 5):
                    if (number_of+rowIndex >= len(self.board)
                            or columnIndex-number_of < 0
                            or self.board[rowIndex+number_of][columnIndex-number_of] != cell):
                        should_end = False
                        break
                if should_end:
                    return cell
        return ""

    # Returns which players turn is next
    def apply_strategy(self, player_strategy: Strategy, player_index: int) -> int:
        if self.has_swap_query_occurred and self.has_start_position_been_set:
            move_x, move_y = player_strategy.get_next_move(board=self.board)
            if player_index != 1 and player_index != 2:
                raise "Unknown player index"
            if self.board[move_y][move_x] != "":
                raise ValueError("Place on board already taken")
            self.board[move_y][move_x] = self.player_1_color if player_index == 1 else self.player_2_color
        elif not self.has_start_position_been_set:
            self.has_start_position_been_set = True
            self.board = player_strategy.get_start_swap_position(self.board)
        else:
            self.has_swap_query_occurred = True
            if not player_strategy.choose_starting_color(self.board):
                print(f"Player {player_index} choose black")
                return player_index
            self.player_1_color, self.player_2_color = self.player_2_color, self.player_1_color
            print(f"Player {player_index} choose white")
        return 1 if player_index == 2 else 2

    def print_board(self):
        for i in self.board:
            s = ""
            for j in i:
                s += " "
                if j != "":
                    s += "1" if j == self.player_1_color else "2"
                else:
                    s += "0"
            print(s)


# For manual tests purposes
if __name__ == "__main__":
    board_size = 5
    engine = GomokuEngine(board_size=board_size)

    active_player = 1
    non_active_player = 2
    start_board = [["" for _ in range(board_size)] for _ in range(board_size)]
    # start_board[3][4] = "white"
    # start_board[3][3] = "black"
    # start_board[4][4] = "white"
    engine.apply_strategy(HumanStrategy(None, start_board, False), active_player)
    active_player = engine.apply_strategy(HumanStrategy(None, start_board, False), non_active_player)
    # engine.print_board()
    # while engine.has_game_ended() == 0:
    #     x, y = map(int, input(f"Enter where Player {active_player} wants to move: ").split())
    #     active_player = engine.apply_strategy(HumanStrategy((x, y), None, None), active_player)
    #     engine.print_board()

    while engine.has_game_ended() == 0:
        if active_player == 1:
            x, y = map(int, input(f"Enter where Player {active_player} wants to move: ").split())
            x -= 1
            y -= 1
            active_player = engine.apply_strategy(HumanStrategy((y, x), None, None), active_player)
        else:
            # Let the MCTS algorithm choose a move
            active_player = engine.apply_strategy(MCTSStrategy(None, engine.get_current_board(), None), active_player)
        print()
        engine.print_board()

    print(f"Player {engine.has_game_ended()} won!")

